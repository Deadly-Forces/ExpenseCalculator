import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ExpenseManager:
    def jls_extract_def(self):  # Light blue background
        return

    def __init__(self, master):
        self.master = master
        master.title("Expense Manager")
        master.config(bg="#f0f8ff")  # Light blue background
        self.total_expenses = 0.0
        self.monthly_income = 0.0
        self.loan_balance = 0.0  # New variable to track loan balance

        # Income Frame
        income_frame = tk.LabelFrame(master, text="Income", bg="#ffcccb")
        income_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.monthly_income_label = tk.Label(income_frame, text="Please Put Your Monthly Income:", bg="#ffcccb")
        self.monthly_income_label.grid(row=0, column=0, padx=5, pady=5)
        self.monthly_income_entry = tk.Entry(income_frame)
        self.monthly_income_entry.grid(row=0, column=1, padx=5, pady=5)
        self.set_income_button = tk.Button(income_frame, text="Set Income", command=self.set_income)
        self.set_income_button.grid(row=0, column=2, padx=5, pady=5)

        # Expense Frame
        expense_frame = tk.LabelFrame(master, text="Expense", bg="#add8e6")
        expense_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.category_label = tk.Label(expense_frame, text="Category:", bg="#add8e6")
        self.category_label.grid(row=0, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(expense_frame)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)
        self.description_label = tk.Label(expense_frame, text="Description:", bg="#add8e6")
        self.description_label.grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(expense_frame)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)
        self.amount_label = tk.Label(expense_frame, text="Amount:", bg="#add8e6")
        self.amount_label.grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(expense_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)
        self.add_expense_button = tk.Button(expense_frame, text="Add Expense", command=self.add_expense)
        self.add_expense_button.grid(row=3, column=0, padx=5, pady=5)
        self.delete_expense_button = tk.Button(expense_frame, text="Delete Selected", command=self.delete_expense)
        self.delete_expense_button.grid(row=3, column=1, padx=5, pady=5)
        self.reset_button = tk.Button(expense_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=3, column=2, padx=5, pady=5)

        # Expense List Frame
        expense_list_frame = tk.LabelFrame(master, text="Expense List", bg="#90ee90")
        expense_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.expense_list_tree = ttk.Treeview(expense_list_frame, columns=("Category", "Description", "Amount"))
        self.expense_list_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.expense_list_tree.heading("#0", text="ID")
        self.expense_list_tree.heading("Category", text="Category")
        self.expense_list_tree.heading("Description", text="Description")
        self.expense_list_tree.heading("Amount", text="Amount")
        self.expense_list_tree.column("#0", width=50)
        self.expense_list_tree.column("Category", width=100)
        self.expense_list_tree.column("Description", width=200)
        self.expense_list_tree.column("Amount", width=100)

        # History Frame
        history_frame = tk.LabelFrame(master, text="History", bg="#ffebcd")
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.total_expenses_label = tk.Label(history_frame, text="Your Total Expenses: $0.00", bg="#ffebcd")
        self.total_expenses_label.pack(padx=5, pady=5)
        self.remaining_balance_label = tk.Label(history_frame, text="Your Remaining Balance: $0.00", bg="#ffebcd")
        self.remaining_balance_label.pack(padx=5, pady=5)

    def set_income(self):
        try:
            self.monthly_income = float(self.monthly_income_entry.get())
            messagebox.showinfo("Income Set", f"Monthly income set to ${self.monthly_income:.2f}")
            self.update_balance()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid income amount.")

    def add_expense(self):
        category = self.category_entry.get()
        description = self.description_entry.get()
        try:
            amount = float(self.amount_entry.get())
            # Check if expenses exceed the income
            if self.total_expenses + amount > self.monthly_income + self.loan_balance:
                # If expenses exceed income + loan, prompt for loan
                response = messagebox.askyesno(
                    "Exceeding Budget", 
                    f"Your expenses exceed your budget. Do you want to take a loan to cover this amount?"
                )
                if response:
                    loan_amount = self.ask_for_loan_amount(amount)
                    if loan_amount:
                        self.loan_balance += loan_amount
                        messagebox.showinfo("Loan Added", f"Loan of ${loan_amount:.2f} added to your balance.")
                    else:
                        return  # If user cancels or inputs invalid loan amount, don't proceed with expense
                else:
                    return  # If user doesn't want a loan, don't proceed with expense
            self.total_expenses += amount
            self.expense_list_tree.insert("", "end", values=(category, description, f"${amount:.2f}"))
            self.update_balance()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def ask_for_loan_amount(self, required_amount):
        loan_amount = simpledialog.askfloat("Loan Amount", f"How much loan do you need to cover the remaining balance? You need ${required_amount - (self.monthly_income + self.loan_balance - self.total_expenses):.2f}.")
        if loan_amount and loan_amount > 0:
            return loan_amount
        return 0  # Return 0 if invalid loan amount or user cancels

    def delete_expense(self):
        selected_item = self.expense_list_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to delete.")
            return
        amount = self.expense_list_tree.item(selected_item)['values'][2].replace('$', '')
        self.total_expenses -= float(amount)
        self.expense_list_tree.delete(selected_item)
        self.update_balance()

    def update_balance(self):
        remaining_balance = self.monthly_income + self.loan_balance - self.total_expenses
        self.total_expenses_label.config(text=f"Your Total Expenses: ${self.total_expenses:.2f}")
        self.remaining_balance_label.config(text=f"Your Remaining Balance: ${remaining_balance:.2f}")

    def reset(self):
        self.monthly_income_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.expense_list_tree.delete(*self.expense_list_tree.get_children())
        self.total_expenses = 0.0
        self.monthly_income = 0.0
        self.loan_balance = 0.0  # Reset loan balance
        self.total_expenses_label.config(text="Your Total Expenses: $0.00")
        self.remaining_balance_label.config(text="Your Remaining Balance: $0.00")

import tkinter.simpledialog as simpledialog

root = tk.Tk()
my_gui = ExpenseManager(root)
root.mainloop()
