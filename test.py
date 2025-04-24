import customtkinter as ctk

def add_placeholder(event=None):
    if textbox.get("1.0", "end-1c").strip() == "":
        textbox.insert("1.0", placeholder_text)
        textbox.configure(text_color="gray")

def remove_placeholder(event=None):
    if textbox.get("1.0", "end-1c").strip() == placeholder_text:
        textbox.delete("1.0", "end")
        textbox.configure(text_color="black")

root = ctk.CTk()

placeholder_text = "Enter your message here..."

textbox = ctk.CTkTextbox(root, width=300, height=100)
textbox.pack(pady=20)

# Set initial placeholder
add_placeholder()

# Bind focus in/out
textbox.bind("<FocusIn>", remove_placeholder)
textbox.bind("<FocusOut>", add_placeholder)

root.mainloop()
