import mysql.connector
from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
from customtkinter import *
from pathlib import Path
from animasion import SlideAnimation
import time


class teacher_panal:
    def __init__(self, tec_root_frame, t_username, anime_y, frame_main, login_window):
        set_appearance_mode("light")
        set_default_color_theme("blue")

        self.db = mysql.connector.connect(
            host="mysql-3aa5cf7b-islam12islam1221-3bb6.h.aivencloud.com",
            user="Pondit",
            password="AVNS_CBteuh8GdWD6fO6BrBg",
            database="alif",
            port="12492"
        )
        self.cursor = self.db.cursor()


        self.teacher_windo = tec_root_frame
        self.tec_username = t_username
        self.anime_y = anime_y 
        self.frame_main = frame_main
        self.login_window = login_window
        # self.teacher_windo.geometry("700x400+1200+100")
        # self.teacher_windo.title("Login - School Management System")

        self.create_main_frame()
        self.create_info_frame()
        self.create_class_routine()

        # self.teacher_windo.mainloop()

    def logout(self, log_out_f) :
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to logout?")
        if confirm:
            animation = SlideAnimation(self.anime_y, self.frame_main, self.login_window)
            animation.slide_down()
            log_out_f.destroy()
            # exit()


    def create_main_frame(self):
        # Teacher panel main frame
        self.tec_panal_frame = CTkFrame(self.teacher_windo, fg_color="sky blue", width=700, height=400)
        self.tec_panal_frame.place(x=350, y=200, anchor="center")

        self.tec_h_label = CTkLabel(self.tec_panal_frame, text=f"Teacher\n{'Hi! '}", width=1, height=1,
                                    fg_color="transparent", text_color="black", font=("Helvetica", 22, "bold"))
        self.tec_h_label.place(x=350, y=50, anchor="center")

        self.tec_logout = CTkButton(self.tec_panal_frame, text="⏻ Log Out", width=1, height=1,
                                    command=lambda:self.logout(self.tec_panal_frame), fg_color="transparent", text_color="black", font=("Helvetica", 16, "bold"), hover=False)
        self.tec_logout.place(x=640, y=50, anchor="center")
        self.tec_logout.bind("<Enter>", lambda event: self.hover_on(event, "red", self.tec_logout))
        self.tec_logout.bind("<Leave>", lambda event: self.hover_off(event, "black", self.tec_logout))

    def create_info_frame(self):
        # Info view frame inside the panel
        self.tec_info_view_frame = CTkFrame(self.tec_panal_frame, width=700, height=300, fg_color="transparent")
        self.tec_info_view_frame.place(x=350, y=230, anchor="center")

        self.cursor.execute("SELECT t_name FROM teacher WHERE username='ashikuzzaman01';")
        t_name = self.cursor.fetchone()

        self.cursor.execute("SELECT COUNT(sub_name) FROM subjects WHERE username='ashikuzzaman01' GROUP BY t_name;")
        total_sub = self.cursor.fetchone()

        tec_name_label = CTkLabel(self.tec_info_view_frame, text_color="black", text="Name",
                                  font=("Helvetica", 15, "bold"), anchor="w")
        tec_name_label.place(x=220, y=10)
        tec_tclass_label = CTkLabel(self.tec_info_view_frame, text_color="black", text="Total Class",
                                    font=("Helvetica", 15, "bold"), anchor="w")
        tec_tclass_label.place(x=220, y=40)

        name_value_label = CTkLabel(self.tec_info_view_frame, text=f":     {t_name[0]}", text_color="black",
                                        font=("Helvetica", 14, "bold"), anchor="w")
        name_value_label.place(x=320, y=10)

        class_value_label = CTkLabel(self.tec_info_view_frame, text=f":     {total_sub[0]}", text_color="black",
                                         font=("Helvetica", 14, "bold"), anchor="w")
        class_value_label.place(x=320, y=40)

    def create_class_routine(self):
        # Class routine display
        self.cursor.execute(
            "SELECT sub_name, class, section, class_start_time, class_end_time FROM subjects WHERE username = 'ashikuzzaman01';")
        results = self.cursor.fetchall()

        ruttin_label = CTkLabel(self.tec_info_view_frame, text="Class Routine", text_color="black",
                                width=1, height=1, fg_color="transparent", font=("Helvetica", 13, "bold"))
        ruttin_label.place(x=350, y=100, anchor="center")

        subject_box = CTkTextbox(self.tec_info_view_frame, wrap="none", activate_scrollbars=True,
                                 width=500, height=160, fg_color="transparent",
                                 scrollbar_button_color="sky blue", font=("Helvetica", 13, "bold"))
        subject_box.place(x=390, y=200, anchor="center")

        subject_box.delete('0.0', 'end')
        header = "Subject\t\t\tClass\tSection\t   Start Time\t\tEnd Time\n"
        subject_box.insert('end', header)
        subject_box.insert('end', "-" * 115 + '\n')

        for info in results:
            line = f"{info[0]}\t\t\t  {info[1]}\t  {info[2]}\t     {info[3]}\t\t {info[4]}\n"
            subject_box.insert('end', line)
        subject_box.configure(state="disabled")

    def hover_on(self, event, color, btn_name):
        btn_name.configure(text_color=color)

    def hover_off(self, event, color, btn_name):
        btn_name.configure(text_color=color)


if __name__ == "__main__":
    teacher_panal()
