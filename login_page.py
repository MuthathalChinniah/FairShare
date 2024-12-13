from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import database_communication
from Main_Dashboard import open_dashboard

class LoginForm:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1166x718")
        self.window.state("zoomed")
        self.window.resizable(0, 0)
        self.window.config(cursor='arrow')

        # Background Image
        self.bg_frame = Image.open('Logo.gif')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo  # Keep a reference to prevent garbage collection
        self.bg_panel.pack(fill='both', expand='yes')

        self.ign_frame = Frame(self.window, bg="#040405", width="1000", height=550)
        self.ign_frame.place(x=200, y=70)

        # WELCOME TO FARESHARE
        self.txt = "WELCOME TO FARESHARE"
        self.heading = Label(self.ign_frame, text=self.txt, font=("yu gothic ui", 25, "bold"), bg="#040405", fg="white", anchor="center")
        self.heading.place(x=250, y=20, width=400)

        # SIGN IN
        self.sign_in_label = Label(self.ign_frame, text="Sign In", bg="#040405", fg="white", font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=400, y=80)

        # Name
        self.name_label = Label(self.ign_frame, text="Name", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.name_label.place(x=325, y=110)

        self.name_entry = Entry(self.ign_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#666669", font=("yu gothic ui", 12, "bold"))
        self.name_entry.place(x=325, y=140, width=270)

        self.name_line = Canvas(self.ign_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.name_line.place(x=325, y=160)

        # Username (Mobile Number)
        self.mobile_label = Label(self.ign_frame, text="Mobile Number", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.mobile_label.place(x=325, y=190)

        self.mobile_entry = Entry(self.ign_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#666669", font=("yu gothic ui", 12, "bold"))
        self.mobile_entry.place(x=325, y=220, width=270)

        self.mobile_line = Canvas(self.ign_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.mobile_line.place(x=325, y=240)

        # Password
        self.password_label = Label(self.ign_frame, text="Password", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.password_label.place(x=325, y=270)

        self.password_entry = Entry(self.ign_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show='*')
        self.password_entry.place(x=325, y=300, width=270)

        self.password_line = Canvas(self.ign_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=325, y=320)

        # Login Button
        login_button = Button(self.ign_frame, text="Login", font=("yu gothic ui", 13, "bold"), width=25, bd=0, bg="#3047ff", cursor="hand2", activebackground="#3047ff", fg="white", command=self.validate_login)
        login_button.place(x=350, y=350)

        # Forgot Password
        self.forgot_button = Button(self.ign_frame, text="Forgot Password?", font=("yu gothic ui", 13, "bold underline"), fg="white", width=25, bd=0, bg="#040405", activebackground="#040405", cursor="hand2")
        self.forgot_button.place(x=350, y=385)

        # No account yet label
        self.sign_label = Label(self.ign_frame, text="Don't have an account yet?", font=("yu gothic ui", 11, "bold"), bg="#040405", fg="white")
        self.sign_label.place(x=280, y=450)

        # Sign Up Button
        signup_button = Button(self.ign_frame, text="Sign Up", font=("yu gothic ui", 11, "bold"), bg="#3047ff", fg="white", cursor="hand2", activebackground="#3047ff", bd=0, command=self.open_sign_up_form)
        signup_button.place(x=490, y=450)

    def validate_login(self):
        """Validate Login Credentials and Navigate to Dashboard."""
        mobile_number = self.mobile_entry.get()
        password = self.password_entry.get()

        # Replace with actual user verification logic
        valid_login, msg = database_communication.login(mobile_number, password)

        if valid_login:
            messagebox.showinfo("Login Successful", "Welcome to the Dashboard!")
            self.open_dashboard(msg)
        else:
            messagebox.showerror("Login Failed", msg)

    def open_dashboard(self, user_id):
        """Open the Dashboard Page."""
        self.window.destroy()  # Close the login page
        open_dashboard(user_id)

    def open_sign_up_form(self):
        """Open the Sign-Up Form."""
        self.window.destroy()
        sign_up_page()

def sign_up_page():
    """Opens the Sign-Up Page."""
    from signup_page import SignUpForm
    window = Tk()
    SignUpForm(window)
    window.mainloop()

def page():
    """Opens the Login Page."""
    window = Tk()
    LoginForm(window)
    window.mainloop()

if __name__ == "__main__":
    page()
