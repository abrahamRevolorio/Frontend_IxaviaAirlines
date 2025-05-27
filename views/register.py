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

        validation_states = {
            'nombres': False,
            'apellidos': False,
            'email': False,
            'password': False,
            'confirm_password': False,
            'dpi': False,
            'telefono': False,
            'direccion': False,
            'nacionalidad': False,
            'telefono_emergencia': False,
            'nacimiento': False
        }

        def validate_fecha(fecha):
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
                return True
            except ValueError:
                return False

        def validate_field(field, value, validator, error_label, error_msg=None, field_name=None):
            if validator == isValidEmail:
                valid, msg = validator(value)
                error_label.set_text('' if valid else (msg if msg else 'Correo inválido'))
            elif validator == isSamePassword:
                valid = validator(password.value, confirm_password.value)
                error_label.set_text('' if valid else 'Las contraseñas no coinciden')
            else:
                valid = validator(value)
                error_label.set_text('' if valid else (error_msg if error_msg else 'Campo inválido'))
            
            if field_name:
                validation_states[field_name] = valid
                update_register_button_state()
            
            return valid

        def update_register_button_state():
            all_valid = all(validation_states.values())
            register_button.enabled = all_valid

        nombres.on('blur', lambda: validate_field(nombres, nombres.value, isNotEmpty, error_nombres, 'Este campo no puede estar vacío', 'nombres'))
        apellidos.on('blur', lambda: validate_field(apellidos, apellidos.value, isNotEmpty, error_apellidos, 'Este campo no puede estar vacío', 'apellidos'))
        email.on('blur', lambda: validate_field(email, email.value, isValidEmail, error_email, field_name='email'))
        password.on('blur', lambda: validate_field(password, password.value, isNotEmpty, error_password, 'Este campo no puede estar vacío', 'password'))
        confirm_password.on('blur', lambda: validate_field(confirm_password, confirm_password.value, isSamePassword, error_confirm, field_name='confirm_password'))
        dpi.on('blur', lambda: validate_field(dpi, dpi.value, isValidDpi, error_dpi, 'DPI debe tener 13 dígitos', 'dpi'))
        telefono.on('blur', lambda: validate_field(telefono, telefono.value, isValidPhone, error_telefono, 'Teléfono debe tener 8 dígitos', 'telefono'))
        direccion.on('blur', lambda: validate_field(direccion, direccion.value, isNotEmpty, error_direccion, 'Este campo no puede estar vacío', 'direccion'))
        nacionalidad.on('blur', lambda: validate_field(nacionalidad, nacionalidad.value, isNotEmpty, error_nacionalidad, 'Este campo no puede estar vacío', 'nacionalidad'))
        telefono_emergencia.on('blur', lambda: validate_field(telefono_emergencia, telefono_emergencia.value, isValidPhone, error_telefono_emergencia, 'Teléfono debe tener 8 dígitos', 'telefono_emergencia'))
        nacimiento.on('blur', lambda: 
            (error_nacimiento.set_text('' if validate_fecha(nacimiento.value) else 'Fecha inválida. Formato: yyyy-mm-dd'),
             validation_states.update({'nacimiento': validate_fecha(nacimiento.value)}),
             update_register_button_state())
        )

        async def handle_register():
            if not all(validation_states.values()):
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

        register_button = ui.button('Registrarse', on_click=handle_register).classes('!w-full !py-2 !bg-[#486142] !text-white !hover:bg-[#3a4d36] !transition')
        register_button.enabled = False

    Footer()