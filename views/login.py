from nicegui import ui, app
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
                margin: 0;
                height: 100%;
                overflow: auto !important;
                background-color: #f7f9fb;
            }
            .content-wrapper {
                display: flex !important;
                flex-direction: column;
                justify-content: center !important;
                align-items: center !important;
                text-align: center;
                min-height: calc(100vh - 180px);
                padding: 20px 20px 60px 20px;
                width: 100%;
                box-sizing: border-box;
            }
            /* Centrar los labels de los inputs */
            .content-wrapper label {
                display: block;
                width: 100%;
                text-align: center !important;
            }
        </style>
    ''')

    with ui.row().classes('content-wrapper w-full h-full justify-center items-center'):
        with ui.column().classes(
            'max-w-2xl w-full bg-white mx-auto self-center rounded-xl shadow-md p-10 gap-y-5 border border-gray-200'
        ):
            ui.label('Iniciar sesión').classes('text-3xl font-bold mb-4 text-center text-gray-800')

            email_input = ui.input(label='Correo electrónico', placeholder='ejemplo@correo.com')\
                .classes('w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 focus:border-transparent')

            email_error = ui.label('').classes('text-red-600 text-sm').style('min-height: 1.25rem')

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

            password_error = ui.label('').classes('text-red-600 text-sm').style('min-height: 1.25rem')

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

                    token = result.get('accessToken')

                    ui.run_javascript(f'localStorage.setItem("accessToken", "{token}");')

                    ui.notify(f"¡Bienvenido {result.get('nombre', '')}!", color='green')
                    await asyncio.sleep(2)

                    if result.get('rol') == 'Agente':
                        ui.run_javascript("window.location.href='/agente'")
                    elif result.get('rol') == 'Administrador':
                        ui.run_javascript("window.location.href='/admin'")
                    elif result.get('rol') == 'Cliente':
                        ui.run_javascript("window.location.href='/cliente'")
                    else:
                        ui.notify('Rol no reconocido', color='red')
                        
                else:
                    ui.notify(result.get('message', 'Error al iniciar sesión.'), color='red')

            ui.button(
                'Entrar',
                on_click=on_submit
            ).classes(
                'w-full bg-[#008020!important] text-[#F0F4FF!important] text-[18px!important] font-semibold py-[14px!important] px-[24px!important] rounded-md hover:bg-[#006414!important] transition mt-2'
            )

            ui.html('¿No tienes cuenta? <a href="/register" class="text-[#1E4DBB] hover:underline ml-1">Regístrate</a>')\
                .classes('mt-6 text-center text-sm text-gray-700')

    Footer()