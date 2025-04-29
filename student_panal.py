import mysql.connector
from customtkinter import *
from tkinter import messagebox
from animasion import SlideAnimation
from pathlib import Path

class student_panel:
    def __init__(self, std_root_frame, s_username, anime_y, frame_main, login_window):
        set_appearance_mode("light")
        set_default_color_theme("blue")

        self.db = mysql.connector.connect(
            host="mysql-3aa5cf7b-islam12islam1221-3bb6.h.aivencloud.com",
            user="Pondit",
            password="AVNS_CBteuh8GdWD6fO6BrBg",
            database="alif",
            port="12492"
        )
        self.std_root_frame = std_root_frame
        self.cursor = self.db.cursor()
        self.setup_login_window()
        self.anime_y = anime_y 
        self.frame_main = frame_main
        self.login_window = login_window


    def setup_login_window(self):
        self.login_window = self.std_root_frame
        # self.login_window.geometry("700x400")
        # self.login_window.title("Login - School Management System")

        self.create_student_panel()
        # self.login_window.mainloop()

    def create_student_panel(self):
        self.std_panal_frame = CTkFrame(self.login_window, fg_color="sky blue", width=800, height=400)
        self.std_panal_frame.place(x=350, y=200, anchor="center")

        # Header
        self.std_label = CTkLabel(self.std_panal_frame, text="Student\nHi!", width=1, height=1, fg_color="transparent",
                                      text_color="black", font=("Helvetica", 22, "bold"))
        self.std_label.place(x=400, y=50, anchor="center")

        # Logout Button
        self.std_logout = CTkButton(self.std_panal_frame, text="⏻ Log Out", width=1, height=1,
                                        fg_color="transparent", text_color="black", font=("Helvetica", 16, "bold"),
                                        hover=False, command=lambda:self.logout(self.std_panal_frame))
        self.std_logout.place(x=640, y=50, anchor="center")
        self.std_logout.bind("<Enter>", lambda event: self.hover_on(event, "red", self.std_logout))
        self.std_logout.bind("<Leave>", lambda event: self.hover_off(event, "black", self.std_logout))

        # Info Frame
        self.std_info_view_frame = CTkFrame(self.std_panal_frame, width=700, height=300, fg_color="transparent")
        self.std_info_view_frame.place(x=350, y=230, anchor="center")

        self.show_student_info()
        self.show_fee_info()
        self.show_class_routine()

    def hover_on(self, event, color, btn_name):
        btn_name.configure(text_color=color)

    def hover_off(self, event, color, btn_name):
        btn_name.configure(text_color=color)

    def logout(self, log_out_f):
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to logout?")
        if confirm:
            animation = SlideAnimation(self.anime_y, self.frame_main, self.login_window)
            animation.slide_down()
            log_out_f.destroy()

    def show_student_info(self):
        fields = ["Name", "Class", "Roll", "Section", "Grade"]
        self.cursor.execute("SELECT s_name, class, roll, section, grade FROM students WHERE username = 'rafihossain275';")
        info = list(self.cursor.fetchone())

        for i, (field, value) in enumerate(zip(fields, info)):
            label_field = CTkLabel(self.std_info_view_frame, text_color="black", text=field,
                                       font=("Helvetica", 14, "bold"), anchor="w")
            label_field.place(x=100, y=10 + i * 25)

            label_value = CTkLabel(self.std_info_view_frame, text=f":     {value}", text_color="black",
                                       font=("Helvetica", 14, "bold"), anchor="w")
            label_value.place(x=200, y=10 + i * 25)

    def show_fee_info(self):
        fee_frame = CTkFrame(self.std_info_view_frame, width=200, height=110, fg_color="transparent",
                                 border_width=2, border_color="white")
        fee_frame.place(x=570, y=60, anchor="center")

        fee_labels = ["Tution Fees", "Total Payed", "Due"]

        self.cursor.execute("SELECT tution_fee, paid_fee, (tution_fee - paid_fee) AS remaining_fee FROM students WHERE username = 'rafihossain275';")
        fee_details = list(self.cursor.fetchone())

        fee_header = CTkLabel(fee_frame, text_color="black", text="Fees", width=1, height=1,
                                  font=("Helvetica", 16, "bold"), anchor="w")
        fee_header.place(x=100, y=15, anchor="center")

        for i, (label, detail) in enumerate(zip(fee_labels, fee_details)):
            fee_label = CTkLabel(fee_frame, text_color="black", text=label, width=1, height=1,
                                     font=("Helvetica", 14, "bold"), anchor="w")
            fee_label.place(x=50, y=45 + i * 20, anchor="center")

            fee_value = CTkLabel(fee_frame, text=f":  {detail}", text_color="black", width=1, height=1,
                                     font=("Helvetica", 14, "bold"), anchor="w")
            fee_value.place(x=120, y=35 + i * 20)

            if label == "Due":
                fee_label.configure(text_color="red")
                fee_value.configure(text_color="red")

    def show_class_routine(self):
        self.cursor.execute("SELECT sub_name, t_name, class_start_time, class_end_time FROM subjects WHERE class = '10';")
        routine = self.cursor.fetchall()

        routine_label = CTkLabel(self.std_info_view_frame, text="Class Routine", text_color="black", width=1,
                                     height=1, fg_color="transparent", font=("Helvetica", 13, "bold"))
        routine_label.place(x=350, y=150)

        subject_box = CTkTextbox(self.std_info_view_frame, wrap="none", activate_scrollbars=True,
                                     width=500, height=160, fg_color="transparent", scrollbar_button_color="sky blue",
                                     font=("Helvetica", 13, "bold"))
        subject_box.place(x=160, y=170)

        subject_box.delete('0.0', 'end')
        header = "  Subject\t\t\t   Teacher\t\tStart Time\t\tEnd Time\n"
        subject_box.insert('end', header)
        subject_box.insert('end', "-" * 115 + '\n')

        for subject in routine:
            line = f"{subject[0]}\t\t\t{subject[1]}\t\t   {subject[2]}\t\t  {subject[3]}\n"
            subject_box.insert('end', line)

        subject_box.configure(state="disabled")


if __name__ == "__main__":
    student_panel()
