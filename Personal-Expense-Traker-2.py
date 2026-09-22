# Personal Expense Tracker - Phase 2

expenses = []


# 1. ADD EXPENSE
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

    category = input(
        "Enter Category (Food/Travel/Shopping/Bills/Others): "
    )

    description = input("Enter Description: ")

    expense = {
        "Date": date,
        "Amount": amount,
        "Category": category,
        "Description": description
    }

    expenses.append(expense)

    print("\nExpense Added Successfully!")


# 2. VIEW EXPENSES
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
    print("Total Expense = ₹{:.2f}".format(total))


# 3. TOTAL EXPENSE
def total_expense():

    if len(expenses) == 0:
        print("\nNo Expenses Found!")
        return

    total = 0

    for expense in expenses:
        total = total + expense["Amount"]

    print("\n----- Total Expense -----")
    print("Total Expense = ₹{:.2f}".format(total))


# 4. CATEGORY-WISE SUMMARY
def category_summary():

    if len(expenses) == 0:
        print("\nNo Expenses Found!")
        return

    category_total = {}

    for expense in expenses:

        category = expense["Category"]
        amount = expense["Amount"]

        if category in category_total:
            category_total[category] += amount
        else:
            category_total[category] = amount

    print("\n----- Category-wise Summary -----")

    for category, amount in category_total.items():
        print("{} : ₹{:.2f}".format(category, amount))


# 5. SEARCH EXPENSE BY CATEGORY
def search_by_category():

    if len(expenses) == 0:
        print("\nNo Expenses Found!")
        return

    search_category = input(
        "\nEnter Category to Search: "
    )

    found = False

    print("\n----- Search Result -----")

    for expense in expenses:

        if expense["Category"].lower() == search_category.lower():

            print(
                "Date: {} | Amount: ₹{:.2f} | Description: {}".format(
                    expense["Date"],
                    expense["Amount"],
                    expense["Description"]
                )
            )

            found = True

    if not found:
        print("No expense found in this category.")


# 6. DELETE EXPENSE
def delete_expense():

    if len(expenses) == 0:
        print("\nNo Expenses Found!")
        return

    print("\n----- Delete Expense -----")

    for i, expense in enumerate(expenses, start=1):

        print(
            "{}. {} | ₹{:.2f} | {} | {}".format(
                i,
                expense["Date"],
                expense["Amount"],
                expense["Category"],
                expense["Description"]
            )
        )

    while True:

        try:
            choice = int(input("\nEnter expense number to delete: "))

            if 1 <= choice <= len(expenses):

                deleted_expense = expenses.pop(choice - 1)

                print("\nExpense Deleted Successfully!")

                print(
                    "Deleted: {} | ₹{:.2f} | {}".format(
                        deleted_expense["Date"],
                        deleted_expense["Amount"],
                        deleted_expense["Category"]
                    )
                )

                break

            else:
                print("Please enter a valid expense number.")

        except ValueError:
            print("Please enter a valid number.")


# 7. MONTHLY VISUAL REPORT



# 8. MAIN MENU
while True:

    print("\n========================================")
    print("       PERSONAL EXPENSE TRACKER")
    print("========================================")

    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Show Total Expense")
    print("4. Category-wise Summary")
    print("5. Search Expense by Category")
    print("6. Delete Expense")
    print("7. Generate Monthly Visual Report")
    print("8. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        total_expense()

    elif choice == "4":
        category_summary()

    elif choice == "5":
        search_by_category()

    elif choice == "6":
        delete_expense()

    elif choice == "7":
        monthly_report()

    elif choice == "8":
        print("\nThank you for using Personal Expense Tracker!")
        break

    else:
        print("\nInvalid choice! Please try again.")