import tkinter as tk
import db
from login import LoginScreen, RegisterScreen
from dashboard import OfficeDashboard

class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My App Manager")
        self.root.geometry("400x450")
        
        db.initialize_db()
        
        self.current_frame = None
        self.show_login()
        
        self.root.mainloop()

    def show_login(self):
        """Ipinapakita ang Login Screen."""
        self.clear_frame()
        self.root.geometry("400x450")
        self.current_frame = LoginScreen(self.root, on_login_success=self.show_homepage, on_go_to_signup=self.show_signup)

    def show_signup(self):
        """Ipinapakita ang Sign Up Screen."""
        self.clear_frame()
        self.root.geometry("400x450")
        self.current_frame = RegisterScreen(self.root, on_go_to_login=self.show_login)

    def show_homepage(self, username, user_role):
        """Ipinapakita ang Main Dashboard."""
        self.clear_frame()
        self.current_frame = OfficeDashboard(self.root, username=username, user_role=user_role, on_logout=self.show_login)
        self.current_frame.pack(fill="both", expand=True)

    def clear_frame(self):
        """Linisin ang window bago magpalit ng screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    AppController()