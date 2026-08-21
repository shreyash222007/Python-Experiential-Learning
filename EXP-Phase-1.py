# Personal Expense Tracker - Phase 1

expenses = []

def add_expense():
    print("\n----- Add Expense -----")

    date = input("Enter Date (DD-MM-YYYY): ")

    while True:
        try:
            amount = float(input("Enter Amount: ₹"))
            if amount <= 0:
                print("Amount should be greater than 0.")
            else:
                break
        except ValueError:
            print("Please enter a valid amount.")

    category = input("Enter Category (Food/Travel/Shopping/Bills/Others): ")
    description = input("Enter Description: ")

    expense = {
        "Date": date,
        "Amount": amount,
        "Category": category,
        "Description": description
    }

    expenses.append(expense)

    print("\nExpense Added Successfully!")


def view_expenses():

    if len(expenses) == 0:
        print("\nNo Expenses Found!")
        return

    print("\n---------------- Expense List ----------------")
    print("{:<12} {:<10} {:<15} {:<20}".format(
        "Date", "Amount", "Category", "Description"))
    print("-" * 60)

    total = 0

    for expense in expenses:

        print("{:<12} ₹{:<9.2f} {:<15} {:<20}".format(
            expense["Date"],
            expense["Amount"],
            expense["Category"],
            expense["Description"]
        ))

        total = total + expense["Amount"]

    print("-" * 60)
    print("Total Expense = ₹", total)


