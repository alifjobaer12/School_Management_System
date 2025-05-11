import mysql.connector
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class MySQLQuery:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            port=os.getenv("PORT")
        )
        self.cursor = self.db.cursor()
        self.encript_key = os.getenv("ENC_KEY")
        self.fernet = Fernet(self.encript_key)

    def log_in(self, username):
        try:
            sql = "SELECT password, role FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            access = self.cursor.fetchone()

            if access is None:
                return False
            
            password, role = access

            try:
                decrypted_password = self.fernet.decrypt(password.encode()).decode()
            except Exception as e:
                print(f"Decryption failed: {e}")
                return False

            return (decrypted_password, role)
            
        except:
            return False


    def add_users(self, user_info: dict):
        try:
            sql = """INSERT INTO users (username, password, role, s_q_a)
            VALUES (%s, %s, %s, %s);"""

            user_info['pass'] = self.fernet.encrypt(user_info['pass'].encode())

            values = (user_info['username'], user_info['pass'], user_info['role'], user_info['qna'])
            
            self.cursor.execute(sql, values)
            self.db.commit()

            return True
        except mysql.connector.IntegrityError as e:
            return f"Error : {e}"
        except Exception as e:
            return f"Error : {e}"

    def ck_class_roll_section(self, student_data: dict):
        try:
            sql = """SELECT COUNT(*) AS total FROM students WHERE class = %s AND roll = %s AND section = %s GROUP BY class, roll, LOWER(section) HAVING COUNT(*) > 0;"""
            self.cursor.execute(sql, (student_data['class'], student_data['roll'], student_data['section']))
            ck = self.cursor.fetchone()
            if ck is not None:
                return False
            else:
                return True
        except mysql.connector.IntegrityError as e:
            pass

    def ck_tec_class_sub_section(self, sub_info: dict):
        try:
            sql = """SELECT COUNT(*) AS total FROM subjects WHERE class = %s AND sub_name = %s AND section = %s AND class_start_time = %s AND class_end_time = %s GROUP BY class, LOWER(sub_name), LOWER(section), class_start_time, class_end_time HAVING COUNT(*) > 0;"""
            self.cursor.execute(sql, (sub_info['class'], sub_info['subject'], sub_info['section'], sub_info['start_t'], sub_info['end_t']))
            ck = self.cursor.fetchone()
            if ck is not None:
                return False
            else:
                return True
        except mysql.connector.IntegrityError as e:
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


    # 2. Find Student
    def find_student(self, username):
        sql = "SELECT * FROM students WHERE username = %s;"
        self.cursor.execute(sql, (username,))
        f_s = self.cursor.fetchone()
        return f_s
        


    # 3. Delete Student
    def delete_student(self, username):
        try:
            ck = self.find_student(username)
            if ck is not None:
                sql = "DELETE FROM students WHERE username = %s;"
                self.cursor.execute(sql, (username,))
                self.db.commit()
                return True
            else:
                return "❌ Student Not Found"
            
        except Exception as e:
            return f"❌ [Error] Failed to delete student: {e}"

    # 4. All Students
    def all_students(self):
        sql = "SELECT * FROM students;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 5. Student Routine
    def student_routine(self, username):
        try:
            sql = "SELECT class FROM students WHERE username = %s;"
            self.cursor.execute(sql, (username,))
            s_class = self.cursor.fetchone()
            # print(s_class)

            sql = "SELECT sub_name, t_name, class_start_time, class_end_time FROM subjects WHERE class = %s;"
            self.cursor.execute(sql, (s_class[0],))
            # print(self.cursor.fetchall())
            return self.cursor.fetchall()
        except Exception as e:
            return f"❌ Error : {e}"

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
            return False
        except Exception as e:
            return False

    # 7. Find Teacher
    def find_teacher(self, username):
        sql = "SELECT * FROM teacher WHERE username = %s"
        self.cursor.execute(sql, (username,))
        f_t = self.cursor.fetchone()
        return f_t

    # 8. Delete Teacher
    def delete_teacher(self, username):
        try:
            ck = self.find_teacher(username)
            if ck is not None:
                sql = "DELETE FROM teacher WHERE username = %s;"
                self.cursor.execute(sql, (username,))
                self.db.commit()
                return True
            else:
                return "❌ Teacher Not Found"
            
        except Exception as e:
            return f"❌ [Error] Failed to delete student: {e}"

    # 9. Teacher Info
    def teacher_info(self, username):
        try:
            sql = "SELECT t_name FROM teacher WHERE username = %s"
            self.cursor.execute(sql, (username,))
            name = self.cursor.fetchone()

            return name
        
        except Exception as e:
            return False

    def teacher_total_sub(self, username):
        try:
            sql = "SELECT COUNT(sub_name) FROM subjects WHERE username= %s GROUP BY t_name;"
            self.cursor.execute(sql, (username,))
            t_t_sub = self.cursor.fetchone()

            return t_t_sub
        
        except Exception as e:
            return False

    # 10. All Teachers
    def all_teachers(self):
        sql = "SELECT * FROM teacher;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 11. Teacher Routine
    def teacher_routine(self, username):
        sql = "SELECT sub_name, class, section, class_start_time, class_end_time FROM subjects WHERE username = %s"
        self.cursor.execute(sql, (username,))
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
            return False
        except Exception as e:
            return False

    def show_fees(self, username):
        try:
            sql = "SELECT tution_fee, paid_fee, (tution_fee - paid_fee) AS remaining_fee FROM students WHERE username = %s ;"
            self.cursor.execute(sql, (username,))
            return self.cursor.fetchone()
        except Exception as e:
            return f"❌ Error : {e}"

    def update_fees(self, username, tuition_fee, paid_fee):
        try:
            sql = "SELECT paid_fee, tution_fee FROM students WHERE username = %s"
            self.cursor.execute(sql, (username,))
            result = self.cursor.fetchone()
    
            if not result:
                return "❌ User not found."
    
            current_paid, current_tuition = result
    
            tuition_fee = int(tuition_fee) if tuition_fee else 0
            paid_fee = int(paid_fee) if paid_fee else 0
    
            new_paid = current_paid + paid_fee
            new_tuition = current_tuition + tuition_fee
    
            if tuition_fee > 0:
                sql = """UPDATE students SET tution_fee = %s, paid_fee = %s WHERE username = %s"""
                self.cursor.execute(sql, (new_tuition, new_paid, username))
            else:
                self.cursor.execute(
                    "UPDATE students SET paid_fee = %s WHERE username = %s",
                    (new_paid, username)
                )
    
            self.db.commit()
            return True
    
        except Exception as e:
            return f"❌ Error updating fees: {e}"

    def close_db(self):
        try:
            self.cursor.close()
            self.conn.close()
            return 0
        except Exception as e:
            return f"Error : {e}"
