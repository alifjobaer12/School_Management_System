import mysql.connector
import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
from teacher_panel import teacher_panal
from admin_panel import admin_panel
from test import student_panel
from animasion import SlideAnimation


import time


# MySQL Connection
db = mysql.connector.connect(
    host="mysql-3aa5cf7b-islam12islam1221-3bb6.h.aivencloud.com",
    user="Pondit",
    password="AVNS_CBteuh8GdWD6fO6BrBg",
    database="alif",
    port="12492"
)
cursor = db.cursor()


global anime_x, anime_r_x
anime_x = 320
anime_y = 200
anime_r_x = -302

def slide_right():
    global anime_x, anime_r_x
    anime_x += 3
    anime_r_x += 3
    if anime_r_x <= 30 or anime_x <= 650:
        frame_main.place(x=anime_x, y=200, anchor="center")
        e_lf_frame.place(x=anime_r_x, y=25, )
        login_window.after(1,slide_right)

def slide_left():
    global anime_x, anime_r_x
    anime_x -= 3
    anime_r_x -= 3
    if anime_r_x >= -303 or anime_x >= 350:
        frame_main.place(x=anime_x, y=200, anchor="center")
        e_lf_frame.place(x=anime_r_x, y=25, )
        login_window.after(1,slide_left)


def slide_up(callback=None):
    loading_lable = CTkLabel(uper_main_frame, text="Loading...", width=1, height=1, fg_color="transparent")
    loading_lable.place(x=350, y=200, anchor="center")
    global anime_y
    anime_y -= 3
    if anime_y >= -203:
        # loading_lable.pack_forget()
        frame_main.place(x=320, y=anime_y, anchor="center")
        login_window.after(2,lambda: slide_up(callback))
    else:
        if callback:
            callback()





# ===== Admin Panel =====
def load_admin_panel():
    admin_app = ctk.CTk()
    admin_app.geometry("600x400")
    admin_app.title("Admin Panel - School Management")

    def register_student():
        name = entry_name.get()
        grade = entry_grade.get()
        if name and grade:
            cursor.execute("INSERT INTO students (name, grade) VALUES (%s, %s)", (name, grade))
            db.commit()
            messagebox.showinfo("Success", "Student registered successfully.")
            entry_name.delete(0, 'end')
            entry_grade.delete(0, 'end')
            load_students()
        else:
            messagebox.showerror("Error", "All fields are required.")

    def load_students():
        listbox_students.delete("0.0", "end")
        cursor.execute("SELECT * FROM students")
        for row in cursor.fetchall():
            listbox_students.insert("end", f"{row[0]} - {row[1]} (Grade: {row[2]})\n")

    def delete_student():
        # global entry_name
        try:
            line = listbox_students.get("insert linestart", "insert lineend")
            student_id = line.split(" - ")[0]
            user_name = entry_name.get()
            cursor.execute(f"DELETE FROM students WHERE name ='{user_name}';")
            db.commit()
            load_students()
            messagebox.showinfo("Deleted", "Student removed.")
        except:
            messagebox.showerror("Error", "Select a student to delete.")

    frame = ctk.CTkFrame(admin_app)
    frame.pack(pady=20, padx=20, fill="x")

    entry_name = ctk.CTkEntry(frame, placeholder_text="Student Name")
    entry_name.pack(pady=5, padx=10, fill="x")

    entry_grade = ctk.CTkEntry(frame, placeholder_text="Grade")
    entry_grade.pack(pady=5, padx=10, fill="x")

    btn_register = ctk.CTkButton(frame, text="Register Student", command=register_student)
    btn_register.pack(pady=10)

    listbox_students = ctk.CTkTextbox(admin_app, width=500, height=150)
    listbox_students.pack(pady=10)

    btn_delete = ctk.CTkButton(admin_app, text="Delete Selected", command=delete_student)
    btn_delete.pack()

    load_students()
    admin_app.mainloop()

# ===== Student Panel =====
def load_student_panel(username):
    student_app = ctk.CTk()
    student_app.geometry("400x200")
    student_app.title(f"{username}'s Dashboard")

    cursor.execute("SELECT name, grade FROM students WHERE name='%s'", (username,))
    student_data = cursor.fetchone()

    if student_data:
        name, grade = student_data
        label = ctk.CTkLabel(student_app, text=f"Welcome, {name}!\nYour Grade: {grade}", font=ctk.CTkFont(size=20))
        label.pack(pady=40)
    else:
        label = ctk.CTkLabel(student_app, text="No student record found.", font=ctk.CTkFont(size=18))
        label.pack(pady=40)

    student_app.mainloop()



def open_admin_panel():
    # login_window.destroy()
    load_admin_panel()

def open_student_panel(username):
    # login_window.destroy()
    load_student_panel(username)


def login():
    global error_lable, login_window, anime_y, frame_main
    username = entry_username.get()
    password = entry_password.get()
    # animasion = SlideAnimation(anime_y, frame_main, login_window)
    # print(username, " ", password)

    if username and password:
        cursor.execute(f"SELECT password, role FROM users WHERE username='{username}';")
        user = cursor.fetchone()
        if user:
            stored_password, role = user
            if password == stored_password:
                with open("remember.txt", "w") as f:
                    f.write(username)
                if role == "admin":
                    slide_up(lambda: admin_panel(uper_main_frame, username, anime_y, frame_main, login_window))
                elif role == "teacher":
                    slide_up(lambda: teacher_panal(uper_main_frame, username, anime_y, frame_main, login_window))
                    # teacher_panal(uper_main_frame, username, anime_y, frame_main, login_window)
                elif role == "student":
                    slide_up(lambda: student_panel(uper_main_frame, username, anime_y, frame_main, login_window))
            else:
                error_lable.configure(text="Invalid password.")
                # messagebox.showerror("Error", "Invalid password.")
        else:
            error_lable.configure(text="User not found.")
            # messagebox.showerror("Error", "User not found.")
    else:
        error_lable.configure(text="Enter username and password.")
        # messagebox.showerror("Error", "Enter username and password.")


# CustomTkinter Setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ===== LOGIN WINDOW =====
login_window = ctk.CTk()
login_window.geometry("700x400")
login_window.title("School Management System")

main_windo = CTkFrame(login_window, width=700, height=400, fg_color="white")
main_windo.pack(fill="both", expand=True)

uper_main_frame = CTkFrame(main_windo, width=700, height=400, fg_color="white")
uper_main_frame.place(x=350, y=200, anchor="center")

frame_main = ctk.CTkFrame(uper_main_frame, fg_color="transparent")
frame_main.place(x=320, y=200, anchor="center")

# LEFT PANEL (Illustration)
frame_left = ctk.CTkFrame(frame_main, width=200, fg_color="transparent", corner_radius=0)
frame_left.pack(side="left",)

try:
    BASE_DIR = Path(__file__).resolve().parent
    icon1_path = BASE_DIR / "image" / "login.png"
    icon1 = CTkImage(light_image=Image.open(icon1_path), size=(300, 300))
    label_img = ctk.CTkLabel(frame_left, image=icon1, text="")
    label_img.pack(padx=30, pady=(80,55), )
except:
    ctk.CTkLabel(frame_left, text="Image\nMissing", font=ctk.CTkFont(size=20, weight="bold")).pack(expand=True)

# RIGHT PANEL (Login Form)
frame_right = ctk.CTkFrame(frame_main, fg_color="transparent")
frame_right.pack(side="right", fill="both", expand=True, padx=(20,0), pady=(70,0), anchor="center")

sing_in_lable = CTkLabel(frame_right, text_color="#58a2f9", text="WELCOME", font=("Helvetica",22, "bold"),)
sing_in_lable.pack(pady=(10,0))

sing_in_lable1 = ctk.CTkLabel(frame_right, text_color="#9a9a9a", text="Login in to your account to continue", font=ctk.CTkFont(size=12, weight="bold"))
sing_in_lable1.pack(pady=(0,10))

error_lable = CTkLabel(frame_right, text_color="red", width=1, height=1, text="", font=("Helvetica",12),)
error_lable.place(x=110, y=72, anchor="center")

entry_username = ctk.CTkEntry(frame_right, font=("Harvatika", 14), border_width=0, fg_color="transparent", placeholder_text="Username", width=200)
entry_username.pack(pady=10)
try:
    with open("remember.txt", "r") as f:
        entry_username.insert(0, f.read())
except:
    pass

entry_password = ctk.CTkEntry(frame_right, border_width=0,font=("Harvatika", 14), fg_color="transparent", placeholder_text="Password", show="*", width=200)
entry_password.pack(pady=10)

line = ctk.CTkFrame(frame_right, height=2, width=200, fg_color="gray")
line.place(x=110, y=110, anchor="center")

line2 = ctk.CTkFrame(frame_right, height=2, width=200, fg_color="gray")
line2.place(x=110, y=110+50, anchor="center")

forgot_pass_bttn = ctk.CTkButton(frame_right, height=1, width=1, text="Forgot Password?", fg_color="transparent", text_color="#2a63db", hover=False)
forgot_pass_bttn.place(x=160, y=175, anchor="center")


btn_login = ctk.CTkButton(frame_right, text="Log in", command=login, width=200)
btn_login.pack(pady=(30,0))

account = ctk.CTkLabel(frame_right, text="Don't have an account?", width=1, height=1, font=ctk.CTkFont(size=12))
account.place(x=90, y=255, anchor="center")

sign_up = ctk.CTkButton(frame_right, text="Sign up", width=1, height=1, hover=False, command=slide_right, fg_color="transparent", font=ctk.CTkFont(size=12), text_color="#2a63db",)
sign_up.place(x=180, y=255, anchor="center")


e_lf_frame = CTkFrame(uper_main_frame, width=300, height=350, fg_color="transparent")
e_lf_frame.place(x=-302, y=40, )

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

r_signup_btn = CTkButton(e_lf_frame, command=slide_left, text="Sign Up")
r_signup_btn.place(x=150, y=300, anchor="center")


login_window.mainloop()