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

delete = 0
fees=0

def add_std_slide_right(frame, add_std_anime_x):
    # add_std_anime_x = st
    add_std_anime_x += 6
    if add_std_anime_x <= 4*263:
        frame.place(x=add_std_anime_x, y=260, anchor="center")
        login_window.after(3,lambda:add_std_slide_right(frame, int(add_std_anime_x)))
    # else:
    #     add_std_anime_x = 4*351

def add_std_slide_left(frame, add_std_anime_x):
    # add_std_anime_x = st
    add_std_anime_x -= 6
    if add_std_anime_x >= 350:
        frame.place(x=add_std_anime_x, y=260, anchor="center")
        login_window.after(3,lambda:add_std_slide_left(frame, int(add_std_anime_x)))

def see_all_std_info():
    all_std_info = CTk()
    all_std_info.geometry("1150x900")
    all_std_info.title("All Student Info")

    all_std_textbox = CTkTextbox(all_std_info, font=("Helvetica",12))
    all_std_textbox.pack(fill="both", expand=True, side="top")

    # sql  
    all_std_sql = f"select * from students;"
    cursor.execute(all_std_sql)
    see_info = cursor.fetchall()

    all_std_textbox.delete('0.0', 'end')
    header = "ID\tUsername\t\t\tName\t\t\tClass\tRoll\tSection\tGrade\tPhone\t\t\tAddress\t\t\tTuition Fee\t\tPaid Fee\n"
    all_std_textbox.insert('end', header)
    all_std_textbox.insert('end', "-"*280 + '\n')

    for info in see_info:
        line = f"{info[0]}\t{info[1]}\t\t\t{info[2]}\t\t\t{info[3]}\t{info[4]}\t{info[5]}\t{info[6]}\t{info[7]}\t\t\t{info[8]}\t\t\t{info[9]}\t\t{info[10]}\n"
        all_std_textbox.insert('end', line)

    all_std_info.mainloop()



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
    e_s_adderss.place(x=350, y=260-50, anchor="center")
    add_placeholder()
    e_s_adderss.bind("<FocusIn>", remove_placeholder)
    e_s_adderss.bind("<FocusOut>", add_placeholder)
    e_s_grade = CTkEntry(add_std_frame,font=("Helvetica",14,),  placeholder_text=" Grade ", width=200, fg_color="transparent",)
    e_s_grade.place(x=460, y=20+100, anchor="center")
    e_s_submit_btn = CTkButton(add_std_frame, text="ADD Student", command=std_add, font=("Helvetica",14, "bold"), hover=True,)
    e_s_submit_btn.place(x=350, y=280, anchor="center")

    e_s_back_btn = CTkButton(add_std_frame, text="❌", command=add_std_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=True,)
    e_s_back_btn.place(x=670, y=20, anchor="center")

    add_std_slide_left(add_std_frame, int(4*263))
    

def std_find(admin_frame):

    def std_find_result():
        global delete, fees
        find_std_result_frame = CTkFrame(admin_frame, fg_color="transparent", width=700, height=350 )
        find_std_result_frame.place(x=4*263, y=260, anchor="center")


        # SQL

        header_lable = CTkLabel(find_std_result_frame, text="Found", fg_color="transparent", width=1, height=1, font=("Helvetica",12, "bold"),)
        header_lable.place(x=350, y=40, anchor="center")

        add_std_slide_left(find_std_result_frame, int(4*263))

        e_s_back_btn = CTkButton(find_std_result_frame, text="❌", command=find_std_result_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=True,)
        e_s_back_btn.place(x=670, y=20, anchor="center")

        if delete == 1:
            e_s_delete_btn = CTkButton(find_std_result_frame, text="Delete", command=std_add, font=("Helvetica",14, "bold"), hover=True,)
            e_s_delete_btn.place(x=350, y=280, anchor="center")

            delete = 0

        if fees == 1:
            update_fees_frame = CTkFrame(find_std_result_frame, width=200, height=200, fg_color="transparent", border_width=2, border_color="white" )
            update_fees_frame.place(x=580, y=150, anchor="center")

            f_lable = CTkLabel(update_fees_frame, text_color="black", text="Fees Update", width=1, height=1, font=("Helvetica",16, "bold"), anchor="w")
            f_lable.place(x=100, y=15+20, anchor="center")

            f_d_entry = CTkEntry(update_fees_frame, font=("Helvetica",14), placeholder_text=" Tution Fee ", fg_color="transparent",)
            f_d_entry.place(x=100, y=15+60, anchor="center")
            f_p_entry = CTkEntry(update_fees_frame, font=("Helvetica",14), placeholder_text=" Now Payed ", fg_color="transparent",)
            f_p_entry.place(x=100, y=15+100, anchor="center")

            update_btn = CTkButton(update_fees_frame, text="Update", command=std_add, font=("Helvetica",14, "bold"), hover=True,)
            update_btn.place(x=100, y=15+140, anchor="center")

            fees = 0
            pass
        
    
    find_std_frame = CTkFrame(admin_frame, fg_color="transparent", width=700, height=350 )
    find_std_frame.place(x=4*263, y=260, anchor="center")

    e_s_username = CTkEntry(find_std_frame,font=("Helvetica",14), placeholder_text=" Username ", width=200, fg_color="transparent",)
    e_s_username.place(x=350, y=100, anchor="center")

    e_s_submit_btn = CTkButton(find_std_frame, text="Find", command=std_find_result, font=("Helvetica",14, "bold"), hover=True,)
    e_s_submit_btn.place(x=350, y=180, anchor="center")

    e_s_back_btn = CTkButton(find_std_frame, text="❌", command=find_std_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=True,)
    e_s_back_btn.place(x=670, y=20, anchor="center")

    add_std_slide_left(find_std_frame, int(4*263))



def std_delete(admin_frame):
    global delete
    delete = 1
    std_find(admin_frame)


def tec_add(admin_frame):

    def add_placeholder(event=None):
        if e_s_adderss.get("1.0", "end-1c").strip() == "":
            e_s_adderss.insert("1.0", "Address")
            e_s_adderss.configure(text_color="gray")
    
    def remove_placeholder(event=None):
        if e_s_adderss.get("1.0", "end-1c").strip() == "Address":
            e_s_adderss.delete("1.0", "end")
            e_s_adderss.configure(text_color="black")

    add_tec_frame = CTkFrame(admin_frame, fg_color="transparent", width=700, height=350 )
    add_tec_frame.place(x=4*263, y=260, anchor="center")

    e_s_username = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Username ", width=200, fg_color="transparent",)
    e_s_username.place(x=240, y=20+30, anchor="center")
    e_s_name = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Name ", width=200, fg_color="transparent",)
    e_s_name.place(x=460, y=20+30, anchor="center")
    e_s_class = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Class ", width=200, fg_color="transparent",)
    e_s_class.place(x=240, y=20+65, anchor="center")
    e_s_roll = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Subject ", width=200, fg_color="transparent",)
    e_s_roll.place(x=460, y=20+65, anchor="center")
    e_s_section = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Section ", width=200, fg_color="transparent",)
    e_s_section.place(x=240, y=20+100, anchor="center")
    e_cs_section = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Class Start Time ", width=200, fg_color="transparent",)
    e_cs_section.place(x=460, y=20+100, anchor="center")
    e_es_section = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Class End Time ", width=200, fg_color="transparent",)
    e_es_section.place(x=460, y=20+135, anchor="center")
    e_s_pn = CTkEntry(add_tec_frame,font=("Helvetica",14,),  placeholder_text=" Phone Number ", width=200, fg_color="transparent",)
    e_s_pn.place(x=240, y=20+135, anchor="center")
    e_s_adderss = CTkTextbox(add_tec_frame,font=("Helvetica",14,), wrap="word", width=420, height=65, fg_color="transparent", corner_radius=6, border_width=2)
    e_s_adderss.place(x=350, y=208, anchor="center")
    add_placeholder()
    e_s_adderss.bind("<FocusIn>", remove_placeholder)
    e_s_adderss.bind("<FocusOut>", add_placeholder)

    e_t_submit_btn = CTkButton(add_tec_frame, text="ADD Teacher", command=std_add, font=("Helvetica",14, "bold"), hover=True,)
    e_t_submit_btn.place(x=350, y=280, anchor="center")

    e_s_back_btn = CTkButton(add_tec_frame, text="❌", command=add_tec_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=True,)
    e_s_back_btn.place(x=670, y=20, anchor="center")

    add_std_slide_left(add_tec_frame, int(4*263))
    

def tec_find(admin_frame):
    std_find(admin_frame)
    pass

def tec_delete(admin_frame):
    std_delete(admin_frame)
    pass


def fee_update(admin_frame):
    global fees
    fees = 1
    std_find(admin_frame)

    pass


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

find_std_btn = CTkButton(admin_frame, text="Find Student", width=1, height=1, fg_color="transparent", command=lambda:std_find(admin_frame), text_color="black", font=("Helvetica",16, "bold"), hover=False, )
find_std_btn.place(x=250, y=200, anchor="center")
find_std_btn.bind("<Enter>", lambda event: hover_on(event, "blue", find_std_btn))
find_std_btn.bind("<Leave>", lambda event: hover_off(event, "black", find_std_btn))

del_std_btn = CTkButton(admin_frame, text="Delete Student", width=1, height=1, fg_color="transparent", command=lambda:std_delete(admin_frame), text_color="black", font=("Helvetica",16, "bold"), hover=False, )
del_std_btn.place(x=250, y=250, anchor="center")
del_std_btn.bind("<Enter>", lambda event: hover_on(event, "blue", del_std_btn))
del_std_btn.bind("<Leave>", lambda event: hover_off(event, "black", del_std_btn))

add_tec_btn = CTkButton(admin_frame, text="ADD Teacher", width=1, height=1, fg_color="transparent", command=lambda:tec_add(admin_frame), text_color="black", font=("Helvetica",16, "bold"), hover=False, )
add_tec_btn.place(x=450, y=150, anchor="center")
add_tec_btn.bind("<Enter>", lambda event: hover_on(event, "blue", add_tec_btn))
add_tec_btn.bind("<Leave>", lambda event: hover_off(event, "black", add_tec_btn))

find_tec_btn = CTkButton(admin_frame, text="Find Teacher", width=1, height=1, fg_color="transparent", command=lambda:tec_find(admin_frame), text_color="black", font=("Helvetica",16, "bold"), hover=False, )
find_tec_btn.place(x=450, y=200, anchor="center")
find_tec_btn.bind("<Enter>", lambda event: hover_on(event, "blue", find_tec_btn))
find_tec_btn.bind("<Leave>", lambda event: hover_off(event, "black", find_tec_btn))

del_tec_btn = CTkButton(admin_frame, text="Delete Teacher", width=1, height=1, fg_color="transparent", command=lambda:tec_delete(admin_frame), text_color="black", font=("Helvetica",16, "bold"), hover=False, )
del_tec_btn.place(x=450, y=250, anchor="center")
del_tec_btn.bind("<Enter>", lambda event: hover_on(event, "blue", del_tec_btn))
del_tec_btn.bind("<Leave>", lambda event: hover_off(event, "black", del_tec_btn))

admin_logout = CTkButton(admin_frame, text="⏻ Log Out", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False, )
admin_logout.place(x=640, y=50, anchor="center")
admin_logout.bind("<Enter>", lambda event: hover_on(event, "red", admin_logout))
admin_logout.bind("<Leave>", lambda event: hover_off(event, "black", admin_logout))


std_fee_update = CTkButton(admin_frame, text="Update Fees", width=1, height=1, fg_color="transparent", command=lambda:fee_update(admin_frame), text_color="black", font=("Helvetica",16, "bold"), hover=False, )
std_fee_update.place(x=250, y=300, anchor="center")
std_fee_update.bind("<Enter>", lambda event: hover_on(event, "blue", std_fee_update))
std_fee_update.bind("<Leave>", lambda event: hover_off(event, "black", std_fee_update))


all_std_btn = CTkButton(admin_frame, text="See All Student Info", width=1, height=1, fg_color="transparent", command=see_all_std_info, text_color="black", font=("Helvetica",16, "bold"), hover=False, )
all_std_btn.place(x=450, y=300, anchor="center")
all_std_btn.bind("<Enter>", lambda event: hover_on(event, "blue", all_std_btn))
all_std_btn.bind("<Leave>", lambda event: hover_off(event, "black", all_std_btn))


login_window.mainloop()