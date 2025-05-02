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


    def add_users(self, user_info):
        try:
            sql = """INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s);"""

            values = (user_info['username'], user_info['pass'], user_info['role'] )
            
            self.cursor.execute(sql, values)
            self.db.commit()

            return True
        except mysql.connector.IntegrityError as e:
            return f"Error : {e}"
        except Exception as e:
            return f"Error : {e}"
        pass

    # 1. Add Student
    def add_student(self, student_data: dict):
        try:
            sql = """INSERT INTO students (username, s_name, class, roll, section, grade, pn_number, address, tution_fee, paid_fee)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            values = (student_data['username'], student_data['s_name'], student_data['class'], student_data['roll'], student_data['section'], student_data['grade'], student_data['pn_number'], student_data['address'], student_data['tution_fee'], student_data['paid_fee'] )
            
            self.cursor.execute(sql, values)
            self.db.commit()

            return True
        except mysql.connector.IntegrityError as e:
            return f"Error : {e}"
        except Exception as e:
            return f"Error : {e}"


    # 2. Find Student
    def find_student(self, username):
        self.cursor.execute("SELECT * FROM students WHERE username = %s;", (username,))
        f_s = self.cursor.fetchone()
        return f_s
        


    # 3. Delete Student
    def delete_student(self, username):
        try:
            ck = self.find_student(username)
            if ck is not None:
                self.cursor.execute("DELETE FROM students WHERE username = %s;", (username,))
                self.db.commit()
                return True
            else:
                return "❌ Student Not Found"
            
        except Exception as e:
            return f"❌ [Error] Failed to delete student: {e}"

    # 4. All Students
    def all_students(self):
        self.cursor.execute("SELECT * FROM students;")
        return self.cursor.fetchall()

    # 5. Student Routine
    def student_routine(self, username):
        self.cursor.execute("SELECT subject_name, class, section, class_start_time, class_end_time FROM subject WHERE username = %s", (username,))
        return self.cursor.fetchall()

    # 6. Add Teacher
    def add_teacher(self, teacher_data: dict):
        
        try:
            sql = """INSERT INTO teacher (username, t_name, t_pn_number, t_address)
                     VALUES (%s, %s, %s, %s)"""
            values = (
                teacher_data['username'], teacher_data['name'],
                teacher_data['phone'], teacher_data['address']
            )
            self.cursor.execute(sql, values)
            self.db.commit()
            return True
        except mysql.connector.IntegrityError as e:
            print(f"[Error] Failed to add teacher: {e}")
            return False
        except Exception as e:
            print(f"[Error] Unexpected error: {e}")
            return False

    # 7. Find Teacher
    def find_teacher(self, username):
        self.cursor.execute("SELECT * FROM teacher WHERE username = %s", (username,))
        f_t = self.cursor.fetchone()
        return f_t

    # 8. Delete Teacher
    def delete_teacher(self, username):
        try:
            ck = self.find_teacher(username)
            if ck is not None:
                self.cursor.execute("DELETE FROM teacher WHERE username = %s;", (username,))
                self.db.commit()
                return True
            else:
                return "❌ Teacher Not Found"
            
        except Exception as e:
            return f"❌ [Error] Failed to delete student: {e}"

    # 9. Teacher Info
    def teacher_info(self, username):
        try:
            self.cursor.execute("SELECT t_name FROM teacher WHERE username = %s", (username,))
            name = self.cursor.fetchone()

            return name
        
        except Exception as e:
            return False

    def teacher_total_sub(self, username):
        try:
            self.cursor.execute("SELECT COUNT(sub_name) FROM subjects WHERE username= %s GROUP BY t_name;" , (username,))
            t_t_sub = self.cursor.fetchone()

            return t_t_sub
        
        except Exception as e:
            return False

    # 10. All Teachers
    def all_teachers(self):
        self.cursor.execute("SELECT * FROM teacher;")
        return self.cursor.fetchall()

    # 11. Teacher Routine
    def teacher_routine(self, username):
        self.cursor.execute("SELECT sub_name, class, section, class_start_time, class_end_time FROM subjects WHERE username = %s", (username,))
        return self.cursor.fetchall()
    
    def add_subject(self, sub_info: dict):

        try:
            sql = """INSERT INTO subjects (sub_name, username, t_name, class, class_start_time, class_end_time, section)
                     VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            values = (
                sub_info['subject'],sub_info['username'], sub_info['name'], 
                sub_info['class'], sub_info['start_t'], sub_info['end_t'],sub_info['section']
            )
            self.cursor.execute(sql, values)
            self.db.commit()
            return True
        except mysql.connector.IntegrityError as e:
            print(f"[Error] Failed to add teacher: {e}")
            return False
        except Exception as e:
            print(f"[Error] Unexpected error: {e}")
            return False


    def update_fees(self, username, tuition_fee, paid_fee):
        try:
            self.cursor.execute("SELECT paid_fee, tution_fee FROM students WHERE username = %s", (username,))
            result = self.cursor.fetchone()
    
            if not result:
                return "❌ User not found."
    
            current_paid, current_tuition = result
    
            tuition_fee = int(tuition_fee) if tuition_fee else 0
            paid_fee = int(paid_fee) if paid_fee else 0
    
            new_paid = current_paid + paid_fee
            new_tuition = current_tuition + tuition_fee
    
            if tuition_fee > 0:
                self.cursor.execute(
                    "UPDATE students SET tution_fee = %s, paid_fee = %s WHERE username = %s",
                    (new_tuition, new_paid, username)
                )
            else:
                self.cursor.execute(
                    "UPDATE students SET paid_fee = %s WHERE username = %s",
                    (new_paid, username)
                )
    
            self.db.commit()
            return True
    
        except Exception as e:
            return f"❌ Error updating fees: {e}"

