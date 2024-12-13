from tkinter import *
from tkinter import messagebox
import database_communication as db

class BalancePage:
    def __init__(self, user_id, groups, balances_tab):
        self.user_id = user_id
        self.groups = groups
        self.balances_tab = balances_tab

        for widget in self.balances_tab.winfo_children():
            widget.destroy()

        status, overall_bal = db.overall_user_balance(self.user_id)
        if status:
            self.row = 0
            for key_, val in overall_bal.items():
                Label(self.balances_tab, text=f"{key_}: ", font=("Arial", 12)).grid(row=self.row, column=0, padx=10, pady=5, sticky="w")
                Label(self.balances_tab, text=val, font=("Arial", 12)).grid(row=self.row, column=1, padx=10, pady=5, sticky="w")
                self.row += 1

            self.build_group_dropdown()
        else:
            messagebox.showwarning("Error", "Unable to retrieve balances.")

    def build_group_dropdown(self):
        Label(self.balances_tab, text="Select a group:", font=("Arial", 12)).grid(row=self.row, column=0, padx=10, pady=5, sticky="w")
        self.group_selected = StringVar(value="Select Group")
        groups_dropdown = OptionMenu(self.balances_tab, self.group_selected, *self.groups.keys())
        groups_dropdown.config(width=20, font=("Arial", 12))
        groups_dropdown.grid(row=self.row, column=1, padx=10, pady=5, sticky="w")

        Button(self.balances_tab, text="Get Group Balance", command=self.group_balances, bg="#32a852", fg="white",
               font=("Arial", 10, "bold")).grid(row=self.row, column=2, padx=10, pady=5)
        self.row += 1

    def group_balances(self):
        group_name = self.group_selected.get()
        if group_name not in self.groups:
            messagebox.showwarning("Selection Error", "Please select a valid group!")
            return

        group_id = self.groups[group_name]
        status, group_bal_dict = db.get_balances_of_group(self.user_id, group_id)
        if status:
            for widget in self.balances_tab.winfo_children():
                widget.destroy()
            self.row = 0
            for member, balance in group_bal_dict.items():
                balance_msg = f"You owe {member} {balance:.2f}" if balance > 0 else f"{member} owes you {abs(balance):.2f}"
                Label(self.balances_tab, text=balance_msg, font=("Arial", 12)).grid(row=self.row, column=0, padx=10, pady=5, sticky="w")
                self.row += 1
        else:
            messagebox.showwarning("Error", "Unable to retrieve group balances.")
