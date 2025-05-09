from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageSequence
from pathlib import Path
from teacher_panel import teacher_panal
from admin_panel import admin_panel
from student_panal import student_panel
import threading
import time
from sql_query import MySQLQuery


class LoginApp:
    def __init__(self):
        self.anime_x = 320
        self.anime_r_x = -302
        self.anime_y = 200
        self.s = ""
        self.swich = 0

        # UI Setup
        set_appearance_mode("light")
        set_default_color_theme("blue")

        self.login_window = CTk()
        self.login_window.geometry("700x400")
        self.login_window.title("School Management System")

        self.main_windo = CTkFrame(self.login_window, width=700, height=400, fg_color="#b2fff5")
        self.main_windo.pack(fill="both", expand=True)

        self.uper_main_frame = CTkFrame(self.main_windo, width=700, height=400, fg_color="#b2fff5")
        self.uper_main_frame.place(x=350, y=200, anchor="center")

        self.frame_main = CTkFrame(self.uper_main_frame, fg_color="transparent")
        self.frame_main.place(x=320, y=200, anchor="center")

        self.loading_l = CTkLabel(self.uper_main_frame ,text="", font=("Harvatika", 18), height=1, width=1, fg_color="transparent")
        self.loading_l.place(x=350, y=200, anchor="center")

        # Add GIF beside loading label
        gif_path = Path(__file__).resolve().parent / "image" / "loading-gif.gif"
        self.gif_image = Image.open(gif_path)
        self.gif_frames = []

        # ✅ ADDED CODE: Load frames using ImageSequence
        for frame in ImageSequence.Iterator(self.gif_image):
            frame = frame.convert("RGBA").resize((30, 30))
            self.gif_frames.append(CTkImage(light_image=frame, size=(30, 30)))

        self.gif_label = CTkLabel(self.uper_main_frame, image=self.gif_frames[0], text="", fg_color="transparent")
        self.gif_label.place(x=390, y=190) 
        self.current_frame = 0
        self.animate_gif()

        self.build_ui()
        self.gif_label.place_forget()
        self.loading_l.place_forget()

        self.login_window.mainloop()

    def animate_gif(self):
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.gif_label.configure(image=self.gif_frames[self.current_frame])
        self.login_window.after(10, self.animate_gif)

    def slide_right(self):
        self.anime_x += 3
        self.anime_r_x += 3
        if self.anime_r_x <= 30 or self.anime_x <= 650:
            self.frame_main.place(x=self.anime_x, y=200, anchor="center")
            self.e_lf_frame.place(x=self.anime_r_x, y=25)
            self.login_window.after(1, self.slide_right)

    def slide_left(self):
        self.anime_x -= 3
        self.anime_r_x -= 3
        if self.anime_r_x >= -303 or self.anime_x >= 350:
            self.frame_main.place(x=self.anime_x, y=200, anchor="center")
            self.e_lf_frame.place(x=self.anime_r_x, y=25)
            self.login_window.after(1, self.slide_left)

    def slide_up(self, callback=None):
        self.loading_l.configure(text="Loading...")
        self.loading_l.place(x=380, y=200, anchor="center")
        self.gif_label.place(x=300, y=200, anchor="w")  # Positioned beside text

        def animate():
            while self.anime_y >= -203:
                self.anime_y -= 3
                self.login_window.after(0, lambda: self.frame_main.place(x=320, y=self.anime_y, anchor="center"))
                time.sleep(0.002)

            if callback:
                time.sleep(3)
                self.login_window.after(0, callback)

            self.login_window.after(0, lambda: self.loading_l.configure(text=""))
            self.login_window.after(0, self.loading_l.place_forget)
            self.login_window.after(0, self.gif_label.place_forget)

        threading.Thread(target=animate, daemon=True).start()

    def login(self, event=None):
        sql_error_l = CTkLabel(self.uper_main_frame, text_color="red", width=1, height=1, text="", font=("Helvetica",13))
        sql_error_l.place(x=350, y=30, anchor="center")
        
        def handle_login():
            try:
                sql = MySQLQuery()
            except:
                sql_error_l.configure(text="Oops! We couldn't reach the database.\nMake sure you're connected to the internet and try again.", text_color="red")
                sql_error_l.update()
                time.sleep(2)
                sql_error_l.configure(text="")
                sql_error_l.update()
                self.s = "🎉 Great! You're now connected to the database."
                self.swich = 1
                return

            if self.swich:
                sql_error_l.configure(text=self.s, text_color="#276a2b")
                sql_error_l.update()
                time.sleep(2)
                sql_error_l.configure(text="")
                sql_error_l.update()
                self.swich = 0

            username = self.entry_username.get()
            password = self.entry_password.get()

            if username and password:
                user = sql.log_in(username)
                sql.close_db()

                if user:
                    stored_password, role = user
                    if password == stored_password:
                        self.error_lable.configure(text="Login Successful", text_color="#276a2b")
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
        
        threading.Thread(target=handle_login, daemon=True).start()

    def build_ui(self):
        frame_left = CTkFrame(self.frame_main, width=200, fg_color="transparent", corner_radius=0)
        frame_left.pack(side="left")

        try:
            BASE_DIR = Path(__file__).resolve().parent
            icon1_path = BASE_DIR / "image" / "login.png"
            icon1 = CTkImage(light_image=Image.open(icon1_path), size=(315, 315))
            CTkLabel(frame_left, image=icon1, text="").pack(padx=30, pady=(80,55))
        except:
            CTkLabel(frame_left, text="Image\nMissing", font=CTkFont(size=20, weight="bold")).pack(expand=True)

        frame_right = CTkFrame(self.frame_main, fg_color="#b2fff5")
        frame_right.pack(side="right", fill="both", expand=True, padx=(20,0), pady=(87,0), anchor="center")

        CTkLabel(frame_right, text_color="#3e4d5c", text="WELCOME", font=("Helvetica",24, "bold")).pack(pady=(10,0))
        CTkLabel(frame_right, text_color="#607c84", text="Login in to your account to continue", font=("Helvetica",13, "bold")).pack(pady=(0,10))

        self.error_lable = CTkLabel(frame_right, text_color="red", width=1, height=1, text="", font=("Helvetica",12))
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

        CTkFrame(frame_right, height=2, width=200, fg_color="gray").place(x=110, y=110, anchor="center")
        CTkFrame(frame_right, height=2, width=200, fg_color="gray").place(x=110, y=160, anchor="center")

        CTkButton(frame_right, height=1, width=1, text="Forgot Password?", font=("Harvatika", 12), command=lambda: self.reg_forgatpass(0, 1), fg_color="transparent", text_color="#2a63db", hover=False).place(x=160, y=175, anchor="center")

        self.entry_password.bind("<Return>", self.login)
        CTkButton(frame_right, text="Log in", text_color="#b2fff5", fg_color="#3a506b", hover_color="#2e6f72", font=("Harvatika", 13, "bold"), command=self.login, width=200).pack(pady=(30,0))

        CTkLabel(frame_right, text="Don't have an account?", width=1, height=1, font=("Harvatika", 12)).place(x=90, y=255, anchor="center")
        CTkButton(frame_right, text="Sign up", font=("Harvatika", 12), width=1, height=1, hover=False, command=lambda: self.reg_forgatpass(1, 0), fg_color="transparent", text_color="#2a63db").place(x=180, y=255, anchor="center")

    # registration & forgate pass
    def reg_forgatpass(self, reg, fpass):
        
        if reg == 1:

            self.e_lf_frame = CTkFrame(self.uper_main_frame, width=300, height=350, fg_color="transparent")
            self.e_lf_frame.place(x=-302, y=40)

            h1_lable = CTkLabel(self.e_lf_frame, text="Register", text_color="#3e4d5c", width=1, height=1, font=("Helvetica",20,"bold"), fg_color="transparent")
            h1_lable.place(x=150, y=45, anchor="center")
            h2_lable = CTkLabel(self.e_lf_frame, text="Create Your Account", text_color="#607c84", width=1, height=1, font=("Helvetica",13, "bold"), fg_color="transparent")
            h2_lable.place(x=150, y=70, anchor="center")

            re_lable = CTkLabel(self.e_lf_frame, text="", fg_color="transparent", font=("Helvetica",12), width=1, height=1, text_color="red")
            re_lable.place(x=150, y=75, anchor="center")

            r_Username = CTkEntry(self.e_lf_frame, font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Username ", width=200, fg_color="transparent")
            r_Username.place(x=150, y=105, anchor="center")
            line = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=115, anchor="center")

            r_Password = CTkEntry(self.e_lf_frame, font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Password ", width=200, fg_color="transparent")
            r_Password.place(x=150, y=145, anchor="center")
            line = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=155, anchor="center")

            r_C_Password = CTkEntry(self.e_lf_frame, font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Conform Password ", width=200, fg_color="transparent")
            r_C_Password.place(x=150, y=185, anchor="center")
            line = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=195, anchor="center")

            r_sq = CTkEntry(self.e_lf_frame, font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Security Question ", width=200, fg_color="transparent")
            r_sq.place(x=150, y=225, anchor="center")
            line = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=235, anchor="center")

            click = IntVar(value=0)
            CTkCheckBox(self.e_lf_frame, text="I read and agree to ", variable=click, checkbox_width=15, checkbox_height=15, fg_color="#276a2b", corner_radius=50, border_width=2, hover=False, onvalue=1, offvalue=0).place(x=115, y=260, anchor="center")
            t_c = CTkButton(self.e_lf_frame, width=1, height=1, text_color="blue", fg_color="transparent", text="T & C", hover=False)
            t_c.place(x=195, y=260, anchor="center")

            signup_btn = CTkButton(self.e_lf_frame,  fg_color="#3a506b", hover_color="#2e6f72", font=("Harvatika", 12, "bold"), command=self.slide_left, text="Sign Up", text_color="#b2fff5")
            signup_btn.place(x=150, y=300, anchor="center")

            CTkLabel(self.e_lf_frame, text="Allrady have an account?", width=1, height=1, font=("Harvatika", 12)).place(x=127, y=330, anchor="center")
            CTkButton(self.e_lf_frame, text="Log in", font=("Harvatika", 12), width=1, height=1, hover=False, command=self.slide_left, fg_color="transparent", text_color="#2a63db").place(x=217, y=330, anchor="center")

        if fpass == 1:

            self.e_lf_frame = CTkFrame(self.uper_main_frame, width=300, height=350, fg_color="transparent")
            self.e_lf_frame.place(x=-302, y=40)

            h1_lable = CTkLabel(self.e_lf_frame, text="Reset Your Password", text_color="#3e4d5c", width=1, height=1, font=("Helvetica",19,"bold"), fg_color="transparent")
            h1_lable.place(x=150, y=45, anchor="center")
            h2_lable = CTkLabel(self.e_lf_frame, text="Fill All The Box", text_color="#607c84", width=1, height=1, font=("Helvetica",13, "bold"), fg_color="transparent")
            h2_lable.place(x=150, y=70, anchor="center")

            fpe_lable = CTkLabel(self.e_lf_frame, text="", fg_color="transparent", font=("Helvetica",12), width=1, height=1, text_color="red")
            fpe_lable.place(x=150, y=75, anchor="center")

            fp_Username = CTkEntry(self.e_lf_frame, font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Username ", width=200, fg_color="transparent")
            fp_Username.place(x=150, y=105, anchor="center")
            line = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=115, anchor="center")

            fp_sq = CTkEntry(self.e_lf_frame, font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Security Question ", width=200, fg_color="transparent")
            fp_sq.place(x=150, y=145, anchor="center")
            line = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=155, anchor="center")

            fp_Password = CTkEntry(self.e_lf_frame, font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text="New Password ", width=200, fg_color="transparent")
            fp_Password.place(x=150, y=185, anchor="center")
            line = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=195, anchor="center")

            fp_C_Password = CTkEntry(self.e_lf_frame, font=("Helvetica",14), border_width=0, corner_radius=0, placeholder_text=" Conform New Password ", width=200, fg_color="transparent")
            fp_C_Password.place(x=150, y=225, anchor="center")
            line = CTkFrame(self.e_lf_frame, height=2, width=200, fg_color="#9a9a9a").place(x=150, y=235, anchor="center")

            signup_btn = CTkButton(self.e_lf_frame,  fg_color="#3a506b", hover_color="#2e6f72", font=("Harvatika", 12, "bold"), command=self.slide_left, text="Reset Password", text_color="#b2fff5")
            signup_btn.place(x=150, y=285, anchor="center")

        self.slide_right()

if __name__ == "__main__":
    LoginApp()
