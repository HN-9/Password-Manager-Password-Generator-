import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from crypto_vault import load_vault, save_vault
from password_utils import generate_password

import pyperclip

# ---------------------------------------------------
# LOGIN SYSTEM
# ---------------------------------------------------
MASTER_PASSWORD = "admin123"   # you can replace this

def login_screen():
    login = ttk.Window(themename="flatly")
    login.title("Login - Password Manager")
    login.geometry("350x220")

    ttk.Label(login, text="🔐 MASTER LOGIN", font=("Helvetica", 18, "bold")).pack(pady=20)

    pass_entry = ttk.Entry(login, show="*", width=30, bootstyle="info")
    pass_entry.pack(pady=10)

    def check():
        if pass_entry.get() == MASTER_PASSWORD:
            login.destroy()
            main_app()
        else:
            messagebox.showerror("Error", "Incorrect master password")

    ttk.Button(login, text="Login", bootstyle="success-outline", command=check).pack(pady=10)
    login.mainloop()


# ---------------------------------------------------
# MAIN APP
# ---------------------------------------------------
def main_app():
    root = ttk.Window(themename="flatly")
    root.title("Password Manager")
    root.geometry("800x500")

    ttk.Label(root, text="🔑 Password Manager", font=("Helvetica", 22, "bold")).pack(pady=20)

    # Load data
    vault = load_vault()

    # Search bar
    search_entry = ttk.Entry(root, width=40, bootstyle="info")
    search_entry.pack()

    def refresh_list():
        listbox.delete(0, tk.END)
        for site in vault:
            listbox.insert(tk.END, site)

    def search():
        q = search_entry.get().lower()
        listbox.delete(0, tk.END)
        for site in vault:
            if q in site.lower():
                listbox.insert(tk.END, site)

    ttk.Button(root, text="Search", bootstyle="primary-outline", command=search).pack(pady=5)

    # Listbox for stored sites
    listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
    listbox.pack(pady=10)
    refresh_list()

    # Website/Username/Password fields
    form_frame = ttk.Frame(root)
    form_frame.pack(pady=10)

    ttk.Label(form_frame, text="Website:").grid(row=0, column=0, padx=5)
    website_entry = ttk.Entry(form_frame, width=40)
    website_entry.grid(row=0, column=1)

    ttk.Label(form_frame, text="Username:").grid(row=1, column=0, padx=5)
    username_entry = ttk.Entry(form_frame, width=40)
    username_entry.grid(row=1, column=1)

    ttk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=5)
    password_entry = ttk.Entry(form_frame, width=40)
    password_entry.grid(row=2, column=1)

    # Generate password
    def gen_pass():
        pwd = generate_password(14)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, pwd)

    ttk.Button(form_frame, text="Generate", bootstyle="warning", command=gen_pass).grid(row=2, column=2, padx=10)

    # Copy password
    def copy_pwd():
        pyperclip.copy(password_entry.get())
        messagebox.showinfo("Copied", "Password copied to clipboard")

    ttk.Button(form_frame, text="Copy", bootstyle="secondary", command=copy_pwd).grid(row=2, column=3, padx=10)

    # Save entry
    def save_entry():
        site = website_entry.get()
        user = username_entry.get()
        pwd = password_entry.get()

        vault[site] = {"username": user, "password": pwd}
        save_vault(vault)

        refresh_list()
        messagebox.showinfo("Saved", "Password saved")

    ttk.Button(root, text="Save Entry", bootstyle="success", command=save_entry).pack(pady=5)

    # Delete entry
    def delete_entry():
        site = listbox.get(tk.ACTIVE)
        if site in vault:
            del vault[site]
            save_vault(vault)
            refresh_list()

    ttk.Button(root, text="Delete Entry", bootstyle="danger", command=delete_entry).pack(pady=5)

    # Export vault
    def export():
        with open("export.txt", "w") as f:
            for site, data in vault.items():
                f.write(f"{site} → {data['username']} : {data['password']}\n")
        messagebox.showinfo("Exported", "Passwords exported to export.txt")

    ttk.Button(root, text="Export", bootstyle="info", command=export).pack(pady=10)

    root.mainloop()


# Start app
login_screen()
