import mysql.connector

class MySQLQuery:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="mysql-3aa5cf7b-islam12islam1221-3bb6.h.aivencloud.com",
            user="group_member",
            password="AVNS_Q1-nT1BInCka8F6jYU7",
            database="alif",
            port=12492
        )
        self.cursor = self.db.cursor()

    # 1. Add Student
    def add_student(self, student_data):
        try:
            sql = """
            INSERT INTO students 
            (username, s_name, class, roll, section, grade, pn_number, address, tution_fee, paid_fee) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1000, 0);
            """
            self.cursor.execute(sql, student_data)
            self.db.commit()
            return True
        except mysql.connector.IntegrityError as e:
            return f"Error : {e}"
        except Exception as e:
            return f"Error : {e}"


    # 2. Find Student
    def find_student(self, username):
        self.cursor.execute("SELECT * FROM students WHERE username = %s", (username,))
        return self.cursor.fetchone()

    # 3. Delete Student
    def delete_student(self, username):
        try:
            self.cursor.execute("DELETE FROM students WHERE username = %s", (username,))
            return True
        except Exception as e:
            print(f"[Error] Failed to delete student: {e}")
            return False

    # 4. Student Info
    def student_info(self, username):
        self.cursor.execute("SELECT name, grade, section, roll FROM students WHERE username = %s", (username,))
        return self.cursor.fetchone()

    # 5. All Students
    def all_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    # 6. Student Routine
    def student_routine(self, username):
        self.cursor.execute("SELECT subject_name, class, section, class_start_time, class_end_time FROM subject WHERE username = %s", (username,))
        return self.cursor.fetchall()

    # 7. Add Teacher
    def add_teacher(self, teacher_data: dict):
        required_fields = ['username', 'name', 'phone', 'address']
        missing_fields = [field for field in required_fields if field not in teacher_data]
        if missing_fields:
            print(f"[Error] Missing teacher fields: {', '.join(missing_fields)}")
            return False

        try:
            sql = """INSERT INTO teachers (username, name, phone, address)
                     VALUES (%s, %s, %s, %s)"""
            values = (
                teacher_data['username'], teacher_data['name'],
                teacher_data['phone'], teacher_data['address']
            )
            self.cursor.execute(sql, values)
            return True
        except mysql.connector.IntegrityError as e:
            print(f"[Error] Failed to add teacher: {e}")
            return False
        except Exception as e:
            print(f"[Error] Unexpected error: {e}")
            return False

    # 8. Find Teacher
    def find_teacher(self, username):
        self.cursor.execute("SELECT * FROM teachers WHERE username = %s", (username,))
        return self.cursor.fetchone()

    # 9. Delete Teacher
    def delete_teacher(self, username):
        try:
            self.cursor.execute("DELETE FROM teachers WHERE username = %s", (username,))
            return True
        except Exception as e:
            print(f"[Error] Failed to delete teacher: {e}")
            return False

    # 10. Teacher Info
    def teacher_info(self, username):
        self.cursor.execute("SELECT name, phone FROM teachers WHERE username = %s", (username,))
        return self.cursor.fetchone()

    # 11. All Teachers
    def all_teachers(self):
        self.cursor.execute("SELECT * FROM teachers")
        return self.cursor.fetchall()

    # 12. Teacher Routine
    def teacher_routine(self, username):
        self.cursor.execute("SELECT subject_name, class, section, class_start_time, class_end_time FROM subject WHERE username = %s", (username,))
        return self.cursor.fetchall()

    # 13. Student Fee
    def student_fee(self, username):
        self.cursor.execute("SELECT tuition_fee, paid_fee, (tuition_fee - paid_fee) AS due_fee FROM students WHERE username = %s", (username,))
        return self.cursor.fetchone()
