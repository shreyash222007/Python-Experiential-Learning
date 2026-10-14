import sqlite3
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).with_name("expenses.db")
CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Others"]


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                description TEXT
            )
        """)
        conn.commit()


def fetch_expenses():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, date, amount, category, description "
            "FROM expenses ORDER BY date DESC, id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def add_expense(date_value, amount, category, description):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO expenses (date, amount, category, description) "
            "VALUES (?, ?, ?, ?)",
            (date_value.strftime("%d-%m-%Y"), float(amount), category, description.strip())
        )
        conn.commit()


def delete_expense(expense_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (int(expense_id),))
        conn.commit()


def money(value):
    return f"₹{value:,.2f}"


st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰", layout="wide")
initialize_database()

st.title("💰 Personal Expense Tracker")
st.caption("Record expenses, understand your spending, and view monthly charts.")

expenses = fetch_expenses()
total = sum(item["amount"] for item in expenses)

m1, m2, m3 = st.columns(3)
m1.metric("Total Spending", money(total))
m2.metric("Number of Expenses", len(expenses))
m3.metric("Categories Used", len(set(item["category"] for item in expenses)))

tab_add, tab_view, tab_summary, tab_search, tab_delete, tab_report = st.tabs([
    "➕ Add Expense", "📋 All Expenses", "📊 Summary",
    "🔎 Search", "🗑️ Delete", "📅 Monthly Report"
])

with tab_add:
    st.subheader("Add a new expense")
    with st.form("add_expense_form", clear_on_submit=True):
        expense_date = st.date_input("Date", value=datetime.today().date())
        amount = st.number_input("Amount (₹)", min_value=0.01, step=10.0, format="%.2f")
        category = st.selectbox("Category", CATEGORIES)
        description = st.text_input("Description", placeholder="e.g. Lunch, bus ticket")
        submitted = st.form_submit_button("Save Expense", type="primary")
        if submitted:
            add_expense(expense_date, amount, category, description)
            st.success("Expense added successfully!")
            st.rerun()

with tab_view:
    st.subheader("All expenses")
    if expenses:
        df = pd.DataFrame(expenses)
        df = df.rename(columns={
            "date": "Date", "amount": "Amount (₹)",
            "category": "Category", "description": "Description"
        })
        st.dataframe(df[["Date", "Amount (₹)", "Category", "Description"]],
                     use_container_width=True, hide_index=True)
        st.info(f"Total expense: {money(total)}")
    else:
        st.info("No expenses found. Add an expense to get started.")

with tab_summary:
    st.subheader("Category-wise summary")
    if expenses:
        summary = {}
        for item in expenses:
            summary[item["category"]] = summary.get(item["category"], 0) + item["amount"]
        summary_df = pd.DataFrame(
            [{"Category": category, "Amount (₹)": amount}
             for category, amount in summary.items()]
        ).sort_values("Amount (₹)", ascending=False)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        fig, ax = plt.subplots()
        ax.bar(summary_df["Category"], summary_df["Amount (₹)"])
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Spending by Category")
        ax.tick_params(axis="x", rotation=25)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No expenses available for a summary.")

with tab_search:
    st.subheader("Search by category")
    search_category = st.selectbox("Choose category", CATEGORIES, key="search_category")
    matches = [item for item in expenses if item["category"] == search_category]
    if matches:
        search_df = pd.DataFrame(matches).rename(columns={
            "date": "Date", "amount": "Amount (₹)",
            "category": "Category", "description": "Description"
        })
        st.dataframe(search_df[["Date", "Amount (₹)", "Category", "Description"]],
                     use_container_width=True, hide_index=True)
        st.write("Category total:", money(sum(item["amount"] for item in matches)))
    else:
        st.info("No expenses found in this category.")

with tab_delete:
    st.subheader("Delete an expense")
    if expenses:
        options = {
            f'{item["date"]} | {item["category"]} | {money(item["amount"])} | {item["description"]}': item["id"]
            for item in expenses
        }
        selected_label = st.selectbox("Select expense to delete", list(options.keys()))
        confirm = st.checkbox("I confirm that I want to delete this expense.")
        if st.button("Delete selected expense", type="primary"):
            if confirm:
                delete_expense(options[selected_label])
                st.success("Expense deleted.")
                st.rerun()
            else:
                st.warning("Please tick the confirmation box first.")
    else:
        st.info("There are no expenses to delete.")

with tab_report:
    st.subheader("Monthly visual report")
    month_col, year_col = st.columns(2)
    with month_col:
        selected_month = st.selectbox("Month", list(range(1, 13)),
                                      format_func=lambda month: datetime(2000, month, 1).strftime("%B"))
    with year_col:
        years = sorted({datetime.strptime(item["date"], "%d-%m-%Y").year
                        for item in expenses}, reverse=True)
        selected_year = st.selectbox("Year", years if years else [datetime.today().year])

    monthly = []
    for item in expenses:
        item_date = datetime.strptime(item["date"], "%d-%m-%Y")
        if item_date.month == selected_month and item_date.year == selected_year:
            monthly.append(item)

    if monthly:
        category_totals = {}
        for item in monthly:
            category_totals[item["category"]] = (
                category_totals.get(item["category"], 0) + item["amount"]
            )
        monthly_total = sum(category_totals.values())
        st.metric("Monthly Total", money(monthly_total))
        st.dataframe(
            pd.DataFrame([{"Category": key, "Amount (₹)": value}
                          for key, value in category_totals.items()]),
            use_container_width=True, hide_index=True
        )

        left, right = st.columns(2)
        with left:
            fig_bar, ax_bar = plt.subplots()
            ax_bar.bar(category_totals.keys(), category_totals.values())
            ax_bar.set_xlabel("Category")
            ax_bar.set_ylabel("Amount (₹)")
            ax_bar.set_title("Monthly Expense Report")
            ax_bar.tick_params(axis="x", rotation=25)
            fig_bar.tight_layout()
            st.pyplot(fig_bar)
            plt.close(fig_bar)
        with right:
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(category_totals.values(), labels=category_totals.keys(),
                       autopct="%1.1f%%", startangle=90)
            ax_pie.set_title("Monthly Expense Distribution")
            fig_pie.tight_layout()
            st.pyplot(fig_pie)
            plt.close(fig_pie)
    else:
        st.info("No expenses found for the selected month.")

st.divider()
st.caption("Personal Expense Tracker • Python + Streamlit + SQLite + Matplotlib")
