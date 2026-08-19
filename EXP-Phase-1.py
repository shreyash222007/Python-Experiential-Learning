# Personal Expense Tracker - Phase 1

expenses = []

def add_expense():
    print("\n----- Add Expense -----")

    date = input("Enter Date (DD-MM-YYYY): ")

    while True:
        try:
            amount = float(input("Enter Amount: ₹"))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
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
    print("\n========== Expense List ==========")

    if len(expenses) == 0:
        print("No expenses found.")
        return

    print("{:<12} {:<10} {:<15} {:<20}".format(
        "Date", "Amount", "Category", "Description"))

    print("-" * 60)

    for expense in expenses:
        print("{:<12} ₹{:<9.2f} {:<15} {:<20}".format(
            expense["Date"],
            expense["Amount"],
            expense["Category"],
            expense["Description"]
        ))


def main():
    while True:
        print("\n========== Personal Expense Tracker ==========")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense()

        elif choice == '2':
            view_expenses()

        elif choice == '3':
            print("\nThank you for using Personal Expense Tracker!")
            break

        else:
            print("Invalid choice! Please try again.")


main()
    
