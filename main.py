# main.py
from tkinter import Tk
from ttkbootstrap import Style
from views.loginView import showLoginView
from views.registerView import showRegisterView

def main():
    app = Tk()
    app.title("IXAVIA Airlines")
    app.state("zoomed")
    app.minsize(800, 600)

    style = Style("cosmo")
    style.master = app

    from ttkbootstrap.widgets import Label, Button
    from tkinter import CENTER

    Label(app, text="IXAVIA AIRLINES", font=("Helvetica", 30, "bold"), anchor=CENTER).pack(pady=50)

    Button(app, text="Iniciar sesión", bootstyle="primary", width=30, command=lambda: showLoginView(app)).pack(pady=10)
    Button(app, text="Registrarse", bootstyle="success", width=30, command=lambda: showRegisterView(app)).pack(pady=10)
    Button(app, text="Salir", bootstyle="danger", width=30, command=app.quit).pack(pady=30)

    app.mainloop()

if __name__ == "__main__":
    main()
