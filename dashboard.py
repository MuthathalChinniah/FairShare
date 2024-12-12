from tkinter import *
from PIL import ImageTk, Image
from addExpense import AddExpensePage

class Dashboard:
    def __init__(self, window):
        self.window = window
        self.window.title("Dashboard")
        self.window.geometry("800x600")
        self.window.configure(bg="white")

        # Dashboard Title
        self.title_label = Label(self.window, text="Dashboard", font=("Arial", 20, "bold"), bg="white", fg="#4d9fd1")
        self.title_label.pack(side=TOP, pady=20)

        # Add Expense Button in the center
        self.add_expense_button = Button(self.window, text="Add Expense", font=("Arial", 14, "bold"), bg="#32a852",
                                         fg="white", width=15, height=2, cursor="hand2", command=self.open_add_expense)
        self.add_expense_button.place(relx=0.5, rely=0.5, anchor=CENTER)  # Centered on the page

        # Navigation Bar
        self.nav_bar = Frame(self.window, bg="#4d9fd1", height=60)  # Use light blue as background for the navbar
        self.nav_bar.pack(side=BOTTOM, fill=X)

        # Add navigation buttons
        self.create_nav_button("Groups", "groups.gif", 0, self.open_groups)
        self.create_nav_button("Friends", "friends.gif", 1, self.open_friends)
        self.create_nav_button("Activity", "activity.gif", 2, self.open_activity)
        self.create_nav_button("Account", "account.gif", 3, self.open_account)

    def create_nav_button(self, text, icon_path, index, command):
        """Creates a button with an icon and label for the navigation bar."""
        # Load the icon image
        try:
            icon = Image.open(icon_path)  # Load icon
            icon_img = ImageTk.PhotoImage(icon.resize((30, 30)))  # Resize to 30x30
        except FileNotFoundError:
            print(f"Icon file '{icon_path}' not found.")
            return  # Skip if the file isn't found

        # Create frame for icon and label
        button_frame = Frame(self.nav_bar, bg="#4d9fd1", width=100, height=60)
        button_frame.grid(row=0, column=index, padx=20, pady=10)  # Use grid for equal distribution

        # Icon button
        icon_button = Button(button_frame, image=icon_img, bg="#4d9fd1", borderwidth=0, cursor="hand2", command=command)
        icon_button.image = icon_img  # Keep a reference to prevent garbage collection
        icon_button.pack(side=TOP, pady=2)

        # Text label
        text_label = Label(button_frame, text=text, bg="#4d9fd1", font=("Arial", 10, "bold"), fg="white")
        text_label.pack(side=TOP)

    def open_add_expense(self):
        self.window.destroy()  # Close the dashboard
        open_add_expense_page()

    def open_groups(self):
        print("Groups button clicked!")  # Replace with actual page logic
        # Add logic to navigate to the Groups page

    def open_friends(self):
        print("Friends button clicked!")  # Replace with actual page logic
        # Add logic to navigate to the Friends page

    def open_activity(self):
        print("Activity button clicked!")  # Replace with actual page logic
        # Add logic to navigate to the Activity page

    def open_account(self):
        print("Account button clicked!")  # Replace with actual page logic
        # Add logic to navigate to the Account page

def open_dashboard():
    window = Tk()
    Dashboard(window)
    window.mainloop()

def open_add_expense_page():
    window = Tk()
    AddExpensePage(window)  # Assuming AddExpensePage is your class for the Add Expense page
    window.mainloop()

if __name__ == "__main__":
    open_dashboard()
