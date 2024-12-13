from tkinter import *
from tkinter import messagebox
import database_communication as db

#Balance tab:
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
                key_label = Label(self.balances_tab, text=f"{key_}: ", font=("Arial", 12))
                key_label.grid(row=self.row, column=0, padx=10, pady=5, sticky="w")

                value_label = Label(self.balances_tab, text=val, font=("Arial", 12))
                value_label.grid(row=self.row, column=1, padx=10, pady=5, sticky="w")
                self.row += 1

        if status:
            groups_menu = self.groups.keys()
            self.group_selected = StringVar()
            self.group_selected.set("Select a group")
            groups_dropdown = OptionMenu(self.balances_tab, self.group_selected, *groups_menu)
            groups_dropdown.config(width=20, font=("Arial", 12))
            groups_dropdown.grid(row=self.row, column=1, padx=10, pady=5, sticky="w")
            self.row += 1
            submit_button = Button(self.balances_tab, text="Get balance of this group", font=("Arial", 14, "bold"),
                                   bg="#32a852",
                                   fg="white", width=20, height=1)
            submit_button.grid(row=self.row, column=1, padx=10, pady=5, sticky="w")
            self.row += 1

            # Event handler for submit button
            submit_button.config(command=self.group_balances)
        else:
            messagebox.showwarning("Error", "Invalid user")

    def group_balances(self):
        if self.group_selected.get() in self.groups:
            for widget in self.balances_tab.winfo_children():
                widget.destroy()
            self.row = 0
            status, group_bal_dict = db.get_balances_of_group(self.user_id, self.groups[self.group_selected.get()])
            if status:
                print(group_bal_dict)
                for member, balance in group_bal_dict.items():
                    if balance > 0:
                        msg = "You Owe " + member + " " + f"{balance:.2f}"
                        key_label = Label(self.balances_tab, text=member, font=("Arial", 12))
                        key_label.grid(row=self.row, column=0, padx=10, pady=5, sticky="w")

                        value_label = Label(self.balances_tab, text=msg, font=("Arial", 12))
                        value_label.grid(row=self.row, column=1, padx=10, pady=5, sticky="w")
                        self.row += 1
                    if balance < 0:
                        msg = member + " owes you " + f"{abs(balance):.2f}"
                        key_label = Label(self.balances_tab, text=member, font=("Arial", 12))
                        key_label.grid(row=self.row, column=0, padx=10, pady=5, sticky="w")

                        value_label = Label(self.balances_tab, text=msg, font=("Arial", 12))
                        value_label.grid(row=self.row, column=1, padx=10, pady=5, sticky="w")
                        self.row += 1
                    else:
                        msg = "You are settled up with " + member
                        key_label = Label(self.balances_tab, text=member, font=("Arial", 12))
                        key_label.grid(row=self.row, column=0, padx=10, pady=5, sticky="w")

                        value_label = Label(self.balances_tab, text=msg, font=("Arial", 12))
                        value_label.grid(row=self.row, column=1, padx=10, pady=5, sticky="w")
                        self.row += 1
            else:
                messagebox.showwarning("Error", "Invalid user")
        else:
            messagebox.showwarning("Error", "Select a group")
            return