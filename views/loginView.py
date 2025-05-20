# screens/loginScreen.py

from tkinter import Toplevel, StringVar
from ttkbootstrap import Label, Entry, Button, Frame, Style
from tkinter import messagebox
import requests
from utils.validators import isValidEmail
from core.apiClient import loginUser

def showLoginView(parent):
    window = Toplevel(parent)
    window.title("Login - IXAVIA Airlines")
    window.geometry("500x400")
    window.grab_set()

    def onClose():
        if messagebox.askokcancel("Cerrar", "¿Cerrar el Login?"):
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", onClose)

    Label(window, text="Iniciar Sesión", font=("Helvetica", 24, "bold")).pack(pady=20)

    frame = Frame(window, padding=20)
    frame.pack()

    emailVar = StringVar()
    passwordVar = StringVar()

    # ===== Email =====
    Label(frame, text="Correo electrónico:").grid(row=0, column=0, sticky="w", pady=5)
    emailEntry = Entry(frame, textvariable=emailVar, width=40)
    emailEntry.grid(row=1, column=0, columnspan=2, pady=5)

    # ===== Password =====
    Label(frame, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=5)
    passwordEntry = Entry(frame, textvariable=passwordVar, show="*", width=40)
    passwordEntry.grid(row=3, column=0, columnspan=2, pady=5)

    # ===== Botón Login =====
    def handleLogin():
        email = emailVar.get().strip()
        password = passwordVar.get().strip()

        if not isValidEmail(email):
            messagebox.showwarning("Correo inválido", "Ingrese un correo válido con formato correcto.")
            return
        if not password:
            messagebox.showwarning("Contraseña vacía", "Ingrese su contraseña.")
            return

        result = loginUser(email, password)
        if result["success"]:
            rol = result["rol"]
            messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso. Rol detectado: {rol}")
            window.destroy()
        else:
            messagebox.showerror("Error", result["message"])

    Button(frame, text="Iniciar sesión", bootstyle="primary", width=20, command=handleLogin).grid(row=4, column=0, pady=20)

    Button(frame, text="Cancelar", bootstyle="secondary", width=20, command=window.destroy).grid(row=4, column=1, pady=20)
