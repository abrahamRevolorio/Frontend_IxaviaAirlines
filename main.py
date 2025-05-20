from tkinter import Tk, Frame
from ttkbootstrap import Style
from ttkbootstrap.widgets import Label, Button
from tkinter import CENTER
from views.loginView import showLoginView
from views.registerView import showRegisterView

def main():
    app = Tk()
    app.title("IXAVIA AIRLINES - UMES")
    app.state("zoomed")
    app.minsize(800, 600)

    style = Style("darkly")
    style.theme_use("darkly")
    
    style.configure('.', background='#1a2e1a')
    style.configure('primary.TButton', background='#2d5a2d', foreground='white')
    style.configure('success.TButton', background='#3a7a3a', foreground='white')
    style.configure('danger.TButton', background='#5a2d2d', foreground='white')
    style.configure('confirm.TButton', background="#003272", foreground='white')
    style.configure('login.TButton', background="#046be0", foreground='white')

    style.master = app

    main_frame = Frame(app)
    main_frame.pack(pady=100, padx=50, fill='both', expand=True)

    Label(
        main_frame, 
        text="IXAVIA AIRLINES", 
        font=("Helvetica", 36, "bold"),
        foreground='#6dbd6d'
    ).pack(pady=(0, 20))

    Label(
        main_frame, 
        text="Sistema de Gestión de Vuelos - UMES", 
        font=("Helvetica", 14),
        foreground='#aaaaaa'
    ).pack(pady=(0, 50))

    button_frame = Frame(main_frame)
    button_frame.pack(pady=20)

    topButtonFrame = Frame(button_frame)
    topButtonFrame.pack()

    btn1 = Button(
        topButtonFrame,
        text="INICIAR SESIÓN",
        style='confirm.TButton',
        command=lambda: showLoginView(app),
        width=35,
        padding=(10,20)
    )
    
    btn1.pack(side="left", padx=10)

    btn2 = Button(
        topButtonFrame,
        text="REGISTRARSE",
        style='login.TButton',
        command=lambda: showRegisterView(app),
        width=35,
        padding=(10,20)
    )
    
    btn2.pack(side="left", padx=10)

    btn3 = Button(
        button_frame,
        text="SALIR",
        style='danger.TButton',
        command=app.quit,
        width=35,
        padding=(10,20)
    )
    
    btn3.pack(pady=30)



    footer_frame = Frame(app)
    footer_frame.pack(side='bottom', pady=20)
    
    Label(
        footer_frame,
        text="© 2025 IXAVIA Airlines - Proyecto académico de la Universidad Mesoamericana",
        font=("Helvetica", 9),
        foreground='#aaaaaa'
    ).pack()

    app.mainloop()

if __name__ == "__main__":
    main()