import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from customtkinter import *
from pathlib import Path
import time


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def hover_on(event, color, btn_name):
    btn_name.configure(text_color=color)

def hover_off(event, color, btn_name):
    btn_name.configure(text_color=color)


add_std_anime_x = 4*351
# add_std_anime_xe = 350
def add_std_slide_right(frame):
    global add_std_anime_x
    add_std_anime_x += 3
    if add_std_anime_x <= 4*263:
        frame.place(x=add_std_anime_x, y=260, anchor="center")
        login_window.after(3,lambda:add_std_slide_right(frame))

def add_std_slide_left(frame):
    global add_std_anime_x
    add_std_anime_x -= 3
    if add_std_anime_x >= 350:
        frame.place(x=add_std_anime_x, y=260, anchor="center")
        login_window.after(1,lambda:add_std_slide_left(frame))

def back():
    add_std_slide_right()

def std_add(admin_frame):
    def add_placeholder(event=None):
        if e_s_adderss.get("1.0", "end-1c").strip() == "":
            e_s_adderss.insert("1.0", "Address")
            e_s_adderss.configure(text_color="gray")
    
    def remove_placeholder(event=None):
        if e_s_adderss.get("1.0", "end-1c").strip() == "Address":
            e_s_adderss.delete("1.0", "end")
            e_s_adderss.configure(text_color="black")
    
    add_std_frame = CTkFrame(admin_frame, fg_color="transparent", width=700, height=350 )
    add_std_frame.place(x=4*263, y=260, anchor="center")

    e_s_username = CTkEntry(add_std_frame,font=("Helvetica",14), placeholder_text=" Username ", width=200, fg_color="transparent",)
    e_s_username.place(x=240, y=20+30, anchor="center")
    e_s_name = CTkEntry(add_std_frame,font=("Helvetica",14), placeholder_text=" Name ", width=200, fg_color="transparent",)
    e_s_name.place(x=460, y=20+30, anchor="center")
    e_s_class = CTkEntry(add_std_frame,font=("Helvetica",14), placeholder_text=" Class ", width=200, fg_color="transparent",)
    e_s_class.place(x=240, y=20+65, anchor="center")
    e_s_roll = CTkEntry(add_std_frame,font=("Helvetica",14), placeholder_text=" Roll ", width=200, fg_color="transparent",)
    e_s_roll.place(x=460, y=20+65, anchor="center")
    e_s_section = CTkEntry(add_std_frame,font=("Helvetica",14), placeholder_text=" Section ", width=200, fg_color="transparent",)
    e_s_section.place(x=240, y=20+100, anchor="center")
    e_s_pnumber = CTkEntry(add_std_frame,font=("Helvetica",14), placeholder_text=" Phone Number ", width=420, fg_color="transparent",)
    e_s_pnumber.place(x=350, y=205-50, anchor="center")
    e_s_adderss = CTkTextbox(add_std_frame,font=("Helvetica",14,), wrap="word", width=420, height=65, fg_color="transparent", corner_radius=6, border_width=2)
    add_placeholder()
    e_s_adderss.place(x=350, y=260-50, anchor="center")
    e_s_adderss.bind("<FocusIn>", remove_placeholder)
    e_s_adderss.bind("<FocusOut>", add_placeholder)
    e_s_grade = CTkEntry(add_std_frame,font=("Helvetica",14,),  placeholder_text=" Grade ", width=200, fg_color="transparent",)
    e_s_grade.place(x=460, y=20+100, anchor="center")
    e_s_submit_btn = CTkButton(add_std_frame, text="ADD Student", command=std_add, font=("Helvetica",14, "bold"), hover=True,)
    e_s_submit_btn.place(x=350, y=280, anchor="center")
    e_s_back_btn = CTkButton(admin_frame, text="◀ ", width=2, height=30, corner_radius=500, command=lambda:add_std_slide_right(add_std_frame), font=("Helvetica",24, "bold"), hover=True,)
    e_s_back_btn.place(x=30, y=20, anchor="center")

    add_std_slide_left(add_std_frame)
    


login_window = ctk.CTk()
login_window.geometry("700x400")
login_window.title("Login - School Management System")

admin_frame = CTkFrame(login_window, fg_color="sky blue", width=700, height=400)
admin_frame.place(x=350, y=200, anchor="center")

admin_lable = CTkLabel(admin_frame, text=f"Admin\n{'Hi! '}", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",22, "bold"), )
admin_lable.place(x=350, y=50, anchor="center")

add_std_btn = CTkButton(admin_frame, text="ADD Student", width=1, height=1, fg_color="transparent", command=lambda:std_add(admin_frame), text_color="black", font=("Helvetica",16, "bold"), hover=False, )
add_std_btn.place(x=250, y=150, anchor="center")
add_std_btn.bind("<Enter>", lambda event: hover_on(event, "blue", add_std_btn))
add_std_btn.bind("<Leave>", lambda event: hover_off(event, "black", add_std_btn))

find_std_btn = CTkButton(admin_frame, text="Find Student", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False, )
find_std_btn.place(x=250, y=200, anchor="center")
find_std_btn.bind("<Enter>", lambda event: hover_on(event, "blue", find_std_btn))
find_std_btn.bind("<Leave>", lambda event: hover_off(event, "black", find_std_btn))

del_std_btn = CTkButton(admin_frame, text="Delete Student", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False, )
del_std_btn.place(x=250, y=250, anchor="center")
del_std_btn.bind("<Enter>", lambda event: hover_on(event, "blue", del_std_btn))
del_std_btn.bind("<Leave>", lambda event: hover_off(event, "black", del_std_btn))

add_tec_btn = CTkButton(admin_frame, text="ADD Teacher", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False, )
add_tec_btn.place(x=450, y=150, anchor="center")
add_tec_btn.bind("<Enter>", lambda event: hover_on(event, "blue", add_tec_btn))
add_tec_btn.bind("<Leave>", lambda event: hover_off(event, "black", add_tec_btn))

find_tec_btn = CTkButton(admin_frame, text="Find Teacher", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False, )
find_tec_btn.place(x=450, y=200, anchor="center")
find_tec_btn.bind("<Enter>", lambda event: hover_on(event, "blue", find_tec_btn))
find_tec_btn.bind("<Leave>", lambda event: hover_off(event, "black", find_tec_btn))

del_tec_btn = CTkButton(admin_frame, text="Delete Teacher", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False, )
del_tec_btn.place(x=450, y=250, anchor="center")
del_tec_btn.bind("<Enter>", lambda event: hover_on(event, "blue", del_tec_btn))
del_tec_btn.bind("<Leave>", lambda event: hover_off(event, "black", del_tec_btn))

admin_logout = CTkButton(admin_frame, text="⏻ Log Out", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False, )
admin_logout.place(x=640, y=50, anchor="center")
admin_logout.bind("<Enter>", lambda event: hover_on(event, "red", admin_logout))
admin_logout.bind("<Leave>", lambda event: hover_off(event, "black", admin_logout))


e_s_back_btn = CTkButton(admin_frame, text="◀ ", width=2, height=30, corner_radius=500, font=("Helvetica",24, "bold"), hover=True,)
e_s_back_btn.place(x=30, y=20, anchor="center")

login_window.mainloop()