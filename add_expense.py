from tkinter import *
from tkinter import messagebox
import database_communication as db

class AddExpensePage:
    def __init__(self, parent_frame, friends, groups):
        self.parent_frame = parent_frame
        self.friends = friends
        self.groups = groups

        # Clear any existing content in the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Description field
        Label(self.parent_frame, text="Description", font=("Arial", 12), fg="white", bg="#2d2d2d").pack(pady=5)
        self.description_entry = Entry(self.parent_frame, font=("Arial", 12), width=40)
        self.description_entry.pack(pady=10)

        # Amount field
        Label(self.parent_frame, text="Amount ($)", font=("Arial", 12), fg="white", bg="#2d2d2d").pack(pady=5)
        self.amount_entry = Entry(self.parent_frame, font=("Arial", 12), width=40)
        self.amount_entry.pack(pady=10)

        # Group selection
        Label(self.parent_frame, text="Select Group", font=("Arial", 12), fg="white", bg="#2d2d2d").pack(pady=5)
        self.group_listbox = Listbox(self.parent_frame, font=("Arial", 12), width=40, height=4)
        self.group_listbox.pack(pady=10)
        for group in self.groups:
            self.group_listbox.insert(END, group)
        self.group_listbox.bind("<<ListboxSelect>>", self.update_friends_list)

        # Paid by selection
        Label(self.parent_frame, text="Paid by: Select Friend", font=("Arial", 12), fg="white", bg="#2d2d2d").pack(pady=5)
        self.value_inside = StringVar(value="Select an Option")
        self.friend_listbox = OptionMenu(self.parent_frame, self.value_inside, "Select an Option")
        self.friend_listbox.config(width=20, font=("Arial", 12))
        self.friend_listbox.pack(pady=10)

        # Submit button
        self.submit_button = Button(self.parent_frame, text="Submit", font=("Arial", 14, "bold"), bg="#32a852",
                                    fg="white", width=15, height=2, command=self.submit_expense)
        self.submit_button.pack(pady=20)

    def update_friends_list(self, e):
        selected_group_index = self.group_listbox.curselection()
        if not selected_group_index:
            messagebox.showwarning("Selection Error", "Please select a group!")
            return
        group_name = self.group_listbox.get(selected_group_index)
        members = db.get_group_members(self.groups[group_name])

        # Update the dropdown with group members
        menu = self.friend_listbox["menu"]
        menu.delete(0, "end")
        for member in members:
            menu.add_command(label=member, command=lambda value=member: self.value_inside.set(value))

    def submit_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        group_index = self.group_listbox.curselection()
        if not group_index:
            messagebox.showwarning("Selection Error", "Please select a group!")
            return

        selected_group = self.group_listbox.get(group_index)
        group_id = self.groups[selected_group]
        selected_friend = self.value_inside.get()

        if selected_friend == "Select an Option":
            messagebox.showwarning("Selection Error", "Please select who paid!")
            return

        status, msg = db.add_group_expense(selected_friend, group_id, amount, description)
        if not status:
            messagebox.showwarning("Error", msg)
            return

        # Clear fields after success
        self.description_entry.delete(0, END)
        self.amount_entry.delete(0, END)
        self.value_inside.set("Select an Option")
        self.group_listbox.selection_clear(0, END)
