import re
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

import database_communication  # Assuming this module exists and is implemented correctly
from login_page import LoginForm  # Assuming this module exists and is implemented correctly


class SignUpForm:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1166x718")
        self.window.state("zoomed")
        self.window.resizable(0, 0)
        self.window.config(cursor='arrow')

        # Background Image
        self.bg_frame = Image.open('images/Logo.gif')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo  # Keep a reference to prevent garbage collection
        self.bg_panel.pack(fill='both', expand='yes')

        self.signup_frame = Frame(self.window, bg="#040405", width="1000", height=600)
        self.signup_frame.place(x=200, y=50)

        # WELCOME TO FARESHARE
        self.txt = "CREATE YOUR ACCOUNT"
        self.heading = Label(self.signup_frame, text=self.txt, font=("yu gothic ui", 25, "bold"), bg="#040405", fg="white", anchor="center")
        self.heading.place(x=250, y=20, width=400)

        # Full Name
        self.name_label = Label(self.signup_frame, text="Full Name", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.name_label.place(x=400, y=90)

        self.name_entry = Entry(self.signup_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#666669", font=("yu gothic ui", 12, "bold"))
        self.name_entry.place(x=325, y=120, width=270)

        self.name_line = Canvas(self.signup_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.name_line.place(x=325, y=140)

        # Email
        self.email_label = Label(self.signup_frame, text="Email Address", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.email_label.place(x=400, y=160)

        self.email_entry = Entry(self.signup_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#666669", font=("yu gothic ui", 12, "bold"))
        self.email_entry.place(x=325, y=190, width=270)

        self.email_line = Canvas(self.signup_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.email_line.place(x=325, y=210)

        # Mobile Number
        self.mobile_label = Label(self.signup_frame, text="Mobile Number", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.mobile_label.place(x=400, y=230)

        self.mobile_entry = Entry(self.signup_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#666669", font=("yu gothic ui", 12, "bold"))
        self.mobile_entry.place(x=325, y=260, width=270)

        self.mobile_line = Canvas(self.signup_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.mobile_line.place(x=325, y=280)

        # Password
        self.password_label = Label(self.signup_frame, text="Password", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.password_label.place(x=400, y=300)

        self.password_entry = Entry(self.signup_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show='*')
        self.password_entry.place(x=325, y=330, width=270)

        self.password_line = Canvas(self.signup_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=325, y=350)

        # Confirm Password
        self.confirm_password_label = Label(self.signup_frame, text="Confirm Password", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.confirm_password_label.place(x=400, y=370)

        self.confirm_password_entry = Entry(self.signup_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show='*')
        self.confirm_password_entry.place(x=325, y=400, width=270)

        self.confirm_password_line = Canvas(self.signup_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.confirm_password_line.place(x=325, y=420)

        # Sign Up Button
        signup_button = Button(self.signup_frame, text="Sign Up", font=("yu gothic ui", 13, "bold"), width=25, bd=0, bg="#3047ff", cursor="hand2", activebackground="#3047ff", fg="white", command=self.sign_up_action)
        signup_button.place(x=350, y=470)

        # Already have an account
        self.login_label = Label(self.signup_frame, text="Already have an account?", font=("yu gothic ui", 11, "bold"), bg="#040405", fg="white")
        self.login_label.place(x=280, y=530)

        # Login Button
        login_button = Button(self.signup_frame, text="Login", font=("yu gothic ui", 11, "bold"), bg="#3047ff", fg="white", cursor="hand2", activebackground="#3047ff", bd=0, command=self.open_login_form)
        login_button.place(x=490, y=530)

    def validate_password(self, password):
        """Validate the password based on given criteria."""
        if len(password) < 8:
            return "Password must be at least 8 characters long."
        if not re.search(r"[0-9]", password):
            return "Password must contain at least one number."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>+]", password):
            return "Password must contain at least one special character."
        return None

    def validate_mobile(self, mobile):
        """
        Validate a mobile number: only numbers, 10 digits
        """
        pattern = r"\d{10}$"
        return bool(re.match(pattern, mobile))

    def validate_email(self, email):
        """
        Validate an email address.
        """
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, email))

    def sign_up_action(self):
        """Perform sign-up logic here, e.g., validate inputs and save data."""
        full_name = self.name_entry.get()
        email = self.email_entry.get()
        mobile = self.mobile_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if len(full_name) < 1:
            messagebox.showerror("Invalid Name", "Please enter a valid name")
            return

        if not self.validate_mobile(mobile):
            messagebox.showerror("Invalid Mobile", "Mobile number should be 10 digits & all numbers")
            return

        if not self.validate_email(email):
            messagebox.showerror("Invalid Email ID", "Please enter a valid email ID")
            return

        error_message = self.validate_password(password)
        if error_message:
            messagebox.showerror("Invalid Password", error_message)
            return

        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match!")
            return

        created_user, msg = database_communication.create_user_db(full_name, mobile, password, email)

        if created_user:
            messagebox.showinfo("Success", "Account created successfully!")
        else:
            messagebox.showerror("Error", msg)

    def open_login_form(self):
        """Open the login form."""
        self.window.destroy()
        login_window = Tk()
        LoginForm(login_window)
        login_window.mainloop()


# Entry point for running the application
if __name__ == "__main__":
    root = Tk()
    app = SignUpForm(root)
    root.mainloop()
