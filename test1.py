import customtkinter as ctk

def login(event=None):  # event=None allows the function to work with both button click and key press
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "admin" and password == "1234":
        print("Login successful")
    else:
        print("Invalid credentials")

app = ctk.CTk()
app.geometry("300x200")
app.title("Login")

# Username
username_entry = ctk.CTkEntry(app, placeholder_text="Username")
username_entry.pack(pady=10)

# Password
password_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*")
password_entry.pack(pady=10)

# Login button
login_button = ctk.CTkButton(app, text="Login", command=login)
login_button.pack(pady=10)

# Bind Enter key to login function
app.bind("<Return>", login)

app.mainloop()
