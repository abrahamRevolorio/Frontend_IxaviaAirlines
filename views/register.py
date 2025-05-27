from nicegui import ui
from utils.apiClient import registerUser
from utils.validators import isNotEmpty, isValidEmail, isSamePassword, isValidDpi, isValidPhone
from components.navbar import Navbar
from components.footer import Footer
import asyncio
from datetime import datetime

def register():
    opcionesNavbar = [
        {
            'texto': 'Regresar',
            'navigate_to': '/',
            'clases': '!mx-1 !py-2 !px-6 !rounded !border !border-[#486142] !transition !font-bold !text-base !hover:bg-[#1E4DBB] !hover:text-[#F0F4FF]',
            'bgColor': "#AA0000",
            'textColor': '#F0F4FF'
        }
    ]

    Navbar(opcionesNavbar)

    with ui.column().classes('w-full max-w-2xl mx-auto my-8 p-8 bg-white rounded-lg shadow-md'):
        ui.label('Crear una Cuenta').classes('text-2xl font-bold text-center mb-8 text-[#486142]')
        
        nombres = ui.input(label='Nombres').classes('w-full mb-2')
        error_nombres = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        apellidos = ui.input(label='Apellidos').classes('w-full mb-2')
        error_apellidos = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        email = ui.input(label='Correo electrónico').classes('w-full mb-2')
        error_email = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        password = ui.input(label='Contraseña', password=True, password_toggle_button=True).classes('w-full mb-2')
        error_password = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        confirm_password = ui.input(label='Confirmar contraseña', password=True, password_toggle_button=True).classes('w-full mb-2')
        error_confirm = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        dpi = ui.input(label='DPI').classes('w-full mb-2')
        error_dpi = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        telefono = ui.input(label='Teléfono').classes('w-full mb-2')
        error_telefono = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        direccion = ui.input(label='Dirección').classes('w-full mb-2')
        error_direccion = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        nacionalidad = ui.input(label='Nacionalidad').classes('w-full mb-2')
        error_nacionalidad = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        telefono_emergencia = ui.input(label='Teléfono de Emergencia').classes('w-full mb-2')
        error_telefono_emergencia = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        nacimiento = ui.input(label='Fecha de Nacimiento (yyyy-mm-dd)').classes('w-full mb-2')
        error_nacimiento = ui.label('').classes('text-red-500 text-xs -mt-2 mb-6')

        def validate_fecha(fecha):
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
                return True
            except ValueError:
                return False

        def validate_field(field, value, validator, error_label, error_msg=None):
            if validator == isValidEmail:
                valid, msg = validator(value)
                error_label.set_text('' if valid else (msg if msg else 'Correo inválido'))
            elif validator == isSamePassword:
                valid = validator(password.value, confirm_password.value)
                error_label.set_text('' if valid else 'Las contraseñas no coinciden')
            else:
                valid = validator(value)
                error_label.set_text('' if valid else (error_msg if error_msg else 'Campo inválido'))
            return valid

        nombres.on('blur', lambda: validate_field(nombres, nombres.value, isNotEmpty, error_nombres, 'Este campo no puede estar vacío'))
        apellidos.on('blur', lambda: validate_field(apellidos, apellidos.value, isNotEmpty, error_apellidos, 'Este campo no puede estar vacío'))
        email.on('blur', lambda: validate_field(email, email.value, isValidEmail, error_email))
        password.on('blur', lambda: validate_field(password, password.value, isNotEmpty, error_password, 'Este campo no puede estar vacío'))
        confirm_password.on('blur', lambda: validate_field(confirm_password, confirm_password.value, isSamePassword, error_confirm))
        dpi.on('blur', lambda: validate_field(dpi, dpi.value, isValidDpi, error_dpi, 'DPI debe tener 13 dígitos'))
        telefono.on('blur', lambda: validate_field(telefono, telefono.value, isValidPhone, error_telefono, 'Teléfono debe tener 8 dígitos'))
        direccion.on('blur', lambda: validate_field(direccion, direccion.value, isNotEmpty, error_direccion, 'Este campo no puede estar vacío'))
        nacionalidad.on('blur', lambda: validate_field(nacionalidad, nacionalidad.value, isNotEmpty, error_nacionalidad, 'Este campo no puede estar vacío'))
        telefono_emergencia.on('blur', lambda: validate_field(telefono_emergencia, telefono_emergencia.value, isValidPhone, error_telefono_emergencia, 'Teléfono debe tener 8 dígitos'))
        nacimiento.on('blur', lambda: error_nacimiento.set_text('' if validate_fecha(nacimiento.value) else 'Fecha inválida. Formato: yyyy-mm-dd'))

        async def handle_register():
            valid = True
            
            if not validate_field(nombres, nombres.value, isNotEmpty, error_nombres, 'Este campo no puede estar vacío'):
                valid = False
            if not validate_field(apellidos, apellidos.value, isNotEmpty, error_apellidos, 'Este campo no puede estar vacío'):
                valid = False
            if not validate_field(email, email.value, isValidEmail, error_email):
                valid = False
            if not validate_field(password, password.value, isNotEmpty, error_password, 'Este campo no puede estar vacío'):
                valid = False
            if not validate_field(confirm_password, confirm_password.value, isSamePassword, error_confirm):
                valid = False
            if not validate_field(dpi, dpi.value, isValidDpi, error_dpi, 'DPI debe tener 13 dígitos'):
                valid = False
            if not validate_field(telefono, telefono.value, isValidPhone, error_telefono, 'Teléfono debe tener 8 dígitos'):
                valid = False
            if not validate_field(direccion, direccion.value, isNotEmpty, error_direccion, 'Este campo no puede estar vacío'):
                valid = False
            if not validate_field(nacionalidad, nacionalidad.value, isNotEmpty, error_nacionalidad, 'Este campo no puede estar vacío'):
                valid = False
            if not validate_field(telefono_emergencia, telefono_emergencia.value, isValidPhone, error_telefono_emergencia, 'Teléfono debe tener 8 dígitos'):
                valid = False
            if not validate_fecha(nacimiento.value):
                error_nacimiento.set_text('Fecha inválida. Formato: yyyy-mm-dd')
                valid = False
            
            if not valid:
                ui.notify('Por favor corrige los errores en el formulario', type='negative')
                return
            
            result = registerUser(
                nombres.value.strip(),
                apellidos.value.strip(),
                email.value.strip(),
                password.value.strip(),
                dpi.value.strip(),
                telefono.value.strip(),
                direccion.value.strip(),
                nacimiento.value.strip(),
                nacionalidad.value.strip(),
                telefono_emergencia.value.strip()
            )
            
            if result.get('success'):
                ui.notify('Registro exitoso!', type='positive')
                await asyncio.sleep(2)
                ui.run_javascript("window.location.href='/'")
            else:
                ui.notify(result.get('message', 'Error al registrar usuario'), type='negative')

        ui.button('Registrarse', on_click=handle_register).classes('w-full py-2 bg-[#486142] text-white hover:bg-[#3a4d36] transition')

    Footer()