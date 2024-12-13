from tkinter import *
from tkinter import messagebox
import database_communication as db

class Friends:
    def __init__(self, user_id):
        self.user_id = user_id
        self.friends = db.get_friends(self.user_id)  # Fetch friends from database

    def build_friends_tab(self, parent_frame):
        Label(parent_frame, text="Friend's Mobile Number:", bg="#F3F4F6", fg="#2C3E50", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.friend_name_entry = Entry(parent_frame, width=30, font=("Arial", 12))
        self.friend_name_entry.grid(row=0, column=1, padx=10, pady=10)

        Button(parent_frame, text="Add Friend", command=self.add_friend, bg="#27AE60", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10, pady=10)

        self.friends_listbox = Listbox(parent_frame, width=50, height=20, font=("Arial", 10), bg="#ECF0F1")
        self.friends_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        for friend in self.friends:
            self.friends_listbox.insert(END, friend)

    def add_friend(self):
        friend_mobile = self.friend_name_entry.get().strip()
        status, message = db.add_friend(self.user_id, friend_mobile)
        if friend_mobile:
            if status:
                name, id_ = message.rsplit(' ', 1)
                self.friends[name] = id_
                self.friends_listbox.insert(END, name)
                self.friend_name_entry.delete(0, END)
            else:
                messagebox.showwarning("Error", message)
        else:
            messagebox.showwarning("Input Error", "Friend's name cannot be empty!")

    def get_friends(self):
        return self.friends
