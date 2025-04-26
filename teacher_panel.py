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

tec_panal_frame = CTkFrame(login_window, fg_color="sky blue", width=700, height=400)
tec_panal_frame.place(x=350, y=200, anchor="center")

tec_h_lable = CTkLabel(tec_panal_frame, text=f"Teacher\n{'Hi! '}", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",22, "bold"), )
tec_h_lable.place(x=350, y=50, anchor="center")

# logout btn
tec_logout = CTkButton(tec_panal_frame, text="⏻ Log Out", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False, )
tec_logout.place(x=640, y=50, anchor="center")
tec_logout.bind("<Enter>", lambda event: hover_on(event, "red", tec_logout))
tec_logout.bind("<Leave>", lambda event: hover_off(event, "black", tec_logout))

# student Info Frame

tec_info_view_frame = CTkFrame(tec_panal_frame, width=700, height=300, fg_color="transparent",)
tec_info_view_frame.place(x=350, y=230, anchor="center")

cursor.execute("select t_name from teacher where username='ashikuzzaman01';")
t_name = cursor.fetchone()

cursor.execute("select count(sub_name) from subjects where username='ashikuzzaman01' group by t_name;")
total_sub = cursor.fetchone()

tec_name_lable = CTkLabel(tec_info_view_frame, text_color="black", text="Name", font=("Helvetica",15, "bold"), anchor="w" )
tec_name_lable.place(x=220, y=10)
tec_tclass_lable = CTkLabel(tec_info_view_frame, text_color="black", text="Total Class", font=("Helvetica",15, "bold"), anchor="w" )
tec_tclass_lable.place(x=220, y=40)

label_colon = ctk.CTkLabel(tec_info_view_frame, text=f":     {t_name[0]}", text_color="black", font=("Helvetica",14, "bold"), anchor="w")
label_colon.place(x=320, y=10)
label_colon = ctk.CTkLabel(tec_info_view_frame, text=f":     {total_sub[0]}", text_color="black", font=("Helvetica",14, "bold"), anchor="w")
label_colon.place(x=320, y=40)

cursor.execute("SELECT sub_name, class, class_start_time, class_end_time  FROM subjects WHERE username = 'ashikuzzaman01';")
results = cursor.fetchall()

ruttin_lable = CTkLabel(tec_info_view_frame, text="Class Routine", text_color="black", width=1, height=1, fg_color="transparent", font=("Helvetica",13, "bold"))
ruttin_lable.place(x=350, y=100, anchor="center")

subject_box = CTkTextbox(tec_info_view_frame, wrap="none", activate_scrollbars=True, width=500, height=160, fg_color="transparent", scrollbar_button_color="sky blue", font=("Helvetica",13, "bold"),)
subject_box.place(x=400, y=200, anchor="center")

subject_box.delete('0.0', 'end')
header = "Subject\t\t\tClass\tStart Time\t\tEnd Time\n"
subject_box.insert('end', header)
subject_box.insert('end', "-"*100 + '\n')

for info in results:
    line = f"{info[0]}\t\t\t  {info[1]}\t {info[2]}\t\t {info[3]}\n"
    subject_box.insert('end', line)
subject_box.configure(state="disabled")



login_window.mainloop()