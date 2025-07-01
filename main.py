import customtkinter as ctk
from ui.app_ui import XPFileSearchApp

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # mimic XP style
    ctk.set_default_color_theme("blue")  # Windows XP blueish color

    app = XPFileSearchApp()
    app.mainloop()
