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
        # MySQL Connection
        self.db = mysql.connector.connect(
            host="mysql-3aa5cf7b-islam12islam1221-3bb6.h.aivencloud.com",
            user="Pondit",
            password="AVNS_CBteuh8GdWD6fO6BrBg",
            database="alif",
            port="12492"
        )
        self.cursor = self.db.cursor()

        # State variables
        self.anime_x = 320
        self.anime_r_x = -302
        self.anime_y = 200

        # Setup UI
        set_appearance_mode("light")
        set_default_color_theme("blue")

        self.login_window = CTk()
        self.login_window.geometry("700x400")
        self.login_window.title("School Management System")

        self.setup_ui()
        self.login_window.mainloop()

    def setup_ui(self):
        self.main_windo = CTkFrame(self.login_window, width=700, height=400, fg_color="white")
        self.main_windo.pack(fill="both", expand=True)

        self.uper_main_frame = CTkFrame(self.main_windo, width=700, height=400, fg_color="white")
        self.uper_main_frame.place(x=350, y=200, anchor="center")

        self.frame_main = CTkFrame(self.uper_main_frame, fg_color="transparent")
        self.frame_main.place(x=self.anime_x, y=200, anchor="center")

        self.loading_l = CTkLabel(self.uper_main_frame, text="", font=("Harvatika", 18), height=1, width=1, fg_color="transparent")
        self.loading_l.place(x=350, y=200, anchor="center")

        self.setup_left_panel()
        self.setup_right_panel()
        self.setup_register_panel()

    def setup_left_panel(self):
        self.frame_left = CTkFrame(self.frame_main, width=200, fg_color="transparent", corner_radius=0)
        self.frame_left.pack(side="left",)

        try:
            BASE_DIR = Path(__file__).resolve().parent
            icon1_path = BASE_DIR / "image" / "login.png"
            icon1 = CTkImage(light_image=Image.open(icon1_path), size=(300, 300))
            CTkLabel(self.frame_left, image=icon1, text="").pack(padx=30, pady=(80, 55))
        except:
            CTkLabel(self.frame_left, text="Image\nMissing", font=CTkFont(size=20, weight="bold")).pack(expand=True)

    def setup_right_panel(self):
        self.frame_right = CTkFrame(self.frame_main, fg_color="transparent")
        self.frame_right.pack(side="right", fill="both", expand=True, padx=(20, 0), pady=(70, 0), anchor="center")

        CTkLabel(self.frame_right, text_color="#58a2f9", text="WELCOME", font=("Helvetica", 22, "bold")).pack(pady=(10, 0))
        CTkLabel(self.frame_right, text_color="#9a9a9a", text="Login in to your account to continue",
                 font=CTkFont(size=12, weight="bold")).pack(pady=(0, 10))

        self.error_lable = CTkLabel(self.frame_right, text_color="red", width=1, height=1, text="", font=("Helvetica", 12))
        self.error_lable.place(x=110, y=75, anchor="center")

        self.entry_username = CTkEntry(self.frame_right, font=("Harvatika", 14), border_width=0,
                                       fg_color="transparent", placeholder_text="Username", width=200)
        self.entry_username.pack(pady=10)
        try:
            with open("remember.txt", "r") as f:
                self.entry_username.insert(0, f.read())
        except:
            pass

        self.entry_password = CTkEntry(self.frame_right, border_width=0, font=("Harvatika", 14), fg_color="transparent",
                                       placeholder_text="Password", show="*", width=200)
        self.entry_password.pack(pady=10)

        CTkFrame(self.frame_right, height=2, width=200, fg_color="gray").place(x=110, y=110, anchor="center")
        CTkFrame(self.frame_right, height=2, width=200, fg_color="gray").place(x=110, y=160, anchor="center")

        CTkButton(self.frame_right, height=1, width=1, text="Forgot Password?", fg_color="transparent",
                  text_color="#2a63db", hover=False).place(x=160, y=175, anchor="center")

        CTkButton(self.frame_right, text="Log in", command=self.login, width=200).pack(pady=(30, 0))

        CTkLabel(self.frame_right, text="Don't have an account?", font=CTkFont(size=12)).place(x=90, y=255, anchor="center")

        CTkButton(self.frame_right, text="Sign up", command=self.slide_right, fg_color="transparent",
                  font=CTkFont(size=12), text_color="#2a63db").place(x=180, y=255, anchor="center")

    def setup_register_panel(self):
        self.e_lf_frame = CTkFrame(self.uper_main_frame, width=300, height=350, fg_color="transparent")
        self.e_lf_frame.place(x=-302, y=40)

        CTkLabel(self.e_lf_frame, text="Register", text_color="#58a2f9", font=("Helvetica", 20, "bold")).place(x=150, y=35, anchor="center")
        CTkLabel(self.e_lf_frame, text="Create Your Account", text_color="#9a9a9a", font=("Helvetica", 12)).place(x=150, y=55, anchor="center")

        self.wrong_lable = CTkLabel(self.e_lf_frame, text="", fg_color="transparent", text_color="red")
        self.wrong_lable.place(x=150, y=75, anchor="center")

        self.r_username_entry = CTkEntry(self.e_lf_frame, placeholder_text=" Username ", width=200, fg_color="transparent")
        self.r_username_entry.place(x=150, y=105, anchor="center")
        CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=115, anchor="center")

        self.r_pass_entry = CTkEntry(self.e_lf_frame, placeholder_text=" Password ", width=200, fg_color="transparent")
        self.r_pass_entry.place(x=150, y=145, anchor="center")
        CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=155, anchor="center")

        self.r_cpass_entry = CTkEntry(self.e_lf_frame, placeholder_text=" Conform Password ", width=200, fg_color="transparent")
        self.r_cpass_entry.place(x=150, y=185, anchor="center")
        CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=195, anchor="center")

        self.r_vq_entry = CTkEntry(self.e_lf_frame, placeholder_text=" Security Question ", width=200, fg_color="transparent")
        self.r_vq_entry.place(x=150, y=225, anchor="center")
        CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=235, anchor="center")

        self.click = IntVar(value=0)
        CTkCheckBox(self.e_lf_frame, text="I read and agree to ", variable=self.click, checkbox_width=15,
                    checkbox_height=15, fg_color="green", border_width=2).place(x=115, y=260, anchor="center")

        CTkButton(self.e_lf_frame, text="T & C", fg_color="transparent", text_color="blue", hover=False).place(x=195, y=260, anchor="center")

        CTkButton(self.e_lf_frame, text="Sign Up", command=self.slide_left).place(x=150, y=300, anchor="center")

    def slide_right(self):
        def animate():
            if self.anime_r_x <= 30 or self.anime_x <= 650:
                self.anime_x += 3
                self.anime_r_x += 3
                self.frame_main.place(x=self.anime_x, y=200, anchor="center")
                self.e_lf_frame.place(x=self.anime_r_x, y=25)
                self.login_window.after(1, animate)

        animate()

    def slide_left(self):
        def animate():
            if self.anime_r_x >= -303 or self.anime_x >= 350:
                self.anime_x -= 3
                self.anime_r_x -= 3
                self.frame_main.place(x=self.anime_x, y=200, anchor="center")
                self.e_lf_frame.place(x=self.anime_r_x, y=25)
                self.login_window.after(1, animate)

        animate()

    def slide_up(self, callback=None):
        self.loading_l.configure(text="Loading...")

        def animate():
            while self.anime_y >= -203:
                self.anime_y -= 3
                self.login_window.after(0, lambda: self.frame_main.place(x=320, y=self.anime_y, anchor="center"))
                time.sleep(0.002)
            if callback:
                self.login_window.after(0, callback)
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
                        self.slide_up(lambda: admin_panel(self.uper_main_frame, username, self.anime_y, self.frame_main, self.login_window))
                    elif role == "teacher":
                        self.slide_up(lambda: teacher_panal(self.uper_main_frame, username, self.anime_y, self.frame_main, self.login_window))
                    elif role == "student":
                        self.slide_up(lambda: student_panel(self.uper_main_frame, username, self.anime_y, self.frame_main, self.login_window))
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
