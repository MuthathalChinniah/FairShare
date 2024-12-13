from tkinter import *
from tkinter import messagebox
import database_communication as db
from add_expense import AddExpensePage
from balance import BalancePage
from friends import Friends
from groups import Groups

class FareShare:
    def __init__(self, root, user_id):
        if not db.user_exists(user_id):
            messagebox.showwarning("Error", "Invalid user!")
            return
        self.root = root
        self.user_id = user_id
        self.root.title("FareShare App")
        self.root.geometry("800x600")
        self.root.config(bg="#F3F4F6")

        # Initialize Friends and Groups classes
        self.friends = Friends(self.user_id)
        self.groups = Groups(self.user_id)

        # Main content frame
        self.content_frame = Frame(self.root, bg="#F3F4F6")
        self.content_frame.pack(fill="both", expand=True)

        # Bottom navigation bar
        self.bottom_nav = Frame(self.root, bg="#2C3E50", height=50)
        self.bottom_nav.pack(side="bottom", fill="x")

        self.build_navigation_buttons()
        self.create_tabs()
        self.show_friends_tab()

    def build_navigation_buttons(self):
        nav_buttons = [
            ("Friends", self.show_friends_tab, "#2ECC71"),
            ("Groups", self.show_groups_tab, "#9B59B6"),
            ("Add Expense", self.show_add_expense_tab, "#E74C3C"),
            ("Balances", self.show_balances, "#E74C3C")
        ]
        for text, command, color in nav_buttons:
            Button(self.bottom_nav, text=text, command=command, bg="#34495E", fg="white",
                   font=("Arial", 10, "bold"), activebackground=color, relief="flat").pack(side="left", expand=True, fill="both")

    def create_tabs(self):
        self.friends_tab = Frame(self.content_frame, bg="#F3F4F6")
        self.groups_tab = Frame(self.content_frame, bg="#F3F4F6")
        self.add_expense_tab = Frame(self.content_frame, bg="#F3F4F6")
        self.balances_tab = Frame(self.content_frame, bg="#F3F4F6")

    def show_friends_tab(self):
        self.switch_tab(self.friends_tab)
        self.friends.build_friends_tab(self.friends_tab)

    def show_groups_tab(self):
        self.switch_tab(self.groups_tab)
        self.groups.build_groups_tab(self.groups_tab, self.friends.get_friends())

    def show_add_expense_tab(self):
        self.switch_tab(self.add_expense_tab)
        AddExpensePage(self.add_expense_tab, self.friends.get_friends(), self.groups.get_groups())

    def show_balances(self):
        self.switch_tab(self.balances_tab)
        BalancePage(self.user_id, self.groups.get_groups(), self.balances_tab)

    def switch_tab(self, tab):
        for t in [self.friends_tab, self.groups_tab, self.add_expense_tab, self.balances_tab]:
            t.pack_forget()
        tab.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = Tk()
    app = FareShare(root, "675b5efb73589439f508fdf2")
    root.mainloop()
