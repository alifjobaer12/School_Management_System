import customtkinter as ctk
from tkinter import messagebox
from sql_query import MySQLQuery
from datetime import date
import threading


class AttendanceForm:
    def __init__(self, master, teacher_username):

        def first():
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")

            # sql backend
            self.sql = MySQLQuery()

            self.attendence_frame = master
            self.attendence_frame.configure(fg_color="#D7E6FF")
            self.teacher_username = teacher_username

            # Variables
            self.class_var = ctk.StringVar()
            self.section_var = ctk.StringVar()
            self.subject_var = ctk.StringVar()

            self.attendance_data = {}
            self.classes = []
            self.sections = []
            self.subjects = []

            # UI
            self.create_form()

        threading.Thread(target=first, daemon=True).start()


    def create_form(self):

        ctk.CTkLabel(self.attendence_frame, text=f"Teacher {self.teacher_username}", font=("Helvetica", 20, "bold"),).pack(pady=5)

        ctk.CTkLabel(self.attendence_frame, text="Class",font=("Helvetica", 16, "bold")).place(x=100, y=70, anchor="center")
        self.class_menu = ctk.CTkComboBox(self.attendence_frame, justify="center", state="readonly", font=("Helvetica", 16, "bold"), corner_radius=7, border_width=0, fg_color="#ffffff", text_color="#2c3e50", button_color="#4a6fa5", button_hover_color="#3b5c86", dropdown_fg_color="#f0f4fa", dropdown_text_color="#2c3e50", dropdown_hover_color="#d0e0f5", values=self.classes, variable=self.class_var, command=self.find_section)
        self.class_menu.place(x=100, y=100, anchor="center")

        ctk.CTkLabel(self.attendence_frame, text="Section", font=("Helvetica", 16, "bold")).place(x=350, y=70, anchor="center")
        self.section_menu = ctk.CTkComboBox(self.attendence_frame, justify="center", state="disabled", font=("Helvetica", 16, "bold"), corner_radius=7, border_width=0, fg_color="#ffffff", text_color="#2c3e50", button_color="#4a6fa5", button_hover_color="#3b5c86", dropdown_fg_color="#f0f4fa", dropdown_text_color="#2c3e50", dropdown_hover_color="#d0e0f5", values=self.sections, variable=self.section_var, command=self.find_subject)
        self.section_menu.place(x=350, y=100, anchor="center")

        ctk.CTkLabel(self.attendence_frame, text="Subject", font=("Helvetica", 16, "bold"),).place(x=600, y=70, anchor="center")
        self.subject_menu = ctk.CTkComboBox(self.attendence_frame, justify="center", state="disabled", font=("Helvetica", 16, "bold"), corner_radius=7, border_width=0, fg_color="#ffffff", text_color="#2c3e50", button_color="#4a6fa5", button_hover_color="#3b5c86", dropdown_fg_color="#f0f4fa", dropdown_text_color="#2c3e50", dropdown_hover_color="#d0e0f5", values=self.subjects, variable=self.subject_var)
        self.subject_menu.place(x=600, y=100, anchor="center")

        self.load_btn = ctk.CTkButton(self.attendence_frame, text="Load Students", font=("Helvetica", 14, "bold"), command=self.load_students)
        self.load_btn.place(x=350, y=170, anchor="center")

        self.header_frame = ctk.CTkFrame(self.attendence_frame, fg_color="white")
        self.header_frame.place(x=350, y=275, anchor="center",)
        Today = date.today()
        headers = ["SL No", "Roll", "Name", "Present", "Absent", Today]
        widths = [65, 80, 250, 85, 70, 95]
        for i, header in enumerate(headers):
            ctk.CTkLabel(self.header_frame, text=header, width=widths[i], anchor="center").grid(row=0, column=i, padx=2)

        self.student_frame = ctk.CTkScrollableFrame(self.attendence_frame, width=650, height=500, fg_color="white")
        self.student_frame.place(x=350, y=550, anchor="center")

        self.save_btn = ctk.CTkButton(self.attendence_frame, font=("Helvetica", 14, "bold"), text="Save Attendance", command=self.save_attendance).place(x=350, y=850, anchor="center")

        ctk.CTkLabel(self.attendence_frame, text=f"Today Date : {date.today()} ", font=("Helvetica", 13, "bold"), width=1, height=1).place(x=100, y=23, anchor="center")

        self.find_class()

    def find_section(self, selected_class):

        def theading_find_section():

            self.selected_class = selected_class

            # sql backend
            self.all_sections_list = self.sql.att_find_section(self.teacher_username, self.selected_class)

            self.section_menu.configure(values=self.all_sections_list, state="readonly")
    
            self.section_menu.set("")
            self.subject_menu.set("")
            self.subject_menu.configure(values=[], state="disabled")

        threading.Thread(target=theading_find_section, daemon=True).start()
    
    def find_subject(self, selected_section):

        def theading_find_subject():


            self.selected_section = selected_section

            # sql backend
            self.all_subject_list = self.sql.att_find_subject(self.teacher_username, self.selected_class, self.selected_section)
            
            self.subject_menu.configure(values=self.all_subject_list, state="readonly")

        threading.Thread(target=theading_find_subject, daemon=True).start()

    def find_class(self):

        def theading_find_class():

            # sql backend
            self.classes = self.sql.att_find_class(self.teacher_username)

            self.class_menu.configure(values=self.classes)

        threading.Thread(target=theading_find_class, daemon=True).start()

    def load_students(self):

        def theading_load_student():

            for widget in self.student_frame.winfo_children():
                widget.destroy()

            class_val = self.class_menu.get()
            section_val = self.section_menu.get()
            subject_val = self.subject_menu.get()

            if not class_val or not section_val or not subject_val:
                messagebox.showerror("Input Error", "Subject, Class and Section are required.")
                return

            # sql backend
            students = self.sql.att_load_student(class_val, section_val)
            self.attendance_data.clear()

            for i, (sid, roll, name) in enumerate(students, start=1):
                
                # sql backend
                self.present_count = self.sql.att_std_present(sid,)

                # sql backend
                self.absent_count = self.sql.att_std_absent(sid)

                row = ctk.CTkFrame(self.student_frame)
                row.pack(fill="x", pady=2, padx=5)

                entries = [str(i), str(roll), name, str(self.present_count), str(self.absent_count)]
                widths = [45, 95, 250, 75, 90]

                for j, val in enumerate(entries):
                    ctk.CTkLabel(row, text=val, width=widths[j], fg_color="#D7E6FF", anchor="center").grid(row=0, column=j, padx=2)

                var = ctk.BooleanVar(value=True)
                checkbox = ctk.CTkCheckBox(row, text="", variable=var, onvalue=True, offvalue=False, width=50, height=35)
                checkbox.grid(row=0, column=5, padx=(20,0))

                self.attendance_data[sid] = var

                ctk.CTkLabel(self.attendence_frame, text=f"All Student of Subject {subject_val}, Class {class_val} & Section {section_val} ", font=("Helvetica", 14, "bold"), width=1, height=1, fg_color="transparent").place(x=350, y=245, anchor="center")

                ctk.CTkLabel(self.attendence_frame, text=f"Total Class of Subject {self.subject_menu.get()} = {self.present_count + self.absent_count} ", font=("Helvetica", 14, "bold"), width=1, height=1, fg_color="transparent").place(x=350, y=220, anchor="center")

        threading.Thread(target=theading_load_student, daemon=True).start()


    def save_attendance(self):

        # def theading_save_student():

            class_val = self.class_menu.get()
            section_val = self.section_menu.get()
            subject = self.subject_menu.get()
            t_username = self.teacher_username

            if not subject or not t_username or not class_val or not section_val:
                messagebox.showerror("Input Error", "All fields are required.")
                return

            today = date.today()
            try:
                for student_id, present_var in self.attendance_data.items():
                    status = 1 if present_var.get() else 0

                # sql backend
                save = self.sql.att_save_attendance(student_id, class_val, section_val, subject, today, status, t_username)

                if save is True:
                    messagebox.showinfo("Success", "Attendance saved successfully.")
                    self.attendence_frame.destroy()
                else:
                    messagebox.showerror(save)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save attendance.\n{e}")

        # threading.Thread(target=theading_save_student, daemon=True).start()










# Example function to open form
def open_attendance_form():

    alif = ctk.CTk()
    alif.geometry("700x900")
    # ctk.CTkButton(alif, text="Take Attendance", command=open_attendance_form).pack(pady=30)
    AttendanceForm(alif, "@rabbiler")
    alif.mainloop()

# open_attendance_form()
# For testing as standalone
# if __name__ == "__main__":
#     root = ctk.CTk()
#     root.geometry("300x200")
#     ctk.CTkButton(root, text="Take Attendance", command=open_attendance_form).pack(pady=30)
#     root.mainloop()
