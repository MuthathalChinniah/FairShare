from tkinter import *
from tkinter import messagebox
import database_communication as db
from AddExpenseClass import AddExpensePage
from BalancesClass import BalancePage


# FairShare Main Application
class FairShare:
    def __init__(self, root, user_id):
        if not db.user_exists(user_id):
            messagebox.showwarning("Error", "Invalid user!")
            return
        self.root = root
        self.user_id  = user_id
        self.root.title("FairShare App")
        self.root.geometry("800x600")
        self.root.config(bg="#F3F4F6")

        # Initialize data structures
        self.friends = db.get_friends(self.user_id)  # Dict to store friends
        status, self.groups = db.all_groups(user_id) # Dictionary to store groups


        # Main content frame
        self.content_frame = Frame(self.root, bg="#F3F4F6")
        self.content_frame.pack(fill="both", expand=True)

        # Bottom navigation bar
        self.bottom_nav = Frame(self.root, bg="#2C3E50", height=50)
        self.bottom_nav.pack(side="bottom", fill="x")

        # Creating navigation buttons
        self.friends_button = Button(
            self.bottom_nav,
            text="Friends",
            command=self.show_friends_tab,
            bg="#34495E",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#2ECC71",
            relief="flat",
        )
        self.friends_button.pack(side="left", expand=True, fill="both")

        self.groups_button = Button(
            self.bottom_nav,
            text="Groups",
            command=self.show_groups_tab,
            bg="#34495E",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#9B59B6",
            relief="flat",
        )
        self.groups_button.pack(side="left", expand=True, fill="both")

        self.add_expense_button = Button(
            self.bottom_nav,
            text="Add Expense",
            command=self.show_add_expense_tab,
            bg="#34495E",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#E74C3C",
            relief="flat",
        )
        self.add_expense_button.pack(side="left", expand=True, fill="both")

        self.balances_btn = Button(
            self.bottom_nav,
            text="Balances",
            command=self.show_balances,
            bg="#34495E",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#E74C3C",
            relief="flat",
        )
        self.balances_btn.pack(side="left", expand=True, fill="both")

        # Create tabs as frames
        self.friends_tab = Frame(self.content_frame, bg="#F3F4F6")
        self.groups_tab = Frame(self.content_frame, bg="#F3F4F6")
        self.add_expense_tab = Frame(self.content_frame, bg="#F3F4F6")
        self.balances_tab = Frame(self.content_frame, bg="#F3F4F6")

        # Initialize tabs
        self.build_friends_tab()
        self.build_groups_tab()

        # Show the default tab
        self.show_friends_tab()


    def show_friends_tab(self):
        self.groups_tab.pack_forget()
        self.add_expense_tab.pack_forget()
        self.balances_tab.pack_forget()
        self.friends_tab.pack(fill="both", expand=True)

    def show_groups_tab(self):
        self.friends_tab.pack_forget()
        self.add_expense_tab.pack_forget()
        self.balances_tab.pack_forget()
        self.groups_tab.pack(fill="both", expand=True)

    def show_add_expense_tab(self):
        self.friends_tab.pack_forget()
        self.groups_tab.pack_forget()
        self.balances_tab.pack_forget()
        self.add_expense_tab.pack(fill="both", expand=True)
        self.add_expense_page = AddExpensePage(self.add_expense_tab, self.friends, self.groups)

    def show_balances(self):
        self.friends_tab.pack_forget()
        self.groups_tab.pack_forget()
        self.add_expense_tab.pack_forget()
        self.balances_tab.pack(fill="both", expand=True)
        self.balances_page = BalancePage(self.user_id, self.groups, self.balances_tab)

    # FRIENDS TAB
    def build_friends_tab(self):
        Label(
            self.friends_tab, text="Friend's Mobile Number:", bg="#F3F4F6", fg="#2C3E50", font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.friend_name_entry = Entry(self.friends_tab, width=30, font=("Arial", 12))
        self.friend_name_entry.grid(row=0, column=1, padx=10, pady=10)

        add_friend_button = Button(
            self.friends_tab,
            text="Add Friend",
            command=self.add_friend,
            bg="#27AE60",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#2ECC71",
        )
        add_friend_button.grid(row=0, column=2, padx=10, pady=10)

        self.friends_listbox = Listbox(
            self.friends_tab, width=50, height=20, font=("Arial", 10), bg="#ECF0F1", fg="#2C3E50"
        )
        self.friends_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        for friend in self.friends:
            self.friends_listbox.insert(END, friend)

    def add_friend(self):
        friend_mobile = self.friend_name_entry.get().strip()
        status, message = db.add_friend(self.user_id, friend_mobile)
        if friend_mobile:
            if status:
                name, id_ = message.rsplit(' ', 1)
                self.friends [name] = id_
                self.friends_listbox.insert(END, name)
                self.friend_name_entry.delete(0, END)
                self.update_group_friends_listbox()
            else:
                messagebox.showwarning("Error", message)
        else:
            messagebox.showwarning("Input Error", "Friend's name cannot be empty!")

    # GROUPS TAB
    def build_groups_tab(self):
        Label(
            self.groups_tab, text="Group Name:", bg="#F3F4F6", fg="#2C3E50", font=("Arial", 12)
        ).pack(pady=5, padx=10, anchor="w")

        self.group_name_entry = Entry(self.groups_tab, font=("Arial", 12))
        self.group_name_entry.pack(pady=5, padx=10)

        Label(
            self.groups_tab, text="Select Friends:", bg="#F3F4F6", fg="#2C3E50", font=("Arial", 12)
        ).pack(pady=5, padx=10, anchor="w")

        self.group_friends_listbox = Listbox(
            self.groups_tab, width=50, height=10, font=("Arial", 10), selectmode=MULTIPLE, bg="#ECF0F1", fg="#2C3E50"
        )
        self.group_friends_listbox.pack(pady=5, padx=10)
        self.update_group_friends_listbox()

        create_group_button = Button(
            self.groups_tab,
            text="Create Group",
            command=self.create_group,
            bg="#8E44AD",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#9B59B6",
        )
        create_group_button.pack(pady=10)

        Label(
            self.groups_tab, text="Existing Groups:", bg="#F3F4F6", fg="#2C3E50", font=("Arial", 12)
        ).pack(pady=5, padx=10, anchor="w")

        self.groups_listbox = Listbox(
            self.groups_tab, width=50, height=10, font=("Arial", 10), bg="#ECF0F1", fg="#2C3E50"
        )
        self.groups_listbox.pack(pady=5, padx=10)
        for group in self.groups:
            grounp_mem_names = (db.get_group_members (self.groups[group])).keys()
            self.groups_listbox.insert(END, f"{group}: {', '.join(grounp_mem_names)}")

    def create_group(self):
        group_name = self.group_name_entry.get().strip()
        selected_indices = self.group_friends_listbox.curselection()
        selected_friends = [self.group_friends_listbox.get(i) for i in selected_indices]

        if not group_name:
            messagebox.showwarning("Input Error", "Group name cannot be empty!")
            return
        if not selected_friends:
            messagebox.showwarning("Selection Error", "Please select at least one friend!")
            return
        if group_name in self.groups:
            messagebox.showwarning("Duplicate Error", "A group with this name already exists!")
            return

        friends_id_list = []
        for friend in selected_friends:
            friends_id_list.append (self.friends[friend])
        status, group_id = db.create_group(self.user_id, group_name, friends_id_list)
        self.groups[group_name] = group_id
        self.groups_listbox.insert(END, f"{group_name}: {', '.join(selected_friends)}")
        self.group_name_entry.delete(0, END)

    def update_group_friends_listbox(self):
        self.group_friends_listbox.delete(0, END)
        for friend in self.friends:
            self.group_friends_listbox.insert(END, friend)





def open_dashboard(user_id):
    """Opens the Dashboard window."""
    root = Tk()
    app = FairShare(root, user_id)
    root.mainloop()

if __name__ == "__main__":
    open_dashboard("675b5efb73589439f508fdf2")
