import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from customtkinter import *
from pathlib import Path
import time


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

db = mysql.connector.connect(
    host="mysql-3aa5cf7b-islam12islam1221-3bb6.h.aivencloud.com",
    user="Pondit",
    password="AVNS_CBteuh8GdWD6fO6BrBg",
    database="alif",
    port="12492"
)
cursor = db.cursor()

def hover_on(event, color, btn_name):
    btn_name.configure(text_color=color)

def hover_off(event, color, btn_name):
    btn_name.configure(text_color=color)

login_window = ctk.CTk()
login_window.geometry("700x400+1200+100")
login_window.title("Login - School Management System")



#  student panal main frame

std_panal_frame = CTkFrame(login_window, fg_color="sky blue", width=800, height=400)
std_panal_frame.place(x=350, y=200, anchor="center")


# student panel header

std_lable = CTkLabel(std_panal_frame, text=f"Student\n{'Hi! '}", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",22, "bold"), )
std_lable.place(x=350, y=50, anchor="center")

# logout btn
std_logout = CTkButton(std_panal_frame, text="⏻ Log Out", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False, )
std_logout.place(x=640, y=50, anchor="center")
std_logout.bind("<Enter>", lambda event: hover_on(event, "red", std_logout))
std_logout.bind("<Leave>", lambda event: hover_off(event, "black", std_logout))


# student Info Frame

std_info_view_frame = CTkFrame(std_panal_frame, width=700, height=300, fg_color="transparent",)
std_info_view_frame.place(x=350, y=230, anchor="center")


# student Fee Info

fee_frame = CTkFrame(std_info_view_frame, width=200, height=110, fg_color="transparent", border_width=2, border_color="white" )
fee_frame.place(x=570, y=60, anchor="center")

fee_lable = ["Tution Fees", "Total Payed", "Due"]

# Fees SQL
cursor.execute("SELECT tution_fee, payed_fee, (tution_fee - payed_fee) AS remaining_fee FROM students where username = 'rafihossain275';")
fee_det = list(cursor.fetchone())

fee_h_l = CTkLabel(fee_frame, text_color="black", text="Fees", width=1, height=1, font=("Helvetica",16, "bold"), anchor="w")
fee_h_l.place(x=100, y=15, anchor="center")

for i, (f, d) in enumerate(zip(fee_lable, fee_det)):
    fee_l = CTkLabel(fee_frame, text_color="black", text=f, width=1, height=1, font=("Helvetica",14, "bold"), anchor="w")
    fee_l.place(x=50, y=45 + i * 20, anchor="center")

    fee_dettles = CTkLabel(fee_frame, text=f":  {d}", text_color="black", width=1, height=1, font=("Helvetica",14, "bold"), anchor="w")
    fee_dettles.place(x=120, y=35 + i * 20)

    if f == "Due":
        fee_l.configure(text_color="red")
        fee_dettles.configure(text_color="red")



# student Info & SQL

fields = ["Name", "Class", "Roll", "Section", "Grade", "Total Subject"]

# std info SQL
cursor.execute("select s_name, class, roll, section, grade from students where username = 'rafihossain275';")
info = list(cursor.fetchone())

for i, (a, b) in enumerate(zip(fields, info)):
    label_field = ctk.CTkLabel(std_info_view_frame, text_color="black", text=a, font=("Helvetica",14, "bold"), anchor="w")
    label_field.place(x=100, y=10 + i * 25)

    label_colon = ctk.CTkLabel(std_info_view_frame, text=f":     {b}", text_color="black", font=("Helvetica",14, "bold"), anchor="w")
    label_colon.place(x=200, y=10 + i * 25)


# class Routine & SQL

cursor.execute("SELECT sub_name, teacher_name, class_start_time, class_end_time  FROM class_subjects WHERE class = '10';")
results = cursor.fetchall()

ruttin_lable = CTkLabel(std_info_view_frame, text="Class Routine", text_color="black", width=1, height=1, fg_color="transparent", font=("Helvetica",13, "bold"))
ruttin_lable.place(x=380, y=140, anchor="center")

subject_box = CTkTextbox(std_info_view_frame, wrap="none", activate_scrollbars=True, width=600, height=160, fg_color="transparent", scrollbar_button_color="sky blue", font=("Helvetica",13, "bold"),)
subject_box.place(x=100, y=150,)

subject_box.insert(END, "Subject\t\t\tTeacher\t\t\tClass Start\t\t\tClass End\n")
subject_box.insert(END, "-"*200 + '\n')

for sub_name in results:
    subject_box.insert(END,'\t\t\t'.join(sub_name) + '\n')

login_window.mainloop()