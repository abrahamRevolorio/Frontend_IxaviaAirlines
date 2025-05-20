from tkinter import Toplevel, StringVar, messagebox
from tkinter import ttk, Frame as TkFrame
from ttkbootstrap import Style
import re

from utils.validators import isValidEmail, isSamePassword, isNotEmpty, isValidDpi, isValidPhone
from core.apiClient import registerUser
from utils.styles import centerWindow

def showRegisterView(parent):

    style = Style()

    window = Toplevel(parent)
    window.title("Registro")
    window.geometry("700x600")
    centerWindow(window)
    window.grab_set()

    def onClose():
        if messagebox.askokcancel("Cerrar", "¿Cerrar formulario?"):
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", onClose)

    ttk.Label(window, text="Crear una Cuenta", font=("Helvetica", 20, "bold")).pack(pady=10)

    container = ttk.Frame(window, padding=10)
    container.pack(fill="both", expand=True)

    currentPage = [0]

    fields = {
        "nombres": StringVar(),
        "apellidos": StringVar(),
        "email": StringVar(),
        "password": StringVar(),
        "confirmPassword": StringVar(),
        "dpi": StringVar(),
        "telefono": StringVar(),
        "direccion": StringVar(),
        "nacionalidad": StringVar(),
        "telefonoEmergencia": StringVar(),
        "nacimiento": StringVar(),
    }

    errorLabels = {}
    pages = []

    def createField(parent, labelText, varName, validatorFunc=None, errorMsg="", show=""):
        ttk.Label(parent, text=labelText).pack(anchor="w")
        entry = ttk.Entry(parent, textvariable=fields[varName], show=show)
        entry.pack(fill="x", pady=(0, 0))

        errorLabel = ttk.Label(parent, text="", font=("Helvetica", 8, "italic"), foreground="red")
        errorLabel.pack(anchor="w", pady=(0, 5))
        errorLabels[varName] = errorLabel

        if validatorFunc:
            def onFocusOut(event):
                value = fields[varName].get()
                if varName == "email":
                    valid, msg = validatorFunc(value)
                    if not valid:
                        errorLabel.config(text=msg)
                    else:
                        errorLabel.config(text="")
                else:
                    if not validatorFunc(value):
                        errorLabel.config(text=errorMsg)
                    else:
                        errorLabel.config(text="")
            entry.bind("<FocusOut>", onFocusOut)

    page1 = ttk.Frame(container)
    page2 = ttk.Frame(container)
    pages.extend([page1, page2])

    createField(page1, "Nombres:", "nombres", isNotEmpty, "Este campo no puede estar vacío")
    createField(page1, "Apellidos:", "apellidos", isNotEmpty, "Este campo no puede estar vacío")
    createField(page1, "Correo electrónico:", "email", isValidEmail, "Correo inválido")
    createField(page1, "Contraseña:", "password", isNotEmpty, "Este campo no puede estar vacío", show="*")
    createField(page1, "Confirmar contraseña:", "confirmPassword", isNotEmpty, "Este campo no puede estar vacío", show="*")

    def onConfirmPasswordFocusOut(event):
        pwd = fields["password"].get()
        conf = fields["confirmPassword"].get()
        if conf != pwd:
            errorLabels["confirmPassword"].config(text="Las contraseñas no coinciden")
        else:
            errorLabels["confirmPassword"].config(text="")

    confirmEntry = errorLabels["confirmPassword"].master.winfo_children()[1]
    confirmEntry.bind("<FocusOut>", onConfirmPasswordFocusOut)

    createField(page2, "DPI:", "dpi", isValidDpi, "DPI debe tener 13 dígitos")
    createField(page2, "Teléfono:", "telefono", isValidPhone, "Teléfono debe tener 8 dígitos")
    createField(page2, "Dirección:", "direccion", isNotEmpty, "Este campo no puede estar vacío")
    createField(page2, "Nacionalidad:", "nacionalidad", isNotEmpty, "Este campo no puede estar vacío")
    createField(page2, "Teléfono de Emergencia:", "telefonoEmergencia", isValidPhone, "Teléfono debe tener 8 dígitos")

    ttk.Label(page2, text="Fecha de Nacimiento (yyyy-mm-dd):").pack(anchor="w")
    fechaEntry = ttk.Entry(page2, textvariable=fields["nacimiento"])
    fechaEntry.pack(fill="x", pady=(0, 5))

    errorLabels["nacimiento"] = ttk.Label(page2, text="", font=("Helvetica", 8, "italic"), foreground="red")
    errorLabels["nacimiento"].pack(anchor="w", pady=(0, 5))

    def validateFecha(fecha):
        pattern = r"^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
        return re.match(pattern, fecha) is not None

    def onFechaFocusOut(event):
        valor = fields["nacimiento"].get()
        if not validateFecha(valor):
            errorLabels["nacimiento"].config(text="Fecha inválida. Formato: yyyy-mm-dd")
        else:
            errorLabels["nacimiento"].config(text="")

    fechaEntry.bind("<FocusOut>", onFechaFocusOut)

    navFrame = ttk.Frame(container)
    navFrame.pack(side="bottom", pady=10)

    def showPage(index):
        for page in pages:
            page.pack_forget()
        pages[index].pack(fill="both", expand=True)

    def validatePage(index):
        if index == 0:
            keys = ["nombres", "apellidos", "email", "password", "confirmPassword"]
        else:
            keys = ["dpi", "telefono", "direccion", "nacionalidad", "telefonoEmergencia", "nacimiento"]

        valid = True
        for key in keys:
            value = fields[key].get()
            entryValid = True
            if key == "email":
                entryValid, msg = isValidEmail(value)
                if not entryValid:
                    errorLabels[key].config(text=msg)
            elif key == "dpi":
                entryValid = isValidDpi(value)
            elif key in ["telefono", "telefonoEmergencia"]:
                entryValid = isValidPhone(value)
            elif key == "nacimiento":
                entryValid = validateFecha(value)
            else:
                entryValid = isNotEmpty(value)

            if not entryValid and key != "email":
                errorLabels[key].config(text="Campo inválido")
            elif key != "email":
                errorLabels[key].config(text="")

            if not entryValid:
                valid = False

        if index == 0 and not isSamePassword(fields["password"].get(), fields["confirmPassword"].get()):
            errorLabels["confirmPassword"].config(text="Las contraseñas no coinciden")
            valid = False
        return valid

    def nextPage():
        if validatePage(currentPage[0]):
            currentPage[0] += 1
            showPage(currentPage[0])
            nextBtn.pack_forget()
            registerBtn.grid(row=0, column=0, padx=(0, 6), pady=10)

    def handleRegister():
        if not validatePage(1):
            return

        data = {k: v.get().strip() for k, v in fields.items()}

        result = registerUser(
            data["nombres"], data["apellidos"], data["email"],
            data["password"], data["dpi"], data["telefono"],
            data["direccion"], data["nacimiento"], data["nacionalidad"],
            data["telefonoEmergencia"]
        )

        if result["success"]:
            messagebox.showinfo("Registrado", "El usuario se ha registrado exitosamente.")
            window.destroy()
        else:
            messagebox.showerror("Error", result["message"])

    nextBtn = ttk.Button(navFrame, text="Siguiente", style='confirm.TButton', command=nextPage)
    registerBtn = ttk.Button(navFrame, text="Registrarse", style='success.TButton', command=handleRegister)
    cancelBtn = ttk.Button(navFrame, text="Cancelar", style='danger.TButton', command=window.destroy)

    nextBtn.grid(row=0, column=0, padx=(0,6), pady=10)
    cancelBtn.grid(row=0, column=1, padx=(6, 0), pady=10)

    showPage(0)
