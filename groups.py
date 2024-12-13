from tkinter import *
from tkinter import messagebox
import database_communication as db

class Groups:
    def __init__(self, user_id):
        self.user_id = user_id
        self.groups = db.all_groups(self.user_id)[1]  # Fetch groups from database

    def build_groups_tab(self, parent_frame, friends):
        Label(parent_frame, text="Group Name:", bg="#F3F4F6", fg="#2C3E50", font=("Arial", 12)).pack(pady=5, padx=10, anchor="w")

        self.group_name_entry = Entry(parent_frame, font=("Arial", 12))
        self.group_name_entry.pack(pady=5, padx=10)

        Label(parent_frame, text="Select Friends:", bg="#F3F4F6", fg="#2C3E50", font=("Arial", 12)).pack(pady=5, padx=10, anchor="w")

        self.group_friends_listbox = Listbox(parent_frame, width=50, height=10, selectmode=MULTIPLE)
        self.group_friends_listbox.pack(pady=5, padx=10)
        for friend in friends:
            self.group_friends_listbox.insert(END, friend)

        Button(parent_frame, text="Create Group", command=self.create_group, bg="#8E44AD", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        Label(parent_frame, text="Existing Groups:", bg="#F3F4F6", font=("Arial", 12)).pack()
        self.groups_listbox = Listbox(parent_frame, width=50, height=10)
        self.groups_listbox.pack()
        for group in self.groups:
            self.groups_listbox.insert(END, group)

    def create_group(self):
        group_name = self.group_name_entry.get().strip()
        if not group_name:
            messagebox.showwarning("Input Error", "Group name cannot be empty!")
            return

        selected_friends = self.group_friends_listbox.curselection()
        if not selected_friends:
            messagebox.showwarning("Selection Error", "Select at least one friend!")
            return

        friends_id_list = [self.group_friends_listbox.get(i) for i in selected_friends]
        status, group_id = db.create_group(self.user_id, group_name, friends_id_list)
        if status:
            self.groups[group_name] = group_id
            self.groups_listbox.insert(END, group_name)
            self.group_name_entry.delete(0, END)

    def get_groups(self):
        return self.groups
