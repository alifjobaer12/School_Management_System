import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from customtkinter import *
from pathlib import Path


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

global anime_x, anime_r_x
anime_x = 320
anime_r_x = -302

def slide_right():
    global anime_x, anime_r_x
    anime_x += 10
    anime_r_x += 10
    if anime_r_x <= 30 and anime_x <= 650:
        frame_main.place(x=anime_x, y=200, anchor="center")
        e_lf_frame.place(x=anime_r_x, y=25, )
        login_window.after(100,slide_right)

        pass


    pass

def slide_left():
    pass


# ===== LOGIN WINDOW =====
login_window = ctk.CTk()
login_window.geometry("700x400")
login_window.title("Login - School Management System")

uper_main_frame = CTkFrame(login_window, fg_color="white")
uper_main_frame.pack(fill="both", expand=True)


frame_main = ctk.CTkFrame(uper_main_frame, fg_color="transparent")
frame_main.place(x=320, y=200, anchor="center")

# LEFT PANEL (Illustration)
frame_left = ctk.CTkFrame(frame_main, width=200, fg_color="transparent", corner_radius=0)
frame_left.pack(side="right",)

try:
    BASE_DIR = Path(__file__).resolve().parent
    icon1_path = BASE_DIR / "image" / "login.png"
    icon1 = CTkImage(light_image=Image.open(icon1_path), size=(300, 300))
    label_img = ctk.CTkLabel(frame_left, image=icon1, text="")
    label_img.pack(padx=30, pady=(80,55), )
except:
    ctk.CTkLabel(frame_left, text="Image\nMissing", font=ctk.CTkFont(size=20, weight="bold")).pack(expand=True)

# RIGHT PANEL (Login Form)

e_lf_frame = CTkFrame(frame_main, width=300, height=350, fg_color="transparent")
e_lf_frame.place(x=-302, y=25, )

r_lable = CTkLabel(e_lf_frame, text="Register", text_color="#58a2f9", width=1, height=1, font=("Helvetica",20,"bold"), fg_color="transparent")
r_lable.place(x=150, y=35, anchor="center")
r_lable = CTkLabel(e_lf_frame, text="Create Your Account", text_color="#9a9a9a", width=1, height=1, font=("Helvetica",12), fg_color="transparent")
r_lable.place(x=150, y=55, anchor="center")

wrong_lable = CTkLabel(e_lf_frame, text="", fg_color="transparent", width=1, height=1, text_color="red",)
wrong_lable.place(x=150, y=75, anchor="center")

r_username_entry = CTkEntry(e_lf_frame,font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Username ", width=200, fg_color="transparent", )
r_username_entry.place(x=150, y=105, anchor="center")
line = ctk.CTkFrame(e_lf_frame, height=2, width=200, fg_color="#9a9a9a")
line.place(x=150, y=115, anchor="center")

r_pass_entry = CTkEntry(e_lf_frame,font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Password ", width=200, fg_color="transparent", )
r_pass_entry.place(x=150, y=145, anchor="center")
line = ctk.CTkFrame(e_lf_frame, height=2, width=200, fg_color="#9a9a9a")
line.place(x=150, y=155, anchor="center")

r_cpass_entry = CTkEntry(e_lf_frame,font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Conform Password ", width=200, fg_color="transparent", )
r_cpass_entry.place(x=150, y=185, anchor="center")
line = ctk.CTkFrame(e_lf_frame, height=2, width=200, fg_color="#9a9a9a")
line.place(x=150, y=195, anchor="center")

r_vq_entry = CTkEntry(e_lf_frame,font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Security Question ", width=200, fg_color="transparent", )
r_vq_entry.place(x=150, y=225, anchor="center")
line = ctk.CTkFrame(e_lf_frame, height=2, width=200, fg_color="#9a9a9a")
line.place(x=150, y=235, anchor="center")

click = IntVar(value=0)
r_ckbox = CTkCheckBox(e_lf_frame, text="I read and agree to ", variable=click, checkbox_width=15, checkbox_height=15, fg_color="green", corner_radius=50, border_width=2, hover=False, onvalue=1, offvalue=0)
r_ckbox.place(x=115, y=260, anchor="center")

term_condition = CTkButton(e_lf_frame, width=1, height=1, text_color="blue", fg_color="transparent", text="T & C", hover=False)
term_condition.place(x=195, y=260, anchor="center")

r_signup_btn = CTkButton(e_lf_frame, text="Sign Up")
r_signup_btn.place(x=150, y=300, anchor="center")


login_window.mainloop()