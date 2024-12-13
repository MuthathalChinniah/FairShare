from tkinter import *
from tkinter import messagebox
import database_communication as db


# Add Expense Page
class AddExpensePage:
    def __init__(self, parent_frame, friends, groups):
        self.parent_frame = parent_frame
        self.friends = friends
        self.groups = groups

        # Clear any existing content in the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Description field
        self.description_label = Label(self.parent_frame, text="Description", font=("Arial", 12), fg="white", bg="#2d2d2d")
        self.description_label.pack(pady=5)

        self.description_entry = Entry(self.parent_frame, font=("Arial", 12), width=40)
        self.description_entry.pack(pady=10)

        # Amount field with Dollar currency symbol
        self.amount_label = Label(self.parent_frame, text="Amount ($)", font=("Arial", 12), fg="white", bg="#2d2d2d")
        self.amount_label.pack(pady=5)

        self.amount_entry = Entry(self.parent_frame, font=("Arial", 12), width=40)
        self.amount_entry.pack(pady=10)

        # Groups listbox
        self.group_label = Label(self.parent_frame, text="Select Group", font=("Arial", 12), fg="white", bg="#2d2d2d")
        self.group_label.pack(pady=5)

        self.group_listbox = Listbox(self.parent_frame, font=("Arial", 12), width=40, height=4)
        self.group_listbox.pack(pady=10)

        # Populate group listbox with group names from the previous tab
        for group in self.groups:
            self.group_listbox.insert(END, group)

        self.group_listbox.bind("<<ListboxSelect>>", self.update_friends_list)



        # Paid by options (You and someone else)
        self.paid_by_label = Label(self.parent_frame, text="Paid by: Select Friend", font=("Arial", 12), fg="white", bg="#2d2d2d")
        self.paid_by_label.pack(pady=5)

        self.paid_by_frame = Frame(self.parent_frame, bg="#2d2d2d")
        self.paid_by_frame.pack(pady=10)

        # Friends listbox
        members = ["Select an Option"]
        self.value_inside = StringVar()
        self.value_inside.set("Select an Option")
        self.friend_listbox = OptionMenu(self.parent_frame, self.value_inside, *members)
        self.friend_listbox.config(width=20, font=("Arial", 12))
        self.friend_listbox.pack(pady=10)

        # Confirm button to submit the expense details
        self.submit_button = Button(self.parent_frame, text="Submit", font=("Arial", 14, "bold"), bg="#32a852",
                                    fg="white", width=15, height=2)
        self.submit_button.pack(pady=20)

        # Event handler for submit button
        self.submit_button.config(command=self.submit_expense)
    def update_friends_list(self, e):
        # Populate friend listbox
        i = self.group_listbox.curselection()
        if not i:
            messagebox.showwarning("Selection Error", "Please select at least one group!")
            return
        selected_g = self.group_listbox.get(i)
        members = db.get_group_members(self.groups[selected_g])
        self.friend_listbox["menu"].delete(0, "end")  # Clear existing options

        # Add new options
        for option in members:
            self.friend_listbox["menu"].add_command(label=option, command=lambda value=option: self.value_inside.set(value))

    def submit_expense(self):
        """Handle the expense submission."""
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        i = self.group_listbox.curselection()
        if not i:
            messagebox.showwarning("Selection Error", "Please select at least one group!")
            return
        selected_group_name = self.group_listbox.get(i)
        group_id = self.groups[selected_group_name]
        members = db.get_group_members(group_id)

        friend = self.value_inside.get()
        if friend not in members:
            messagebox.showwarning("Selection Error", "Please select at least one friend name!")
            return



        friend_id = members[friend]
        status, msg = db.add_group_expense(friend_id, group_id, amount, description)
        if not status:
            messagebox.showwarning("Error", msg)
            return
        self.description_entry.delete(0, END)
        self.amount_entry.delete(0, END)
        self.value_inside.set("Select an Option")
        self.group_listbox.selection_clear(0, END)