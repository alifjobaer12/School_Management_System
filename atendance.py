import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from datetime import date

class AttendanceForm:
    def __init__(self, master, teacher_username):
        # # super().__init__(master)
        # self.title("Take Attendance")
        # self.geometry("700x850")

        # Database connection setup
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="alifjobaer12",
            database="sms_p_db_backup",
            port=3306
        ) 
        # self.db = mysql.connector.connect(**self.db_config)
        self.cursor = self.db.cursor()
        self.attendence_frame = master
        self.teacher_username = teacher_username

        # Variables
        # self.teacher_username = ctk.StringVar()
        self.class_var = ctk.StringVar()
        self.section_var = ctk.StringVar()
        self.subject_var = ctk.StringVar()

        self.attendance_data = {}
        self.classes = []
        self.sections = []
        self.subjects = []

        # UI
        self.create_form()

    def create_form(self):
        ctk.CTkLabel(self.attendence_frame, text=f"Teacher {self.teacher_username}", font=("Helvetica", 20, "bold"),).pack(pady=5)
        # self.teacher_entry = ctk.CTkEntry(self.attendence_frame, textvariable=self.teacher_username.pack(pady=5)

        # ctk.CTkButton(self.attendence_frame, text="Load Teacher Subjects", command=self.load_teacher_subjects).pack(pady=10)

        ctk.CTkLabel(self.attendence_frame, text="Select Class",font=("Helvetica", 16, "bold")).place(x=100, y=70, anchor="center")
        self.class_menu = ctk.CTkComboBox(self.attendence_frame, font=("Helvetica", 16, "bold"), values=self.classes, variable=self.class_var)
        self.class_menu.place(x=100, y=100, anchor="center")

        ctk.CTkLabel(self.attendence_frame, text="Select Section", font=("Helvetica", 16, "bold")).place(x=350, y=70, anchor="center")
        self.section_menu = ctk.CTkComboBox(self.attendence_frame, font=("Helvetica", 16, "bold"), values=self.sections, variable=self.section_var)
        self.section_menu.place(x=350, y=100, anchor="center")

        ctk.CTkLabel(self.attendence_frame, text="Select Subject", font=("Helvetica", 16, "bold"),).place(x=600, y=70, anchor="center")
        self.subject_menu = ctk.CTkComboBox(self.attendence_frame, font=("Helvetica", 16, "bold"), values=self.subjects, variable=self.subject_var)
        self.subject_menu.place(x=600, y=100, anchor="center")

        self.load_btn = ctk.CTkButton(self.attendence_frame, text="Load Students", font=("Helvetica", 14, "bold"), command=self.load_students)
        self.load_btn.place(x=350, y=170, anchor="center")

        self.header_frame = ctk.CTkFrame(self.attendence_frame,)
        self.header_frame.place(x=350, y=230, anchor="center",)
        headers = ["SL No", "Roll", "Name", "Present", "Absent", "Today"]
        widths = [50, 80, 250, 85, 70, 80]
        for i, header in enumerate(headers):
            ctk.CTkLabel(self.header_frame, text=header, width=widths[i], anchor="center").grid(row=0, column=i, padx=2)

        self.student_frame = ctk.CTkScrollableFrame(self.attendence_frame, width=650, height=550)
        self.student_frame.place(x=350, y=530, anchor="center")

        self.save_btn = ctk.CTkButton(self.attendence_frame, font=("Helvetica", 14, "bold"), text="Save Attendance", command=self.save_attendance).place(x=350, y=850, anchor="center")

        self.load_teacher_subjects()

    def load_teacher_subjects(self):
        username = self.cursor.execute(
            "SELECT DISTINCT class, section, sub_name FROM subjects_backup WHERE username=%s",
            (self.teacher_username,)
        )
        results = self.cursor.fetchall()

        self.classes = sorted(set([row[0] for row in results]))
        self.sections = sorted(set([row[1] for row in results]))
        self.subjects = sorted(set([row[2] for row in results]))

        self.class_menu.configure(values=self.classes)
        self.section_menu.configure(values=self.sections)
        self.subject_menu.configure(values=self.subjects)

        if self.classes: self.class_var.set(self.classes[0])
        if self.sections: self.section_var.set(self.sections[0])
        if self.subjects: self.subject_var.set(self.subjects[0])

    def load_students(self):
        for widget in self.student_frame.winfo_children():
            widget.destroy()

        class_val = self.class_var.get()
        section_val = self.section_var.get()

        if not class_val or not section_val:
            messagebox.showerror("Input Error", "Subject, Class and Section are required.")
            return

        self.cursor.execute(
            "SELECT id, roll, s_name FROM students_backup WHERE class=%s AND section=%s order by roll",
            (class_val, section_val)
        )
        students = self.cursor.fetchall()
        self.attendance_data.clear()

        for i, (sid, roll, name) in enumerate(students, start=1):
            self.cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=%s AND status=1", (sid,))
            present_count = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=%s AND status=0", (sid,))
            absent_count = self.cursor.fetchone()[0]

            row = ctk.CTkFrame(self.student_frame)
            row.pack(fill="x", pady=2, padx=5)

            entries = [str(i), str(roll), name, str(present_count), str(absent_count)]
            widths = [45, 75, 250, 90, 110]

            for j, val in enumerate(entries):
                ctk.CTkLabel(row, text=val, width=widths[j], anchor="center").grid(row=0, column=j, padx=2)

            var = ctk.BooleanVar(value=True)
            checkbox = ctk.CTkCheckBox(row, text="", variable=var, onvalue=True, offvalue=False, width=80)
            checkbox.grid(row=0, column=5)

            self.attendance_data[sid] = var

    def save_attendance(self):
        subject = self.subject_var.get()
        class_val = self.class_var.get()
        section_val = self.section_var.get()
        t_username = self.teacher_username

        if not subject or not t_username:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        today = date.today()
        try:
            for student_id, present_var in self.attendance_data.items():
                status = 1 if present_var.get() else 0
                self.cursor.execute("""
                    INSERT INTO attendance (student_id, class, section, subject, date, status, t_username)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (student_id, class_val, section_val, subject, today, status, t_username))

            self.db.commit()
            messagebox.showinfo("Success", "Attendance saved successfully.")
            self.attendence_frame.destroy()
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to save attendance.\n{e}")

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
