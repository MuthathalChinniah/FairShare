from tkinter import *
from tkinter import messagebox


class AddExpensePage:
    def __init__(self, window):
        self.window = window
        self.window.title("Add Expense")
        self.window.geometry("600x600")
        self.window.configure(bg="#2d2d2d")

        # Header for Add Expense
        self.header_label = Label(self.window, text="Add expense", font=("Arial", 20, "bold"), fg="white", bg="#2d2d2d")
        self.header_label.pack(pady=20)

        # Description field
        self.description_label = Label(self.window, text="Enter a description", font=("Arial", 12), fg="white", bg="#2d2d2d")
        self.description_label.pack(pady=5)

        self.description_entry = Entry(self.window, font=("Arial", 12), width=40)
        self.description_entry.pack(pady=10)

        # Amount field with Dollar currency symbol
        self.amount_label = Label(self.window, text="Amount ($)", font=("Arial", 12), fg="white", bg="#2d2d2d")
        self.amount_label.pack(pady=5)

        self.amount_entry = Entry(self.window, font=("Arial", 12), width=40)
        self.amount_entry.pack(pady=10)

        # Paid by options (You and someone else)
        self.paid_by_label = Label(self.window, text="Paid by", font=("Arial", 12), fg="white", bg="#2d2d2d")
        self.paid_by_label.pack(pady=5)

        self.paid_by_frame = Frame(self.window, bg="#2d2d2d")
        self.paid_by_frame.pack(pady=10)

        self.paid_by_you_button = Button(self.paid_by_frame, text="You", font=("Arial", 12), bg="#32a852", fg="white", width=10)
        self.paid_by_you_button.grid(row=0, column=0, padx=10)

        self.paid_by_other_button = Button(self.paid_by_frame, text="Other", font=("Arial", 12), bg="#32a852", fg="white", width=10)
        self.paid_by_other_button.grid(row=0, column=1, padx=10)

        # Split equally options
        self.split_label = Label(self.window, text="Split equally", font=("Arial", 12), fg="white", bg="#2d2d2d")
        self.split_label.pack(pady=5)

        self.split_frame = Frame(self.window, bg="#2d2d2d")
        self.split_frame.pack(pady=10)

        self.split_button = Button(self.split_frame, text="Equally", font=("Arial", 12), bg="#32a852", fg="white", width=10)
        self.split_button.grid(row=0, column=0, padx=10)

        # Confirm button to submit the expense details
        self.submit_button = Button(self.window, text="Submit", font=("Arial", 14, "bold"), bg="#32a852", fg="white", width=15, height=2)
        self.submit_button.pack(pady=20)

        # Event handler for submit button
        self.submit_button.config(command=self.submit_expense)

    def submit_expense(self):
        """Handle the expense submission."""
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        if description == "" or amount == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            # Normally, here we would store the expense data, but for now, just show a success message.
            messagebox.showinfo("Success", f"Expense '{description}' of ${amount} added successfully!")

def open_add_expense_page():
    window = Tk()
    AddExpensePage(window)
    window.mainloop()

if __name__ == "__main__":
    open_add_expense_page()
