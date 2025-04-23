import mysql.connector
import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path


# MySQL Connection
db = mysql.connector.connect(
    host="mysql-3aa5cf7b-islam12islam1221-3bb6.h.aivencloud.com",
    user="avnadmin",
    password="AVNS_75SJDnpTc2SZB7hG5bX",
    database="school",
    port="12492"
)
cursor = db.cursor()


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
    username = entry_username.get()
    password = entry_password.get()
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
                    open_admin_panel()
                elif role == "student":
                    open_student_panel(username)
            else:
                messagebox.showerror("Error", "Invalid password.")
        else:
            messagebox.showerror("Error", "User not found.")
    else:
        messagebox.showerror("Error", "Enter username and password.")


# CustomTkinter Setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ===== LOGIN WINDOW =====
login_window = ctk.CTk()
login_window.geometry("700x400")
login_window.title("School Management System")

uper_main_frame = CTkFrame(login_window, fg_color="white")
uper_main_frame.pack(fill="both", expand=True)

frame_main = ctk.CTkFrame(uper_main_frame, fg_color="transparent")
frame_main.pack(fill="both", expand=True)

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
frame_right.pack(side="right", fill="both", expand=True, pady=(50,0), anchor="center")

sing_in_lable = ctk.CTkLabel(frame_right, text_color="#58a2f9", text="WELCOME", font=ctk.CTkFont(size=22, weight="bold"))
sing_in_lable.pack(pady=(10,0))

sing_in_lable1 = ctk.CTkLabel(frame_right, text_color="#9a9a9a", text="Login in to your account to continue", font=ctk.CTkFont(size=12, weight="bold"))
sing_in_lable1.pack(pady=(0,10))

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
line.place(x=170, y=110, anchor="center")

line2 = ctk.CTkFrame(frame_right, height=2, width=200, fg_color="gray")
line2.place(x=170, y=110+50, anchor="center")

forgot_pass_bttn = ctk.CTkButton(frame_right, height=1, width=1, text="Forgot Password?", fg_color="transparent", text_color="#2a63db", hover=False)
forgot_pass_bttn.place(x=220, y=175, anchor="center")


btn_login = ctk.CTkButton(frame_right, text="Sign in", command=login, width=200)
btn_login.pack(pady=(30,0))

account = ctk.CTkLabel(frame_right, text="Don't have an account?", width=1, height=1, font=ctk.CTkFont(size=12))
account.place(x=142, y=255, anchor="center")

sign_up = ctk.CTkButton(frame_right, text="Sign up", width=1, height=1, hover=False, fg_color="transparent", font=ctk.CTkFont(size=12), text_color="#2a63db",)
sign_up.place(x=237, y=255, anchor="center")


login_window.mainloop()