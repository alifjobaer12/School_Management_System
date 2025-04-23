import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="alif60024",
    database="school_managment_system",
    port="3306"
)
cursor = db.cursor()

# CustomTkinter Setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ===== LOGIN WINDOW =====
login_window = ctk.CTk()
login_window.geometry("700x400")
login_window.title("Login - School Management System")

# ===== Helper Functions =====
def open_admin_panel():
    login_window.destroy()
    load_admin_panel()

def open_student_panel(username):
    login_window.destroy()
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

def register_student_user():
    def submit_registration():
        uname = entry_uname.get()
        pwd = entry_pwd.get()
        role = "student"
        if uname and pwd:
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (uname, pwd, role))
                db.commit()
                messagebox.showinfo("Success", "Student account created.")
                reg_window.destroy()
            except:
                messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    reg_window = ctk.CTkToplevel()
    reg_window.geometry("400x300")
    reg_window.title("Register - Student")

    ctk.CTkLabel(reg_window, text="Student Registration", font=ctk.CTkFont(size=20)).pack(pady=10)
    entry_uname = ctk.CTkEntry(reg_window, placeholder_text="Username")
    entry_uname.pack(pady=10, padx=20)
    entry_pwd = ctk.CTkEntry(reg_window, placeholder_text="Password", show="*")
    entry_pwd.pack(pady=10, padx=20)
    ctk.CTkButton(reg_window, text="Register", command=submit_registration).pack(pady=20)

def reset_password():
    def submit_reset():
        uname = entry_user.get()
        newpwd = entry_newpwd.get()
        if uname and newpwd:
            cursor.execute("UPDATE users SET password=%s WHERE username=%s", (newpwd, uname))
            db.commit()
            messagebox.showinfo("Updated", "Password reset successful.")
            reset_window.destroy()
        else:
            messagebox.showerror("Error", "Fill all fields.")

    reset_window = ctk.CTkToplevel()
    reset_window.geometry("400x250")
    reset_window.title("Reset Password")

    ctk.CTkLabel(reset_window, text="Reset Password", font=ctk.CTkFont(size=20)).pack(pady=10)
    entry_user = ctk.CTkEntry(reset_window, placeholder_text="Username")
    entry_user.pack(pady=10, padx=20)
    entry_newpwd = ctk.CTkEntry(reset_window, placeholder_text="New Password", show="*")
    entry_newpwd.pack(pady=10, padx=20)
    ctk.CTkButton(reset_window, text="Reset", command=submit_reset).pack(pady=20)

# ===== Modern Styled UI Layout =====
frame_main = ctk.CTkFrame(login_window, fg_color="#ffffff")
frame_main.pack(fill="both", expand=True)

# LEFT PANEL (Illustration)
frame_left = ctk.CTkFrame(frame_main, width=300, fg_color="#ffffff", corner_radius=0)
frame_left.pack(side="left", fill="both")

try:
    illustration = Image.open("D:\\CSE-207,208\\project\\image\\bubt.png")
    illustration = illustration.resize((260, 260), Image.ANTIALIAS)
    # print("hi")
    img = ImageTk.PhotoImage(illustration)
    label_img = ctk.CTkLabel(frame_left, image=img, text="")
    label_img.pack(pady=30)
except:
    ctk.CTkLabel(frame_left, text="Image\nMissing", font=ctk.CTkFont(size=20, weight="bold")).pack(expand=True)

# RIGHT PANEL (Login Form)
frame_right = ctk.CTkFrame(frame_main, fg_color="#ffffff")
frame_right.pack(side="right", fill="both", expand=True, padx=40, pady=30)

ctk.CTkLabel(frame_right, text="Sign in", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(10, 20))

entry_username = ctk.CTkEntry(frame_right, border_width=0, placeholder_text="Username", width=200)
entry_username.pack(pady=10)
try:
    with open("remember.txt", "r") as f:
        entry_username.insert(0, f.read())
except:
    pass

entry_password = ctk.CTkEntry(frame_right, border_width=0, placeholder_text="Password", show="*", width=200)
entry_password.pack(pady=10)

line = ctk.CTkFrame(frame_right, height=2, width=200, fg_color="transparent")
line.place(x=270, y=95, anchor="center")

line2 = ctk.CTkFrame(frame_right, height=2, width=200, fg_color="transparent")
line2.place(x=270, y=90+50, anchor="center")

btn_login = ctk.CTkButton(frame_right, text="Sign in", command=login, width=200)
btn_login.pack(pady=20)

ctk.CTkLabel(frame_right, text="Don't have an account?", font=ctk.CTkFont(size=12)).pack(pady=(5, 0))
ctk.CTkButton(frame_right, text="Sign up", command=register_student_user, width=100).pack()

ctk.CTkButton(frame_right, text="Forgot Password?", command=reset_password, fg_color="transparent", text_color="#2a63db", hover=False).pack(pady=(10, 0))

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
        try:
            line = listbox_students.get("insert linestart", "insert lineend")
            student_id = line.split(" - ")[0]
            cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
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

    cursor.execute("SELECT name, grade FROM students WHERE name=%s", (username,))
    student_data = cursor.fetchone()

    if student_data:
        name, grade = student_data
        label = ctk.CTkLabel(student_app, text=f"Welcome, {name}!\nYour Grade: {grade}", font=ctk.CTkFont(size=20))
        label.pack(pady=40)
    else:
        label = ctk.CTkLabel(student_app, text="No student record found.", font=ctk.CTkFont(size=18))
        label.pack(pady=40)

    student_app.mainloop()

# ===== Start App =====
login_window.mainloop()