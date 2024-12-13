from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import database_communication
from fare_share import FareShare  # Import the FareShare class

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
        self.bg_panel.image = photo
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

        self.name_entry = Entry(self.ign_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#666669", font=("yu gothic ui", 12, "bold"))
        self.name_entry.place(x=325, y=140, width=300)

        # Username (Mobile Number)
        self.mobile_label = Label(self.ign_frame, text="Mobile Number", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.mobile_label.place(x=325, y=190)

        self.mobile_entry = Entry(self.ign_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#666669", font=("yu gothic ui", 12, "bold"))
        self.mobile_entry.place(x=325, y=220, width=300)

        # Password
        self.password_label = Label(self.ign_frame, text="Password", bg="#040405", font=("yu gothic ui", 15, "bold"), fg="#4f4e4d")
        self.password_label.place(x=325, y=270)

        self.password_entry = Entry(self.ign_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show='*')
        self.password_entry.place(x=325, y=300, width=300)

        # Login Button
        login_button = Button(self.ign_frame, text="Login", font=("yu gothic ui", 13, "bold"), width=25, bd=0, bg="#3047ff", cursor="hand2", activebackground="#3047ff", fg="white", command=self.validate_login)
        login_button.place(x=350, y=350)

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
        root = Tk()
        FareShare(root, user_id)  # Pass user_id to FareShare class
        root.mainloop()

def page():
    """Opens the Login Page."""
    window = Tk()
    LoginForm(window)
    window.mainloop()

if __name__ == "__main__":
    page()
