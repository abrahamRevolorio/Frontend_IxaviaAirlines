from nicegui import ui
from utils.apiClient import loginUser
from utils.validators import isNotEmpty, isValidEmail
from components.navbar import Navbar
from components.footer import Footer
import asyncio

def login():
    opcionesNavbar = [
        {
            'texto': 'Regresar',
            'navigate_to': '/',
            'clases': 'mx-2 py-2 px-6 rounded border border-[#486142] transition font-bold text-base hover:bg-[#1E4DBB] hover:text-[#F0F4FF]',
            'bgColor': "#AA0000",
            'textColor': '#F0F4FF'
        }
    ]
    Navbar(opcionesNavbar)

    ui.add_head_html('''
        <style>
            html, body {
                height: 100%;
                margin: 0;
                overflow: hidden;
            }
            .no-scroll {
                height: calc(100vh - 120px);
                overflow: hidden;
            }
        </style>
    ''')

    with ui.row().classes('no-scroll bg-transparent w-full items-center justify-center'):
        with ui.column().classes('max-w-md w-full bg-transparent rounded-lg shadow-lg p-10 items-center'):
            ui.label('Iniciar sesión').classes('text-3xl font-bold mb-6 text-center text-gray-900')

            email_input = ui.input(label='Correo electrónico', placeholder='ejemplo@correo.com')\
                .classes('w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 focus:border-transparent')

            email_error = ui.label('').classes('text-red-600 text-sm mt-1').style('min-height: 1.25rem')

            def validate_email():
                email = email_input.value or ''
                if not isNotEmpty(email):
                    email_error.text = 'El correo no puede estar vacío.'
                else:
                    valid, msg = isValidEmail(email)
                    email_error.text = '' if valid else msg

            email_input.on('blur', validate_email)

            password_input = ui.input(label='Contraseña', placeholder='********', password=True)\
                .classes('w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 focus:border-transparent')

            password_error = ui.label('').classes('text-red-600 text-sm mt-1').style('min-height: 1.25rem')

            def validate_password():
                password = password_input.value or ''
                password_error.text = '' if isNotEmpty(password) else 'La contraseña no puede estar vacía.'

            password_input.on('blur', validate_password)

            async def on_submit():

                validate_email()
                validate_password()

                if email_error.text or password_error.text:
                    return

                result = loginUser(email_input.value, password_input.value)

                if result.get('success'):
                    ui.notify(f"¡Bienvenido {result.get('nombre', '')}!", color='green')
                    await asyncio.sleep(2)
                    ui.run_javascript("window.location.href='/'")
                else:
                    ui.notify(result.get('message', 'Error al iniciar sesión.'), color='red')

            with ui.row().classes('w-full justify-center'):
                ui.button(
                    'Entrar',
                    on_click=on_submit
                ).classes(
                    'bg-[#008020!important] text-[#F0F4FF!important] text-[18px!important] font-semibold py-[14px!important] px-[24px!important] rounded-md hover:bg-[#006414!important] transition mt-4'
                )

            with ui.row().classes('mt-6 justify-between text-gray-700 text-sm'):
                ui.label('¿No tienes cuenta?')
                ui.link('Regístrate', '/register').classes('hover:underline')

    Footer()
