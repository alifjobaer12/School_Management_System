import mysql.connector
from customtkinter import *
from tkinter import messagebox
from animasion import SlideAnimation
import time
from sql_query import MySQLQuery
from pathlib import Path
from PIL import Image
from datetime import datetime

class admin_panel:
    def __init__(self,admin_root_frame, a_username, anime_y, frame_main, login_window):
        set_appearance_mode("light")
        set_default_color_theme("blue")

        self.sql = MySQLQuery()
        self.delete = 0
        self.fees = 0
        self.username = a_username

        self.login_window = admin_root_frame
        self.anime_y = anime_y 
        self.frame_main = frame_main
        self.login_window = login_window
        self.sw = 0
        self.s = 0
        self.c = 0
        self.r = 0
        self.p = 0

        # self.login_window.geometry("700x400")
        # self.login_window.title("Login - School Management System")

        self.admin_frame = CTkFrame(self.login_window, fg_color="#C8D3Cc", width=700, height=400)
        self.admin_frame.place(x=350, y=200, anchor="center")

        self.setup_admin_ui()

        # self.login_window.mainloop()

    def hover_on(self, event, color, btn_name):
        btn_name.configure(text_color=color)

    def hover_off(self, event, color, btn_name):
        btn_name.configure(text_color=color)

    def add_std_slide_right(self, frame, add_std_anime_x):
        add_std_anime_x += 6
        if add_std_anime_x <= 4*263:
            frame.place(x=add_std_anime_x, y=260, anchor="center")
            self.login_window.after(3, lambda: self.add_std_slide_right(frame, int(add_std_anime_x)))

    def add_std_slide_left(self, frame, add_std_anime_x):
        add_std_anime_x -= 6
        if add_std_anime_x >= 350:
            frame.place(x=add_std_anime_x, y=260, anchor="center")
            self.login_window.after(3, lambda: self.add_std_slide_left(frame, int(add_std_anime_x)))

    def see_all_std_info(self):
        all_std_info = CTk()
        all_std_info.geometry("1150x900")
        all_std_info.title("All Student Info")

        all_std_textbox = CTkTextbox(all_std_info, font=("Helvetica", 12))
        all_std_textbox.pack(fill="both", expand=True, side="top")

        # sql backend
        see_info = self.sql.all_students()

        all_std_textbox.delete('0.0', 'end')
        header = "ID\tUsername\t\t\tName\t\t\tClass\tRoll\tSection\tGrade\tPhone\t\t\tAddress\t\t\tTuition Fee\t\tPaid Fee\n"
        all_std_textbox.insert('end', header)
        all_std_textbox.insert('end', "-"*280 + '\n')

        for info in see_info:
            line = f"{info[0]}\t{info[1]}\t\t\t{info[2]}\t\t\t{info[3]}\t{info[4]}\t{info[5]}\t{info[6]}\t{info[7]}\t\t\t{info[8]}\t\t\t{info[9]}\t\t{info[10]}\n"
            all_std_textbox.insert('end', line)

        all_std_textbox.configure(state="disable")

        all_std_info.mainloop()

    def see_all_tec_info(self):
        all_tec_info = CTk()
        all_tec_info.geometry("720x900")
        all_tec_info.title("All Teacher Info")

        all_tec_textbox = CTkTextbox(all_tec_info, font=("Helvetica", 12))
        all_tec_textbox.pack(fill="both", expand=True, side="top")

        # sql backend
        see_info = self.sql.all_teachers()

        all_tec_textbox.delete('0.0', 'end')
        header = "ID\tUsername\t\t\tName\t\t\tPhone\t\t\tAddress\n"
        all_tec_textbox.insert('end', header)
        all_tec_textbox.insert('end', "-"*175 + '\n')

        for info in see_info:
            line = f"{info[0]}\t{info[1]}\t\t\t{info[2]}\t\t\t{info[3]}\t\t\t{info[4]}\n"
            all_tec_textbox.insert('end', line)

        all_tec_textbox.configure(state="disable")


        all_tec_info.mainloop()

    def std_add(self):

        # take std info and add database
        def add_std(self):
            nonlocal e_s_username, e_s_name, e_s_class, e_s_roll, e_s_section, e_s_grade, e_s_pnumber, e_s_adderss, error_l

            # Retrieve all input values
            username = e_s_username.get().strip()
            name = e_s_name.get().strip()
            std_class = e_s_class.get().strip()
            roll = e_s_roll.get().strip()
            section = e_s_section.get().strip()
            grade = e_s_grade.get().strip()
            phone = e_s_pnumber.get().strip()
            address = e_s_adderss.get("1.0", "end-1c").strip()

            # Check for missing fields
            enter_fild = [e_s_username, e_s_name, e_s_class, e_s_roll, e_s_section, e_s_grade, e_s_pnumber]

            for fild in enter_fild:
                    if not fild.get().strip():
                        fild.configure(border_color="red")
                    else:
                        fild.configure(border_color="#979da2")
                    fild.update()

            if e_s_adderss.get("1.0", "end-1c").strip() == "Address":
                e_s_adderss.configure(border_color="red")
            else:
                e_s_adderss.configure(border_color="#979da2")
            e_s_adderss.update()

            if not all([username, name, std_class, roll, section, grade, phone, address]) or address == "Address":
                error_l.configure(text="⚠️ All fields are required.")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()

                return
            
            else:
                error_l.configure(text="") 
                error_l.update()

            if not (std_class.isdigit() and roll.isdigit() and phone.isdigit()):
                error_l.configure(text="⚠️ Class, Roll & Phone will be only number")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                if not std_class.isdigit():
                    e_s_class.configure(border_color="red")
                    self.c=1
                if not roll.isdigit():
                    e_s_roll.configure(border_color="red")
                    self.r=1
                if phone.isdigit():
                    e_s_pnumber.configure(border_color="red")
                    self.p=1
                return
            else:
                if self.c and self.r and self.p:
                    if self.c:
                        e_s_class.configure(border_color="green")
                        time.sleep(2)
                        e_s_class.configure(border_color="#979da2")
                        e_s_class.update()
                    if self.r:
                        e_s_roll.configure(border_color="green")
                        time.sleep(2)
                        e_s_roll.configure(border_color="#979da2")
                        e_s_roll.update()
                    if self.p:
                        e_s_pnumber.configure(border_color="green")
                        time.sleep(2)
                        e_s_pnumber.configure(border_color="#979da2")
                        e_s_pnumber.update()
            
            if not section.isalpha():
                error_l.configure(text="⚠️ Section will be only letters")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                e_s_section.configure(border_color="red")
                self.s=1
                return
            else:
                if self.s:
                    e_s_section.configure(border_color="green")
                    time.sleep(2)
                    e_s_section.configure(border_color="#979da2")
                    e_s_section.update()


            # student_info = [username, name, std_class, roll, section, grade, phone, address]

            user_info = {'username': username,
                         'pass': phone,
                         'role': "student",
                         'qna': username
            }

            student_info = {'username': username,
                            's_name': name,
                            'class': std_class,
                            'roll': roll,
                            'section': section,
                            'grade': grade,
                            'pn_number': phone,
                            'address': address,
                            'tution_fee': 0,
                            'paid_fee': 0
            }

            # sql backend
            ck_crs = self.sql.ck_class_roll_section(student_info)

            if ck_crs == False:
                error_l.configure(text="Check Class, Roll, Section", text_color="red")
                e_s_class.configure(border_color="red")
                e_s_roll.configure(border_color="red")
                e_s_section.configure(border_color="red")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                e_s_class.configure(border_color="#979da2")
                e_s_roll.configure(border_color="#979da2")
                e_s_section.configure(border_color="#979da2")
                error_l.update()
                self.sw = 1
                return
            
            if self.sw:
                e_s_class.configure(border_color="#2e7d32")
                e_s_roll.configure(border_color="#2e7d32")
                e_s_section.configure(border_color="#2e7d32")
                e_s_username.configure(border_color="#2e7d32")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                e_s_class.configure(border_color="#979da2")
                e_s_roll.configure(border_color="#979da2")
                e_s_section.configure(border_color="#979da2")
                error_l.update()
                self.sw=0
            else:
                e_s_class.configure(border_color="#979da2")
                e_s_roll.configure(border_color="#979da2")
                e_s_section.configure(border_color="#979da2")
                e_s_username.configure(border_color="#979da2")
                
            ck_u = self.sql.add_users(user_info)
            if ck_u != True:
                error_l.configure(text=ck_u, text_color="red")
                e_s_username.configure(border_color="red")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                e_s_username.configure(border_color="#979da2")
                error_l.update()
                self.sw = 1
                return

            #sql backend
            ck_s = self.sql.add_student(student_info)

            if ck_s == True and ck_u == True and ck_crs == True:
                error_l.configure(text="✔️ Student Add Successfully", text_color="#2e7d32")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()

            else:
                if ck_s != True:
                    error_l.configure(text=ck_s, text_color="red")
                elif ck_crs != True:
                    error_l.configure(text="Check Class, Roll, Section", text_color="red")
                else:
                    error_l.configure(text=ck_u, text_color="red")
                    e_s_username.configure(border_color="red")

                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                self.sw = 1
                return
            
            e_s_username.delete(0, END)
            e_s_name.delete(0, END)
            e_s_class.delete(0, END)
            e_s_roll.delete(0, END)
            e_s_section.delete(0, END)
            e_s_grade.delete(0, END)
            e_s_pnumber.delete(0, END)
            e_s_adderss.delete(1.0, END)
            add_placeholder()
            e_s_adderss.bind("<FocusIn>", remove_placeholder)
            e_s_adderss.bind("<FocusOut>", add_placeholder)


        def add_placeholder(event=None):
            if e_s_adderss.get("1.0", "end-1c").strip() == "":
                e_s_adderss.insert("1.0", "Address")
                e_s_adderss.configure(text_color="gray")

        def remove_placeholder(event=None):
            if e_s_adderss.get("1.0", "end-1c").strip() == "Address":
                e_s_adderss.delete("1.0", "end")
                e_s_adderss.configure(text_color="black")

        add_std_frame = CTkFrame(self.admin_frame, fg_color="transparent", width=700, height=350)
        add_std_frame.place(x=4*263, y=260, anchor="center")

        e_s_username = CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Username", width=200, fg_color="transparent")
        e_s_username.place(x=240, y=50, anchor="center")

        e_s_name = CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Name", width=200, fg_color="transparent")
        e_s_name.place(x=460, y=50, anchor="center")

        e_s_class = CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Class", width=200, fg_color="transparent")
        e_s_class.place(x=240, y=85, anchor="center")

        e_s_roll = CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Roll", width=200, fg_color="transparent")
        e_s_roll.place(x=460, y=85, anchor="center")

        e_s_section = CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Section", width=200, fg_color="transparent")
        e_s_section.place(x=240, y=120, anchor="center")

        e_s_grade = CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Grade", width=200, fg_color="transparent")
        e_s_grade.place(x=460, y=120, anchor="center")

        e_s_pnumber = CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Phone Number", width=420, fg_color="transparent")
        e_s_pnumber.place(x=350, y=155, anchor="center")

        e_s_adderss = CTkTextbox(add_std_frame, font=("Helvetica",14), wrap="word", width=420, height=65, fg_color="transparent", corner_radius=6, border_width=2)
        e_s_adderss.place(x=350, y=210, anchor="center")
        add_placeholder()
        e_s_adderss.bind("<FocusIn>", remove_placeholder)
        e_s_adderss.bind("<FocusOut>", add_placeholder)

        e_s_submit_btn = CTkButton(add_std_frame, text_color="#C8D3Cc", fg_color="#2c3e50", hover_color="#3e5770", text="ADD Student", command=lambda: add_std(self), font=("Helvetica",14, "bold"), hover=True)
        e_s_submit_btn.place(x=350, y=280, anchor="center")

        e_s_back_btn = CTkButton(add_std_frame, text="❌", text_color="black", fg_color="#C8D3Cc", command=add_std_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=False)
        e_s_back_btn.place(x=670, y=20, anchor="center")
        e_s_back_btn.bind("<Enter>", lambda event: self.hover_on(event, "red", e_s_back_btn))
        e_s_back_btn.bind("<Leave>", lambda event: self.hover_off(event, "black", e_s_back_btn))

        error_l = CTkLabel(self.admin_frame, text="", height=1, width=1, fg_color="transparent", text_color="red")
        error_l.place(x=350, y=100, anchor="center")

        self.add_std_slide_left(add_std_frame, int(4*263))

    def std_find(self, delete, fees, tec):

        def std_find_result(event=None):

            def updat_fee():
                # nonlocal find_s_username, header_label, show_s_f_result
            
                t_fee = f_d_entry.get()
                p_fee = f_p_entry.get()
            
                if not p_fee.strip():
                    f_p_entry.configure(border_color="red", placeholder_text_color="red")
                    f_p_entry.update()
                    return
                update_fee = self.sql.update_fees(find_s_username, t_fee, p_fee)
            
                if update_fee == True:
                    header_label.configure(text="✔️ Fees Update Successful", text_color="#2e7d32")
                    header_label.update()
            
                    #sql backend
                    updated_data = self.sql.find_student(find_s_username)
                    if updated_data:
                        tuition_fee = float(updated_data[9])
                        paid_fee = float(updated_data[10])
                        due_fee = tuition_fee - paid_fee
                        paid_fee = float(updated_data[9]) - due_fee
            
                        show_s_f_result.configure(state="normal")
                        show_s_f_result.delete("1.0", END)
                        show_s_f_result.insert(END,
                            f"ID \t\t:  {s_f_result[0]}\t\t\n"
                            f"Username \t\t:  {s_f_result[1]}\t\n"
                            f"Name \t\t:  {s_f_result[2]}\t\t\n"
                            f"Class\t\t:  {s_f_result[3]}\n"
                            f"Roll \t\t:  {s_f_result[4]}\nSection \t\t:  {s_f_result[5]}\n\n"
                            f"Tution Fee \t\t:  {s_f_result[9]}/-\nPaid Fee \t\t:  {paid_fee}/-\nDue \t\t:  {due_fee}/-"
                        )
                        show_s_f_result.configure(state="disable")
                else:
                    header_label.configure(text=update_fee, text_color="red")
                    header_label.update()

                return

            def std_del(username):

                if tec == 0:
                    #sql backend
                    ck = self.sql.delete_student(username)
                    if ck == True:
                        header_label.configure(text="✔️ Delete Student Successfull", text_color="#2e7d32")
                        header_label.update
                    else:
                        header_label.configure(text=ck, text_color="red")
                        header_label.update
                
                else:
                    #sql backend
                    ck = self.sql.delete_teacher(username)
                    if ck == True:
                        header_label.configure(text="✔️ Delete Teacher Successfull", text_color="#2e7d32")
                        header_label.update
                    else:
                        header_label.configure(text=ck, text_color="red")
                        header_label.update

            find_std_result_frame = CTkFrame(self.admin_frame, fg_color="transparent", width=700, height=350)
            find_std_result_frame.place(x=4*263, y=200, anchor="center")


            header_label = CTkLabel(find_std_result_frame, text="", text_color="#2e7d32", fg_color="transparent", width=1, height=1, font=("Helvetica",14, "bold"))
            header_label.place(x=350, y=25, anchor="center")

            show_s_f_result = CTkTextbox(find_std_result_frame, wrap="none", activate_scrollbars=True, scrollbar_button_color="#C8D3Cc", fg_color="transparent", width=540, height=220, font=("Helvetica",16, "bold"))             # change sky blue to fg color
            show_s_f_result.place(x=350, y=160, anchor="center")

            find_s_username = e_s_username.get()

            if find_s_username == "":
                e_s_username.configure(placeholder_text_color="red", border_color="red")
                return
            else:
                e_s_username.configure(placeholder_text_color="light_color", border_color="#979da2")
            
            # sql backend
            if tec == 1:
                #sql backend
                s_f_result = self.sql.find_teacher(find_s_username)

                if s_f_result is not None:
                    header_label.configure(text="✔️ Found", text_color="#2e7d32")
                    header_label.update

                    show_s_f_result.insert(END,
                        f"ID \t\t:  {s_f_result[0]}\n\nUsername \t\t:  {s_f_result[1]}\n\n"
                        f"Name \t\t:  {s_f_result[2]}\n\nPhone Number \t\t:  {s_f_result[3]}\n\n"
                        f"Address \t\t:  {s_f_result[4]}\n"
                    )
                    show_s_f_result.configure(state="disable")

                else:
                    header_label.configure(text="❌ Not Found", text_color="red")
                    header_label.update


            else:
                #sql backend
                s_f_result = self.sql.find_student(find_s_username)

                if s_f_result is not None:
                    header_label.configure(text="✔️ Found", text_color="#2e7d32")
                    header_label.update

                    tuition_fee = float(s_f_result[9])
                    paid_fee = float(s_f_result[10])
                    due_fee = tuition_fee - paid_fee

                    if fees == 0:
                        show_s_f_result.insert(END,
                            f"ID \t\t:  {s_f_result[0]}\t\tTution Fee \t\t:  {s_f_result[9]}/-\n"
                            f"Username \t\t:  {s_f_result[1]}\t\tPaid Fee \t\t:  {s_f_result[10]}/-\n"
                            f"Name \t\t:  {s_f_result[2]}\t\tDue \t\t:  {due_fee}/-\n"
                            f"Class\t\t:  {s_f_result[3]}\n"
                            f"Roll \t\t:  {s_f_result[4]}\nSection \t\t:  {s_f_result[5]}\n"
                            f"Grade \t\t:  {s_f_result[6]}\nPhone Number \t\t:  {s_f_result[7]}\n"
                            f"Address \t\t:  {s_f_result[8]}\n"
                        )
                    else:
                        show_s_f_result.insert(END,
                            f"ID \t\t:  {s_f_result[0]}\t\t\n"
                            f"Username \t\t:  {s_f_result[1]}\t\n"
                            f"Name \t\t:  {s_f_result[2]}\t\t\n"
                            f"Class\t\t:  {s_f_result[3]}\n"
                            f"Roll \t\t:  {s_f_result[4]}\nSection \t\t:  {s_f_result[5]}\n\n"
                            f"Tution Fee \t\t:  {s_f_result[9]}/-\nPaid Fee \t\t:  {s_f_result[10]}/-\nDue \t\t:  {due_fee}/-"
                        )

                    show_s_f_result.configure(state="disable")

                else:
                    header_label.configure(text="❌ Not Found", text_color="red")
                    header_label.update



            self.add_std_slide_left(find_std_result_frame, int(4*263))

            e_s_back_btn = CTkButton(find_std_result_frame, text="❌", text_color="black", fg_color="#C8D3Cc", command=find_std_result_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=False)
            e_s_back_btn.place(x=670, y=20, anchor="center")
            e_s_back_btn.bind("<Enter>", lambda event: self.hover_on(event, "red", e_s_back_btn))
            e_s_back_btn.bind("<Leave>", lambda event: self.hover_off(event, "black", e_s_back_btn))

            if delete == 1:

                e_s_delete_btn = CTkButton(find_std_result_frame, text_color="#C8D3Cc", fg_color="#2c3e50", hover_color="#3e5770", text="🗑 Delete", command=lambda: std_del(find_s_username), font=("Helvetica",14, "bold"), hover=True)
                e_s_delete_btn.place(x=350, y=280, anchor="center")

            if fees == 1:
                
                show_s_f_result.configure(width=300, )
                show_s_f_result.place(x=250, y=160, anchor="center")

                update_fees_frame = CTkFrame(find_std_result_frame, width=200, height=200, fg_color="transparent", border_width=2, border_color="white")
                update_fees_frame.place(x=580, y=150, anchor="center")

                f_label = CTkLabel(update_fees_frame, text="Fees Update", text_color="black", font=("Helvetica",16, "bold"))
                f_label.place(x=100, y=35, anchor="center")

                f_d_entry = CTkEntry(update_fees_frame, font=("Helvetica",14), placeholder_text="Tuition Fee", fg_color="transparent")
                f_d_entry.place(x=100, y=75, anchor="center")

                f_p_entry = CTkEntry(update_fees_frame, font=("Helvetica",14), placeholder_text="Now Payed", fg_color="transparent")
                f_p_entry.place(x=100, y=115, anchor="center")

                update_btn = CTkButton(update_fees_frame, text_color="#C8D3Cc", fg_color="#2c3e50", hover_color="#3e5770", text="Update", command=lambda: updat_fee(), font=("Helvetica",14, "bold"), hover=True)
                update_btn.place(x=100, y=155, anchor="center")
                # self.fees = 0


        find_std_frame = CTkFrame(self.admin_frame, fg_color="transparent", width=700, height=350)
        find_std_frame.place(x=4*263, y=260, anchor="center")

        e_s_username = CTkEntry(find_std_frame, font=("Helvetica",14), placeholder_text="Username", width=200, fg_color="transparent")
        e_s_username.place(x=350, y=100, anchor="center")

        
        # print(find_s_username)
        e_s_username.bind("<Return>", std_find_result)
        e_s_submit_btn = CTkButton(find_std_frame, text_color="#C8D3Cc", fg_color="#2c3e50", hover_color="#3e5770", text="🔍 Find", command= lambda: std_find_result(), font=("Helvetica",14, "bold"),  hover=True)
        e_s_submit_btn.place(x=350, y=180, anchor="center")

        e_s_back_btn = CTkButton(find_std_frame, text="❌", text_color="black", fg_color="#C8D3Cc", command=find_std_frame.destroy, width=1, height=1, corner_radius=500, font=("Helvetica",14, "bold"), hover=False)
        e_s_back_btn.place(x=670, y=20, anchor="center")
        e_s_back_btn.bind("<Enter>", lambda event: self.hover_on(event, "red", e_s_back_btn))
        e_s_back_btn.bind("<Leave>", lambda event: self.hover_off(event, "black", e_s_back_btn))

        self.add_std_slide_left(find_std_frame, int(4*263))

    def std_delete(self, delete, fees, tec):
        self.std_find(delete, fees, tec)

    def tec_add(self):

        # take std info and add database
        def add_tec():
            nonlocal e_s_username, e_s_name, e_s_class, e_s_sub, e_s_section, e_s_pn, e_s_adderss, error_l, e_ce_time, e_cs_time

            # Retrieve all input values
            username = e_s_username.get().strip()
            name = e_s_name.get().strip()
            std_class = e_s_class.get().strip()
            sub = e_s_sub.get().strip()
            section = e_s_section.get().strip()
            phone = e_s_pn.get().strip()
            class_st = e_cs_time.get().strip()
            class_et = e_ce_time.get().strip()
            address = e_s_adderss.get("1.0", "end-1c").strip()

            # Check for missing fields

            enter_fild = [e_s_username, e_s_name, e_s_class, e_s_sub, e_s_section, e_s_pn, e_ce_time, e_cs_time]

            for fild in enter_fild:
                    if not fild.get().strip():
                        fild.configure(border_color="red")
                    else:
                        fild.configure(border_color="#979da2")
                    fild.update()

            if e_s_adderss.get("1.0", "end-1c").strip() == "Address":
                e_s_adderss.configure(border_color="red")
            else:
                e_s_adderss.configure(border_color="#979da2")
            e_s_adderss.update()

            if not all([username, name, std_class, sub, section, phone, class_et, class_st]) or address == "Address":
                error_l.configure(text="⚠️ All fields are required.")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                return
            else:
                error_l.configure(text="") 
                error_l.update()

            if not std_class.isdigit():
                error_l.configure(text="⚠️ Class will be only number")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                e_s_class.configure(border_color="red")
                self.s=1
                return
            else:
                if self.s:
                    e_s_class.configure(border_color="green")
                    time.sleep(2)
                    e_s_class.configure(border_color="#979da2")
                    e_s_class.update()
                
            if not (sub.isalpha() and section.isalpha()):
                error_l.configure(text="⚠️ Section & Subject Name will be string with only letters")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                if not sub.isalpha():
                    e_s_sub.configure(border_color="red")
                    self.c=1
                if not section.isalpha():
                    e_s_section.configure(border_color="red")
                    self.r=1
                return
            else:
                if self.c and self.r:
                    if self.c:
                        e_s_sub.configure(border_color="green")
                        time.sleep(2)
                        e_s_sub.configure(border_color="#979da2")
                        e_s_sub.update()
                    if self.r:
                        e_s_section.configure(border_color="green")
                        time.sleep(2)
                        e_s_section.configure(border_color="#979da2")
                        e_s_section.update()
            
            try:
                start_t = datetime.strptime(class_st, "%H:%M").time()
                end_t = datetime.strptime(class_et, "%H:%M").time()
                if start_t == end_t:
                    error_l.configure(text="⚠️ Class Start and End time not be same", text_color="red")
                    error_l.update()
                    time.sleep(2)
                    error_l.configure(text="")
                    error_l.update()
                    return
            except ValueError:
                error_l.configure(text="⚠️ Time must be in HH:MM format", text_color="red")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                return

            sub_info = { 'subject': sub,
                        'username': username,
                        'name': name,
                        'class': std_class,
                        'start_t': start_t,
                        'end_t':end_t,
                        'section': section
            }

            teacher_info = {'username': username,
                            'name': name,
                            'phone': phone,
                            'address': address
            }

            user_info = {'username': username,
                         'pass': phone,
                         'role': "teacher",
                         'qna': username
            }

            # sql backend
            ck_crs = self.sql.ck_tec_class_sub_section(sub_info)
            if not ck_crs:
                error_l.configure(text="Check Subject, Class, Section, Class Start & End time", text_color="red")
                e_s_class.configure(border_color="red")
                e_s_sub.configure(border_color="red")
                e_s_section.configure(border_color="red")
                e_cs_time.configure(border_color="red")
                e_ce_time.configure(border_color="red")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                self.sw = 1
                return
            
            if self.sw:
                e_s_class.configure(border_color="#2e7d32")
                e_s_sub.configure(border_color="#2e7d32")
                e_s_section.configure(border_color="#2e7d32")
                e_cs_time.configure(border_color="#2e7d32")
                e_ce_time.configure(border_color="#2e7d32")
                e_s_username.configure(border_color="#2e7d32")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                e_s_class.configure(border_color="#979da2")
                e_s_sub.configure(border_color="#979da2")
                e_s_section.configure(border_color="#979da2")
                e_cs_time.configure(border_color="#979da2")
                e_ce_time.configure(border_color="#979da2")
                error_l.update()
                self.sw=0
            else:
                e_s_class.configure(border_color="#979da2")
                e_s_sub.configure(border_color="#979da2")
                e_s_section.configure(border_color="#979da2")
                e_cs_time.configure(border_color="#979da2")
                e_ce_time.configure(border_color="#979da2")
                e_s_username.configure(border_color="#979da2")
            
            ck_u = self.sql.add_users(user_info)
            if ck_u != True:
                error_l.configure(text=ck_u, text_color="red")
                e_s_username.configure(border_color="red")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                e_s_username.configure(border_color="#979da2")
                error_l.update()
                self.sw = 1
                return
            
            #sql backend
            ck_t = self.sql.add_teacher(teacher_info)
            ck_s = self.sql.add_subject(sub_info)

            if (ck_t == True) and (ck_s == True) and (ck_u == True):
                error_l.configure(text="✔️ Teacher Add Successfully", text_color="#2e7d32")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()

            else:
                if ck_u != True:
                    error_l.configure(text=ck_u, text_color="red")
                elif ck_t != True:
                    error_l.configure(text=ck_t, text_color="red")
                else:
                    error_l.configure(text="Check Subject, Class, Section, Class Start & End time", text_color="red")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()

            e_s_username.delete(0, END)
            e_s_name.delete(0, END)
            e_s_class.delete(0, END)
            e_s_sub.delete(0, END)
            e_s_section.delete(0, END)
            e_s_pn.delete(0, END)
            e_cs_time.delete(0, END)
            e_ce_time.delete(0, END)
            e_s_adderss.delete(1.0, END)
            add_placeholder()
            e_s_adderss.bind("<FocusIn>", remove_placeholder)
            e_s_adderss.bind("<FocusOut>", add_placeholder)

        def add_placeholder(event=None):
            if e_s_adderss.get("1.0", "end-1c").strip() == "":
                e_s_adderss.insert("1.0", "Address")
                e_s_adderss.configure(text_color="gray")

        def remove_placeholder(event=None):
            if e_s_adderss.get("1.0", "end-1c").strip() == "Address":
                e_s_adderss.delete("1.0", "end")
                e_s_adderss.configure(text_color="black")

        add_tec_frame = CTkFrame(self.admin_frame, fg_color="transparent", width=700, height=350 )
        add_tec_frame.place(x=4*263, y=260, anchor="center")

        e_s_username = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Username ", width=200, fg_color="transparent",)
        e_s_username.place(x=240, y=20+30, anchor="center")
        e_s_name = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Name ", width=200, fg_color="transparent",)
        e_s_name.place(x=460, y=20+30, anchor="center")
        e_s_class = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Class ", width=200, fg_color="transparent",)
        e_s_class.place(x=240, y=20+65, anchor="center")
        e_s_sub = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Subject ", width=200, fg_color="transparent",)
        e_s_sub.place(x=460, y=20+65, anchor="center")
        e_s_section = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Section ", width=200, fg_color="transparent",)
        e_s_section.place(x=240, y=20+100, anchor="center")
        e_cs_time = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Class Start Time ", width=200, fg_color="transparent",)
        e_cs_time.place(x=460, y=20+100, anchor="center")
        e_ce_time = CTkEntry(add_tec_frame,font=("Helvetica",14), placeholder_text=" Class End Time ", width=200, fg_color="transparent",)
        e_ce_time.place(x=460, y=20+135, anchor="center")
        e_s_pn = CTkEntry(add_tec_frame,font=("Helvetica",14,),  placeholder_text=" Phone Number ", width=200, fg_color="transparent",)
        e_s_pn.place(x=240, y=20+135, anchor="center")
        e_s_adderss = CTkTextbox(add_tec_frame,font=("Helvetica",14,), wrap="word", width=420, height=65, fg_color="transparent", corner_radius=6, border_width=2)
        e_s_adderss.place(x=350, y=208, anchor="center")
        add_placeholder()
        e_s_adderss.bind("<FocusIn>", remove_placeholder)
        e_s_adderss.bind("<FocusOut>", add_placeholder)

        e_t_submit_btn = CTkButton(add_tec_frame, text_color="#C8D3Cc", fg_color="#2c3e50", hover_color="#3e5770", text="ADD Teacher", command= add_tec , font=("Helvetica",14, "bold"), hover=True,)
        e_t_submit_btn.place(x=350, y=280, anchor="center")

        e_s_back_btn = CTkButton(add_tec_frame, text="❌", text_color="black", fg_color="#C8D3Cc", command=add_tec_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=False,)
        e_s_back_btn.place(x=670, y=20, anchor="center")
        e_s_back_btn.bind("<Enter>", lambda event: self.hover_on(event, "red", e_s_back_btn))
        e_s_back_btn.bind("<Leave>", lambda event: self.hover_off(event, "black", e_s_back_btn))

        error_l = CTkLabel(self.admin_frame, text="", height=1, width=1, fg_color="transparent", text_color="red")
        error_l.place(x=350, y=100, anchor="center")

        self.add_std_slide_left(add_tec_frame, int(4*263))
    

    def tec_find(self, delete, fees, tec):
        self.std_find(delete, fees, tec)

    def tec_delete(self, delete, fees, tec):
        self.std_delete(delete, fees, tec)

    def fee_update(self, delete, fees, tec):

        self.std_find(delete, fees, tec)

    def subject_asign(self):
        query = self.sql

        def asign_sub(self):
            nonlocal query, t_sa_username, t_sa_name, t_sa_class, t_sa_section, error_l, t_sa_subject, t_sa_Class_et, t_sa_Class_st

            # Retrieve all input values
            username = t_sa_username.get().strip()
            name = query.teacher_info(username)
            # t_sa_name.configure(text = name[0])
            if name == False:
                return
            std_class = t_sa_class.get().strip()
            section = t_sa_section.get().strip()
            subject = t_sa_subject.get().strip() 
            Class_st = t_sa_Class_st.get().strip() 
            Class_et = t_sa_Class_et.get().strip() 

            enter_fild = [t_sa_username, t_sa_class, t_sa_section, t_sa_subject, t_sa_Class_et, t_sa_Class_st]

            for fild in enter_fild:
                    if not fild.get().strip():
                        fild.configure(border_color="red")
                    else:
                        fild.configure(border_color="#979da2")
                    fild.update()

            # Check for missing fields
            if not all([username, std_class, section,  subject, Class_et, Class_st]):
                error_l.configure(text="⚠️ All fields are required.")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                return
            
            else:
                error_l.configure(text="") 
                error_l.update()

            if not std_class.isdigit():
                error_l.configure(text="⚠️ Class will be only number")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                t_sa_class.configure(border_color="red")
                self.s=1
                return
            else:
                if self.s:
                    t_sa_class.configure(border_color="green")
                    time.sleep(2)
                    t_sa_class.configure(border_color="#979da2")
                    t_sa_class.update()

            if not (subject.isalpha() and section.isalpha()):
                error_l.configure(text="⚠️ Section & Subject Name will be string with only letters")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                if not subject.isalpha():
                    t_sa_subject.configure(border_color="red")
                    self.c=1
                if not section.isalpha():
                    t_sa_section.configure(border_color="red")
                    self.r=1
                return
            else:
                if self.c and self.r:
                    if self.c:
                        t_sa_subject.configure(border_color="green")
                        time.sleep(2)
                        t_sa_subject.configure(border_color="#979da2")
                        t_sa_subject.update()
                    if self.r:
                        t_sa_section.configure(border_color="green")
                        time.sleep(2)
                        t_sa_section.configure(border_color="#979da2")
                        t_sa_section.update()

            try:
                start_t = datetime.strptime(Class_st, "%H:%M").time()
                end_t = datetime.strptime(Class_et, "%H:%M").time()
                if start_t == end_t:
                    error_l.configure(text="⚠️ Class Start and End time not be same", text_color="red")
                    error_l.update()
                    time.sleep(2)
                    error_l.configure(text="")
                    error_l.update()
                    return

            except ValueError:
                error_l.configure(text="⚠️ Time must be in HH:MM format", text_color="red")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                return


            sub_info = { 'subject': subject,
                        'username': username,
                        'name': name[0],
                        'class': std_class,
                        'start_t': start_t,
                        'end_t': end_t,
                        'section': section
            }

            #sql backend
            ck = query.add_subject(sub_info)

            if ck:
                error_l.configure(text="✔️ Subject Asign Successfully", text_color="#2e7d32")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
            else:
                error_l.configure(text="❌ Subject Asign Faild", text_color="red")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()

            t_sa_username.delete(0, END)
            t_sa_name.configure(text="Name")
            t_sa_class.delete(0, END)
            t_sa_section.delete(0, END)
            t_sa_subject.delete(0, END)
            t_sa_Class_st.delete(0, END)
            t_sa_Class_et.delete(0, END)


        def find_user(self,  event=None):
            nonlocal t_sa_username, t_sa_name, error_l, query

            username = t_sa_username.get().strip()
            name = query.teacher_info(username)
            if name == False or name is None:
                t_sa_name.configure(text_color="red", text="Not Found")
                error_l.configure(text="Teacher Not Found", text_color="red")
                t_sa_username.configure(border_color="red")
                error_l.update()
                time.sleep(2)
                error_l.configure(text="")
                error_l.update()
                return
            if name is not False and name is not None:
                t_sa_name.configure(text_color="green", text=name[0])
                t_sa_username.configure(border_color="green")


        subject_asign_frame = CTkFrame(self.admin_frame, fg_color="transparent", width=700, height=350)
        subject_asign_frame.place(x=4*263, y=260, anchor="center")

        t_sa_username = CTkEntry(subject_asign_frame, font=("Helvetica",14), placeholder_text="Username", width=200, fg_color="transparent")
        t_sa_username.place(x=240, y=50, anchor="center")
        t_sa_username.bind("<KeyRelease>",find_user)

        name_frame = CTkFrame(subject_asign_frame, width=200, height=30, fg_color="transparent", border_width=2, border_color="#979da2")
        name_frame.place(x=460, y=50, anchor="center")

        t_sa_name = CTkLabel(subject_asign_frame, font=("Helvetica",14), text="Name", text_color="#858585", width=1, height=1, fg_color="transparent",)
        t_sa_name.place(x=370, y=41)
        

        t_sa_class = CTkEntry(subject_asign_frame, font=("Helvetica",14), placeholder_text="Class", width=200, fg_color="transparent")
        t_sa_class.place(x=240, y=100, anchor="center")

        # t_sa_roll = CTkEntry(subject_asign_frame, font=("Helvetica",14), placeholder_text="Roll", width=200, fg_color="transparent")
        # t_sa_roll.place(x=460, y=85, anchor="center")

        t_sa_section = CTkEntry(subject_asign_frame, font=("Helvetica",14), placeholder_text="Section", width=200, fg_color="transparent")
        t_sa_section.place(x=240, y=150, anchor="center")

        t_sa_Class_st = CTkEntry(subject_asign_frame, font=("Helvetica",14), placeholder_text="Class Start Time", width=200, fg_color="transparent")
        t_sa_Class_st.place(x=460, y=150, anchor="center")

        t_sa_Class_et = CTkEntry(subject_asign_frame, font=("Helvetica",14), placeholder_text="Class End Time", width=200, fg_color="transparent")
        t_sa_Class_et.place(x=460, y=200, anchor="center")

        t_sa_subject = CTkEntry(subject_asign_frame, font=("Helvetica",14), placeholder_text="Subject", width=200, fg_color="transparent")
        t_sa_subject.place(x=240, y=200, anchor="center")

        t_sa_submit_btn = CTkButton(subject_asign_frame, text_color="#C8D3Cc", fg_color="#2c3e50", hover_color="#3e5770", text="Submit", command=lambda: asign_sub(self), font=("Helvetica",14, "bold"), hover=True)
        t_sa_submit_btn.place(x=350, y=280, anchor="center")

        t_sa_back_btn = CTkButton(subject_asign_frame, text="❌", text_color="black", fg_color="#C8D3Cc", command=subject_asign_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=False)
        t_sa_back_btn.place(x=670, y=20, anchor="center")
        t_sa_back_btn.bind("<Enter>", lambda event: self.hover_on(event, "red", t_sa_back_btn))
        t_sa_back_btn.bind("<Leave>", lambda event: self.hover_off(event, "black", t_sa_back_btn))

        error_l = CTkLabel(self.admin_frame, text="", height=1, width=1, fg_color="transparent", text_color="red")
        error_l.place(x=350, y=100, anchor="center")

        self.add_std_slide_left(subject_asign_frame, int(4*263))
        

    def setup_admin_ui(self):
        admin_label = CTkLabel(self.admin_frame, text=f"Admin\nHi! {self.username}", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",22, "bold"))
        admin_label.place(x=350, y=50, anchor="center")

        BASE_DIR = Path(__file__).resolve().parent
        ICON_DIR = BASE_DIR / "image"

        # Load icons using pathlib paths
        def load_icon(filename):
            return CTkImage(Image.open(ICON_DIR / filename), size=(30, 30))

        # Define icons
        self.icons = {
            "add_student": load_icon("add_student.png"),
            "find_student": load_icon("find_student.png"),
            "delete_student": load_icon("delete_student.png"),
            "see_student": load_icon("all_students.png"),
            "add_teacher": load_icon("add_teacher.png"),
            "find_teacher": load_icon("find_teacher.png"),
            "delete_teacher": load_icon("teacher_delete.png"),
            "see_teacher": load_icon("all_teacher.png"),
            "update_fees": load_icon("fees_update.png"),
            "subject_assign": load_icon("subject_asign.png"),
        }

        # Button data
        buttons = [
            ("ADD Student", self.std_add, 150, 130, "add_student"),
            ("Find Student", lambda: self.std_find(0, 0, 0), 265, 130, "find_student"),
            ("Delete Student", lambda: self.std_delete(1, 0, 0), 395, 130, "delete_student"),
            ("See All Student Info", self.see_all_std_info, 220, 290, "see_student"),
            ("ADD Teacher", self.tec_add, 150, 210, "add_teacher"),
            ("Find Teacher", lambda: self.tec_find(0, 0, 1), 265, 210, "find_teacher"),
            ("Delete Teacher", lambda: self.tec_delete(1, 0, 1), 395, 210, "delete_teacher"),
            ("See All Teacher Info", self.see_all_tec_info, 420, 290, "see_teacher"),
            ("Update Fees", lambda: self.fee_update(0, 1, 0), 520, 130, "update_fees"),
            ("Subject Assign", self.subject_asign, 520, 210, "subject_assign"),
        ]

        for text, command, x, y, icon_key in buttons:
            btn = CTkButton(
                self.admin_frame,
                text=text,
                image=self.icons[icon_key],
                compound="top",
                width=11,
                height=1,
                fg_color="#C8D3Cc",
                command=command,
                text_color="black",
                font=("Helvetica", 14, "bold"),
                hover_color="#e0e0e0",
                hover=False,
            )
            btn.place(x=x+17, y=y+25, anchor="center")
            btn.bind("<Enter>", lambda e, b=btn: self.hover_on(e, "blue", b))
            btn.bind("<Leave>", lambda e, b=btn: self.hover_off(e, "black", b))

        admin_logout = CTkButton(self.admin_frame, text="⏻ Log Out", command=lambda:self.logout(self.admin_frame), width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False)
        admin_logout.place(x=640, y=50, anchor="center")
        admin_logout.bind("<Enter>", lambda event: self.hover_on(event, "red", admin_logout))
        admin_logout.bind("<Leave>", lambda event: self.hover_off(event, "black", admin_logout))

    def logout(self, log_out_f):
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to logout?")
        if confirm:
            animation = SlideAnimation(self.anime_y, self.frame_main, self.login_window)
            animation.slide_down()
            log_out_f.destroy()
            self.sql.close_db()
