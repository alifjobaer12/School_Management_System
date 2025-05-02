import mysql.connector
from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
from teacher_panel import teacher_panal
from admin_panel import admin_panel
from student_panal import student_panel
import threading
import time


class LoginApp:
    def __init__(self):
        self.anime_x = 320
        self.anime_y = 200
        self.anime_r_x = -302

        # MySQL Connection
        self.db = mysql.connector.connect(
            host="mysql-3aa5cf7b-islam12islam1221-3bb6.h.aivencloud.com",
            user="Pondit",
            password="AVNS_CBteuh8GdWD6fO6BrBg",
            database="alif",
            port="12492"
        )
        self.cursor = self.db.cursor()

        set_appearance_mode("light")
        set_default_color_theme("blue")

        self.window = CTk()
        self.window.geometry("700x400")
        self.window.title("School Management System")

        self.main_windo = CTkFrame(self.window, width=700, height=400, fg_color="white")
        self.main_windo.pack(fill="both", expand=True)

        self.uper_main_frame = CTkFrame(self.main_windo, width=700, height=400, fg_color="white")
        self.uper_main_frame.place(x=350, y=200, anchor="center")

        self.frame_main = CTkFrame(self.uper_main_frame, fg_color="transparent")
        self.frame_main.place(x=320, y=200, anchor="center")

        self.loading_l = CTkLabel(self.uper_main_frame, text="", font=("Harvatika", 18), height=1, width=1, fg_color="transparent")
        self.loading_l.place(x=350, y=200, anchor="center")

        self.build_login_ui()
        self.build_signup_ui()

        self.window.mainloop()

    def build_login_ui(self):
        frame_left = CTkFrame(self.frame_main, width=200, fg_color="transparent", corner_radius=0)
        frame_left.pack(side="left")

        try:
            BASE_DIR = Path(__file__).resolve().parent
            icon1_path = BASE_DIR / "image" / "login.png"
            icon1 = CTkImage(light_image=Image.open(icon1_path), size=(300, 300))
            label_img = CTkLabel(frame_left, image=icon1, text="")
            label_img.pack(padx=30, pady=(80, 55))
        except:
            CTkLabel(frame_left, text="Image\nMissing", font=CTkFont(size=20, weight="bold")).pack(expand=True)

        frame_right = CTkFrame(self.frame_main, fg_color="transparent")
        frame_right.pack(side="right", fill="both", expand=True, padx=(20, 0), pady=(70, 0), anchor="center")

        sing_in_lable = CTkLabel(frame_right, text_color="#58a2f9", text="WELCOME", font=("Helvetica", 22, "bold"))
        sing_in_lable.pack(pady=(10, 0))
        sing_in_lable1 = CTkLabel(frame_right, text_color="#9a9a9a", text="Login in to your account to continue", font=CTkFont(size=12, weight="bold"))
        sing_in_lable1.pack(pady=(0, 10))

        self.error_lable = CTkLabel(frame_right, text_color="red", width=1, height=1, text="", font=("Helvetica", 12))
        self.error_lable.place(x=110, y=75, anchor="center")

        self.entry_username = CTkEntry(frame_right, font=("Harvatika", 14), border_width=0, fg_color="transparent", placeholder_text="Username", width=200)
        self.entry_username.pack(pady=10)
        try:
            with open("remember.txt", "r") as f:
                self.entry_username.insert(0, f.read())
        except:
            pass

        self.entry_password = CTkEntry(frame_right, border_width=0, font=("Harvatika", 14), fg_color="transparent", placeholder_text="Password", show="*", width=200)
        self.entry_password.pack(pady=10)

        line1 = CTkFrame(frame_right, height=2, width=200, fg_color="gray")
        line1.place(x=110, y=110, anchor="center")
        line2 = CTkFrame(frame_right, height=2, width=200, fg_color="gray")
        line2.place(x=110, y=160, anchor="center")

        forgot_pass_bttn = CTkButton(frame_right, height=1, width=1, text="Forgot Password?", fg_color="transparent", text_color="#2a63db", hover=False)
        forgot_pass_bttn.place(x=160, y=175, anchor="center")

        btn_login = CTkButton(frame_right, text="Log in", command=self.login, width=200)
        btn_login.pack(pady=(30, 0))

        account = CTkLabel(frame_right, text="Don't have an account?", width=1, height=1, font=CTkFont(size=12))
        account.place(x=90, y=255, anchor="center")
        sign_up = CTkButton(frame_right, text="Sign up", width=1, height=1, hover=False, command=self.slide_right, fg_color="transparent", font=CTkFont(size=12), text_color="#2a63db")
        sign_up.place(x=180, y=255, anchor="center")

    def build_signup_ui(self):
        self.e_lf_frame = CTkFrame(self.uper_main_frame, width=300, height=350, fg_color="transparent")
        self.e_lf_frame.place(x=-302, y=40)

        r_lable = CTkLabel(self.e_lf_frame, text="Register", text_color="#58a2f9", font=("Helvetica", 20, "bold"), fg_color="transparent")
        r_lable.place(x=150, y=35, anchor="center")
        r_lable1 = CTkLabel(self.e_lf_frame, text="Create Your Account", text_color="#9a9a9a", font=("Helvetica", 12), fg_color="transparent")
        r_lable1.place(x=150, y=55, anchor="center")

        self.wrong_lable = CTkLabel(self.e_lf_frame, text="", fg_color="transparent", text_color="red")
        self.wrong_lable.place(x=150, y=75, anchor="center")

        self.r_username_entry = CTkEntry(self.e_lf_frame, font=("Helvetica", 14), border_width=0, corner_radius=0, placeholder_text=" Username ", width=200, fg_color="transparent")
        self.r_username_entry.place(x=150, y=105, anchor="center")
        CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=115, anchor="center")

        self.r_pass_entry = CTkEntry(self.e_lf_frame, font=("Helvetica", 14), border_width=0, corner_radius=0, placeholder_text=" Password ", width=200, fg_color="transparent")
        self.r_pass_entry.place(x=150, y=145, anchor="center")
        line1 = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a")
        line1.place(x=150, y=155, anchor="center")

        self.r_cpass_entry = CTkEntry(self.e_lf_frame, font=("Helvetica", 14), border_width=0, corner_radius=0, placeholder_text=" Conform Password ", width=200, fg_color="transparent")
        self.r_cpass_entry.place(x=150, y=185, anchor="center")
        line2 = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a")
        line2.place(x=150, y=195, anchor="center")

        self.r_vq_entry = CTkEntry(self.e_lf_frame, font=("Helvetica", 14), border_width=0, corner_radius=0, placeholder_text=" Security Question ", width=200, fg_color="transparent")
        self.r_vq_entry.place(x=150, y=225, anchor="center")
        line3 = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a")
        line3.place(x=150, y=235, anchor="center")

        self.click = IntVar(value=0)
        r_ckbox = CTkCheckBox(self.e_lf_frame, text="I read and agree to ", variable=self.click, checkbox_width=15, checkbox_height=15, fg_color="green", corner_radius=50, border_width=2, hover=False, onvalue=1, offvalue=0)
        r_ckbox.place(x=115, y=260, anchor="center")
        term_condition = CTkButton(self.e_lf_frame, width=1, height=1, text_color="blue", fg_color="transparent", text="T & C", hover=False)
        term_condition.place(x=195, y=260, anchor="center")

        r_signup_btn = CTkButton(self.e_lf_frame, command=self.slide_left, text="Sign Up")
        r_signup_btn.place(x=150, y=300, anchor="center")

    def slide_right(self):
        self.anime_x += 3
        self.anime_r_x += 3
        if self.anime_r_x <= 30 or self.anime_x <= 650:
            self.frame_main.place(x=self.anime_x, y=200, anchor="center")
            self.e_lf_frame.place(x=self.anime_r_x, y=25)
            self.window.after(1, self.slide_right)

    def slide_left(self):
        self.anime_x -= 3
        self.anime_r_x -= 3
        if self.anime_r_x >= -303 or self.anime_x >= 350:
            self.frame_main.place(x=self.anime_x, y=200, anchor="center")
            self.e_lf_frame.place(x=self.anime_r_x, y=25)
            self.window.after(1, self.slide_left)

    def slide_up(self, callback=None):
        self.loading_l.configure(text="Loading...")

        def animate():
            while self.anime_y >= -203:
                self.anime_y -= 3
                self.window.after(0, lambda: self.frame_main.place(x=320, y=self.anime_y, anchor="center"))
                time.sleep(0.002)
            if callback:
                self.window.after(0, callback)
                self.loading_l.configure(text="")

        threading.Thread(target=animate, daemon=True).start()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username and password:
            self.cursor.execute(f"SELECT password, role FROM users WHERE username='{username}';")
            user = self.cursor.fetchone()
            if user:
                stored_password, role = user
                if password == stored_password:
                    self.error_lable.configure(text="Login Successful", text_color="green")
                    self.error_lable.update()
                    time.sleep(0.7)
                    with open("remember.txt", "w") as f:
                        f.write(username)
                    self.anime_y = 200
                    if role == "admin":
                        self.slide_up(lambda: admin_panel(self.uper_main_frame, username, self.anime_y, self.frame_main, self.window))
                    elif role == "teacher":
                        self.slide_up(lambda: teacher_panal(self.uper_main_frame, username, self.anime_y, self.frame_main, self.window))
                    elif role == "student":
                        self.slide_up(lambda: student_panel(self.uper_main_frame, username, self.anime_y, self.frame_main, self.window))
                    self.error_lable.configure(text="")
                else:
                    self.error_lable.configure(text="Invalid password.", text_color="red")
                    self.error_lable.update()
            else:
                self.error_lable.configure(text="User not found.", text_color="red")
                self.error_lable.update()
        else:
            self.error_lable.configure(text="Enter username and password.", text_color="red")
            self.error_lable.update()


if __name__ == "__main__":
    LoginApp()
