import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ===== LOGIN WINDOW =====
login_window = ctk.CTk()
login_window.geometry("700x400")
login_window.title("Login - School Management System")


login_window.mainloop()