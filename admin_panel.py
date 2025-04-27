import mysql.connector
import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import time
from animasion import SlideAnimation


class admin_panel:
    def __init__(self,admin_root_frame, a_username, anime_y, frame_main, login_window):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.db = mysql.connector.connect(
            host="mysql-3aa5cf7b-islam12islam1221-3bb6.h.aivencloud.com",
            user="Pondit",
            password="AVNS_CBteuh8GdWD6fO6BrBg",
            database="alif",
            port=12492
        )
        self.cursor = self.db.cursor()
        self.delete = 0
        self.fees = 0

        self.login_window = admin_root_frame
        self.anime_y = anime_y 
        self.frame_main = frame_main
        self.login_window = login_window

        # self.login_window.geometry("700x400")
        # self.login_window.title("Login - School Management System")

        self.admin_frame = ctk.CTkFrame(self.login_window, fg_color="sky blue", width=700, height=400)
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
        all_std_info = ctk.CTk()
        all_std_info.geometry("1150x900")
        all_std_info.title("All Student Info")

        all_std_textbox = ctk.CTkTextbox(all_std_info, font=("Helvetica", 12))
        all_std_textbox.pack(fill="both", expand=True, side="top")

        all_std_sql = "SELECT * FROM students;"
        self.cursor.execute(all_std_sql)
        see_info = self.cursor.fetchall()

        all_std_textbox.delete('0.0', 'end')
        header = "ID\tUsername\t\t\tName\t\t\tClass\tRoll\tSection\tGrade\tPhone\t\t\tAddress\t\t\tTuition Fee\t\tPaid Fee\n"
        all_std_textbox.insert('end', header)
        all_std_textbox.insert('end', "-"*280 + '\n')

        for info in see_info:
            line = f"{info[0]}\t{info[1]}\t\t\t{info[2]}\t\t\t{info[3]}\t{info[4]}\t{info[5]}\t{info[6]}\t{info[7]}\t\t\t{info[8]}\t\t\t{info[9]}\t\t{info[10]}\n"
            all_std_textbox.insert('end', line)

        all_std_info.mainloop()

    def std_add(self):
        def add_placeholder(event=None):
            if e_s_adderss.get("1.0", "end-1c").strip() == "":
                e_s_adderss.insert("1.0", "Address")
                e_s_adderss.configure(text_color="gray")

        def remove_placeholder(event=None):
            if e_s_adderss.get("1.0", "end-1c").strip() == "Address":
                e_s_adderss.delete("1.0", "end")
                e_s_adderss.configure(text_color="black")

        add_std_frame = ctk.CTkFrame(self.admin_frame, fg_color="transparent", width=700, height=350)
        add_std_frame.place(x=4*263, y=260, anchor="center")

        e_s_username = ctk.CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Username", width=200, fg_color="transparent")
        e_s_username.place(x=240, y=50, anchor="center")

        e_s_name = ctk.CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Name", width=200, fg_color="transparent")
        e_s_name.place(x=460, y=50, anchor="center")

        e_s_class = ctk.CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Class", width=200, fg_color="transparent")
        e_s_class.place(x=240, y=85, anchor="center")

        e_s_roll = ctk.CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Roll", width=200, fg_color="transparent")
        e_s_roll.place(x=460, y=85, anchor="center")

        e_s_section = ctk.CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Section", width=200, fg_color="transparent")
        e_s_section.place(x=240, y=120, anchor="center")

        e_s_grade = ctk.CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Grade", width=200, fg_color="transparent")
        e_s_grade.place(x=460, y=120, anchor="center")

        e_s_pnumber = ctk.CTkEntry(add_std_frame, font=("Helvetica",14), placeholder_text="Phone Number", width=420, fg_color="transparent")
        e_s_pnumber.place(x=350, y=155, anchor="center")

        e_s_adderss = ctk.CTkTextbox(add_std_frame, font=("Helvetica",14), wrap="word", width=420, height=65, fg_color="transparent", corner_radius=6, border_width=2)
        e_s_adderss.place(x=350, y=210, anchor="center")
        add_placeholder()
        e_s_adderss.bind("<FocusIn>", remove_placeholder)
        e_s_adderss.bind("<FocusOut>", add_placeholder)

        e_s_submit_btn = ctk.CTkButton(add_std_frame, text="ADD Student", command=self.std_add, font=("Helvetica",14, "bold"), hover=True)
        e_s_submit_btn.place(x=350, y=280, anchor="center")

        e_s_back_btn = ctk.CTkButton(add_std_frame, text="❌", command=add_std_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=True)
        e_s_back_btn.place(x=670, y=20, anchor="center")

        self.add_std_slide_left(add_std_frame, int(4*263))

    def std_find(self):
        def std_find_result():
            find_std_result_frame = ctk.CTkFrame(self.admin_frame, fg_color="transparent", width=700, height=350)
            find_std_result_frame.place(x=4*263, y=260, anchor="center")

            header_label = ctk.CTkLabel(find_std_result_frame, text="Found", fg_color="transparent", width=1, height=1, font=("Helvetica",12, "bold"))
            header_label.place(x=350, y=40, anchor="center")

            self.add_std_slide_left(find_std_result_frame, int(4*263))

            e_s_back_btn = ctk.CTkButton(find_std_result_frame, text="❌", command=find_std_result_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=True)
            e_s_back_btn.place(x=670, y=20, anchor="center")

            if self.delete == 1:
                e_s_delete_btn = ctk.CTkButton(find_std_result_frame, text="Delete", command=self.std_add, font=("Helvetica",14, "bold"), hover=True)
                e_s_delete_btn.place(x=350, y=280, anchor="center")
                self.delete = 0

            if self.fees == 1:
                update_fees_frame = ctk.CTkFrame(find_std_result_frame, width=200, height=200, fg_color="transparent", border_width=2, border_color="white")
                update_fees_frame.place(x=580, y=150, anchor="center")

                f_label = ctk.CTkLabel(update_fees_frame, text="Fees Update", text_color="black", font=("Helvetica",16, "bold"))
                f_label.place(x=100, y=35, anchor="center")

                f_d_entry = ctk.CTkEntry(update_fees_frame, font=("Helvetica",14), placeholder_text="Tuition Fee", fg_color="transparent")
                f_d_entry.place(x=100, y=75, anchor="center")

                f_p_entry = ctk.CTkEntry(update_fees_frame, font=("Helvetica",14), placeholder_text="Now Payed", fg_color="transparent")
                f_p_entry.place(x=100, y=115, anchor="center")

                update_btn = ctk.CTkButton(update_fees_frame, text="Update", command=self.std_add, font=("Helvetica",14, "bold"), hover=True)
                update_btn.place(x=100, y=155, anchor="center")
                self.fees = 0

        find_std_frame = ctk.CTkFrame(self.admin_frame, fg_color="transparent", width=700, height=350)
        find_std_frame.place(x=4*263, y=260, anchor="center")

        e_s_username = ctk.CTkEntry(find_std_frame, font=("Helvetica",14), placeholder_text="Username", width=200, fg_color="transparent")
        e_s_username.place(x=350, y=100, anchor="center")

        e_s_submit_btn = ctk.CTkButton(find_std_frame, text="Find", command=std_find_result, font=("Helvetica",14, "bold"), hover=True)
        e_s_submit_btn.place(x=350, y=180, anchor="center")

        e_s_back_btn = ctk.CTkButton(find_std_frame, text="❌", command=find_std_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=True)
        e_s_back_btn.place(x=670, y=20, anchor="center")

        self.add_std_slide_left(find_std_frame, int(4*263))

    def std_delete(self):
        self.delete = 1
        self.std_find()

    def tec_add(self):
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

        e_t_submit_btn = CTkButton(add_tec_frame, text="ADD Teacher", command=self.std_add, font=("Helvetica",14, "bold"), hover=True,)
        e_t_submit_btn.place(x=350, y=280, anchor="center")

        e_s_back_btn = CTkButton(add_tec_frame, text="❌", command=add_tec_frame.destroy, width=2, height=30, corner_radius=500, font=("Helvetica",14, "bold"), hover=True,)
        e_s_back_btn.place(x=670, y=20, anchor="center")

        self.add_std_slide_left(add_tec_frame, int(4*263))
    

    def tec_find(self):
        self.std_find()

    def tec_delete(self):
        self.std_delete()

    def fee_update(self):
        self.fees = 1
        self.std_find()

    def setup_admin_ui(self):
        admin_label = ctk.CTkLabel(self.admin_frame, text="Admin\nHi!", width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",22, "bold"))
        admin_label.place(x=350, y=50, anchor="center")

        buttons = [
            ("ADD Student", self.std_add, 250, 150),
            ("Find Student", self.std_find, 250, 200),
            ("Delete Student", self.std_delete, 250, 250),
            ("Update Fees", self.fee_update, 250, 300),
            ("ADD Teacher", self.tec_add, 450, 150),
            ("Find Teacher", self.tec_find, 450, 200),
            ("Delete Teacher", self.tec_delete, 450, 250),
            ("See All Student Info", self.see_all_std_info, 450, 300),
        ]

        for text, command, x, y in buttons:
            btn = ctk.CTkButton(self.admin_frame, text=text, width=1, height=1, fg_color="transparent", command=command, text_color="black", font=("Helvetica",16, "bold"), hover=False)
            btn.place(x=x, y=y, anchor="center")
            btn.bind("<Enter>", lambda e, b=btn: self.hover_on(e, "blue", b))
            btn.bind("<Leave>", lambda e, b=btn: self.hover_off(e, "black", b))

        admin_logout = ctk.CTkButton(self.admin_frame, text="⏻ Log Out", command=lambda:self.logout(self.admin_frame), width=1, height=1, fg_color="transparent", text_color="black", font=("Helvetica",16, "bold"), hover=False)
        admin_logout.place(x=640, y=50, anchor="center")
        admin_logout.bind("<Enter>", lambda event: self.hover_on(event, "red", admin_logout))
        admin_logout.bind("<Leave>", lambda event: self.hover_off(event, "black", admin_logout))

    def logout(self, log_out_f):
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to logout?")
        if confirm:
            animation = SlideAnimation(self.anime_y, self.frame_main, self.login_window)
            animation.slide_down()
            log_out_f.destroy()
            # exit()


if __name__ == "__main__":
    admin_panel()
