import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from datetime import date

class AttendanceForm(ctk.CTkToplevel):
    def __init__(self, tec_username, db_config):
        super().__init__()
        self.title("Take Attendance")
        self.geometry("600x800")

        self.db = mysql.connector.connect(**db_config)
        self.cursor = self.db.cursor()

        self.teacher_username = ctk.StringVar()
        self.class_var = ctk.StringVar()
        self.section_var = ctk.StringVar()
        self.subject_var = ctk.StringVar()
        self.tec_username = tec_username

        self.attendance_data = {}

        self.classes = []
        self.sections = []
        self.subjects = []

        self.create_form()
        self.load_teacher_subjects()

    def create_form(self):
        ctk.CTkLabel(self, text="Select Class").pack(pady=5)
        self.class_menu = ctk.CTkComboBox(self, values=self.classes, variable=self.class_var)
        self.class_menu.pack(pady=5)

        ctk.CTkLabel(self, text="Select Section").pack(pady=5)
        self.section_menu = ctk.CTkComboBox(self, values=self.sections, variable=self.section_var)
        self.section_menu.pack(pady=5)

        ctk.CTkLabel(self, text="Select Subject").pack(pady=5)
        self.subject_menu = ctk.CTkComboBox(self, values=self.subjects, variable=self.subject_var)
        self.subject_menu.pack(pady=5)

        self.load_btn = ctk.CTkButton(self, text="Load Students", command=self.load_students)
        self.load_btn.pack(pady=10)

        self.student_frame = ctk.CTkScrollableFrame(self, width=550, height=250)
        self.student_frame.pack(pady=10)

        self.save_btn = ctk.CTkButton(self, text="Save Attendance", command=self.save_attendance)
        self.save_btn.pack(pady=10)

    def load_teacher_subjects(self):
        self.cursor.execute(
            "SELECT DISTINCT class, section, sub_name FROM subjects_backup WHERE username=%s",
            (self.tec_username,)
        )
        results = self.cursor.fetchall()

        self.classes = sorted(set(row[0] for row in results if row[0]))
        self.sections = sorted(set(row[1] for row in results if row[1]))
        self.subjects = sorted(set(row[2] for row in results if row[2]))

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
            messagebox.showerror("Input Error", "Class and Section are required.")
            return

        self.cursor.execute(
            "SELECT id, roll, s_name FROM students_backup WHERE class=%s AND section=%s ORDER BY roll",
            (class_val, section_val)
        )
        students = self.cursor.fetchall()
        self.attendance_data.clear()

        for student_id, roll, name in students:
            row = ctk.CTkFrame(self.student_frame)
            row.pack(fill="x", pady=2, padx=10)

            ctk.CTkLabel(row, text=f"{roll}. {name}", width=200, anchor="w").pack(side="left")

            var = ctk.BooleanVar(value=True)
            checkbox = ctk.CTkCheckBox(row, text="", variable=var, onvalue=True, offvalue=False)
            checkbox.pack(side="left", padx=10)

            self.attendance_data[student_id] = var

    def save_attendance(self):
        subject = self.subject_var.get()
        class_val = self.class_var.get()
        section_val = self.section_var.get()

        if not subject:
            messagebox.showerror("Input Error", "Subject is required.")
            return

        today = date.today()
        try:
            for student_id, present_var in self.attendance_data.items():
                status = 1 if present_var.get() else 0
                self.cursor.execute("""
                    INSERT INTO attendance (student_id, class, section, subject, date, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (student_id, class_val, section_val, subject, today, status))

            self.db.commit()
            messagebox.showinfo("Success", "Attendance saved successfully.")
            self.destroy()
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to save attendance.\n{e}")

# Example function to open form
def open_attendance_form(tec_username):
    AttendanceForm(tec_username, db_config={
        'host': 'localhost',
        'user': 'root',
        'password': 'alifjobaer12',
        'database': 'sms_p_db_backup'
    })

# Uncomment below to run standalone
# if __name__ == "__main__":
#     open_attendance_form("some_teacher_username")
