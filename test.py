import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database'
)

cursor = conn.cursor()

# Query all subjects for class 10
cursor.execute("SELECT sub_name, teacher_name FROM class_subjects WHERE class = '10';")

# Fetch and print row by row
for sub_name, teacher_name in cursor.fetchall():
    print(f"{sub_name} - {teacher_name}")

# Close the connection
cursor.close()
conn.close()
