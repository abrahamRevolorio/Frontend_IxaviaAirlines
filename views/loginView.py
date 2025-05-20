from tkinter import Toplevel, StringVar
from ttkbootstrap import Label, Entry, Button, Frame
from tkinter import messagebox
from utils.validators import isValidEmail
from core.apiClient import loginUser

from utils.styles import centerWindow

session = {}

def showLoginView(parent):

    window = Toplevel(parent)
    window.title("Login - IXAVIA Airlines")
    window.geometry("500x400")
    centerWindow(window)
    window.grab_set()

    def onClose():
        if messagebox.askokcancel("Cerrar", "¿Cerrar el Login?"):
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", onClose)

    Label(window, text="Iniciar Sesión", font=("Helvetica", 24, "bold")).pack(pady=20)

    formFrame = Frame(window, padding=20)
    formFrame.pack()

    emailVar = StringVar()
    passwordVar = StringVar()
    emailValid = [False]
    passwordValid = [False]

    def validateEmail(_):
        email = emailVar.get().strip()
        if not email:
            emailErrorLabel.config(text="El campo es obligatorio.")
            emailValid[0] = False
        elif not isValidEmail(email):
            emailErrorLabel.config(text="Correo inválido.")
            emailValid[0] = False
        else:
            emailErrorLabel.config(text="")
            emailValid[0] = True
        updateLoginButtonState()

    def validatePassword(_):
        password = passwordVar.get().strip()
        if not password:
            passwordErrorLabel.config(text="El campo es obligatorio.")
            passwordValid[0] = False
        else:
            passwordErrorLabel.config(text="")
            passwordValid[0] = True
        updateLoginButtonState()

    def updateLoginButtonState():
        if emailValid[0] and passwordValid[0]:
            loginBtn.config(state="normal")
        else:
            loginBtn.config(state="disabled")

    Label(formFrame, text="Correo electrónico:").grid(row=0, column=0, sticky="w")
    emailEntry = Entry(formFrame, textvariable=emailVar, width=40)
    emailEntry.grid(row=1, column=0, columnspan=2, pady=(0, 2))
    emailEntry.bind("<FocusOut>", validateEmail)
    emailErrorLabel = Label(formFrame, text="", foreground="red")
    emailErrorLabel.grid(row=2, column=0, columnspan=2, sticky="w")

    Label(formFrame, text="Contraseña:").grid(row=3, column=0, sticky="w", pady=(10, 0))
    passwordEntry = Entry(formFrame, textvariable=passwordVar, show="*", width=40)
    passwordEntry.grid(row=4, column=0, columnspan=2, pady=(0, 2))
    passwordEntry.bind("<FocusOut>", validatePassword)
    passwordErrorLabel = Label(formFrame, text="", foreground="red")
    passwordErrorLabel.grid(row=5, column=0, columnspan=2, sticky="w")

    result = {"info": None}

    def handleLogin():

        email = emailVar.get().strip()
        password = passwordVar.get().strip()
        result = loginUser(email, password)

        if result["success"]:

            global session

            session = result

            print(session)

            messagebox.showinfo("Bienvenido", f"Bienvenido {session['nombre']} ({session['apellido']}) con rol {session['rol']}")
            window.destroy()

        else:
            messagebox.showerror("Error", result["message"])

    navFrame = Frame(formFrame)
    navFrame.grid(row=6, column=0, columnspan=2, pady=20)

    loginBtn = Button(navFrame, text="Iniciar sesión", style='success.TButton', width=20, command=handleLogin, state="disabled")
    loginBtn.grid(row=0, column=0, padx=(0, 6))

    cancelBtn = Button(navFrame, text="Cancelar", style='danger.TButton', width=20, command=window.destroy)
    cancelBtn.grid(row=0, column=1)

    window.wait_window()
    return result["info"]
