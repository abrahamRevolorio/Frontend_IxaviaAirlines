from nicegui import ui
import asyncio


from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import postToBackend, logout
from utils.validators import isNotEmpty, isValidEmail, isSamePassword, isValidDpi, isValidPhone, isValidAge


def createAgent():
    opcionesNavbar = [
        {
            'texto': 'Regresar',
            'onClickJs': "window.location.href = '/'",
            'clases': 'mx-2 py-2 px-6 rounded border border-[transparent] transition font-bold text-base hover:bg-[#1E4DBB] hover:text-[#F0F4FF]',
            'bgColor': "#002678",
            'textColor': '#F0F4FF'
        },
        {
            'texto': 'Logout',
            'onClickJs': "localStorage.clear(); window.location.href = '/'",
            'onClickPy': logout,
            'clases': 'mx-2 py-2 px-6 rounded border border-[#486142] transition font-bold text-base hover:bg-[#1E4DBB] hover:text-[#F0F4FF]',
            'bgColor': "#AA0000",
            'textColor': '#F0F4FF'
        }
    ]

    Navbar(opcionesNavbar)

    with ui.column().classes('w-full max-w-2xl mx-auto my-8 p-8 bg-white rounded-lg shadow-md'):
        ui.label('Agregar Nuevo Cliente').classes('text-2xl font-bold text-center mb-8 text-[#486142]')
        
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

        nit = ui.input(label='NIT').classes('w-full mb-2')
        error_nit = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        telefono = ui.input(label='Teléfono').classes('w-full mb-2')
        error_telefono = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        
        edad = ui.input(label='Edad').classes('w-full mb-2')
        error_edad = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')

        validation_states = {
            'nombres': False,
            'apellidos': False,
            'email': False,
            'password': False,
            'confirm_password': False,
            'dpi': False,
            'nit': False,
            'telefono': False,
            'edad': False
        }

        def validate_field(field, value, validator, error_label, error_msg=None, field_name=None):
            if validator == isValidEmail:
                valid, msg = validator(value)
                error_label.set_text('' if valid else (msg if msg else 'Correo inválido'))
            elif validator == isSamePassword:
                valid = validator(password.value, confirm_password.value)
                error_label.set_text('' if valid else 'Las contraseñas no coinciden')
            elif validator == isValidDpi:
                valid = validator(value)
                error_label.set_text('' if valid else 'DPI debe tener 13 dígitos')
            elif validator == isValidPhone:
                valid = validator(value)
                error_label.set_text('' if valid else 'Teléfono debe tener 8 dígitos')
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
        nit.on('blur', lambda: validate_field(nit, nit.value, isNotEmpty, error_nit, 'NIT debe tener 8 dígitos', 'nit'))
        edad.on('blur', lambda: validate_field(edad, edad.value, isValidAge, error_edad, 'Edad debe tener 2 dígitos', 'edad'))

        async def handle_register():
            global registroExitoso
            registroExitoso = None

            if not all(validation_states.values()):
                registroExitoso = 'validacion'
                return

            data = {
                'nombres': nombres.value.strip(),
                'apellidos': apellidos.value.strip(),
                'email': email.value.strip(),
                'password': password.value.strip(),
                'dpi': dpi.value.strip(),
                'telefono': telefono.value.strip(), 
                'nit': nit.value.strip(),
                'edad': int(edad.value.strip()),
                'rol': 'Agente'
            }

            try:
                response = await postToBackend('user/add', data)
                print(response)
                if response and response.get('success'):
                    registroExitoso = True
                else:
                    registroExitoso = 'fallo:' + response.get('message', 'Error desconocido')
            except Exception as e:
                registroExitoso = 'fallo:' + str(e)

        def on_register_click():
            asyncio.create_task(handle_register())

            def revisarResultado():
                global registroExitoso
                if registroExitoso is None:
                    return
                if registroExitoso == True:
                    ui.notify('Agente Creado', type='positive')
                    ui.timer(2.0, lambda: ui.run_javascript("window.location.href='/'"), once=True)
                elif registroExitoso == 'validacion':
                    ui.notify('Por favor corrige los errores en el formulario', type='negative')
                elif isinstance(registroExitoso, str) and registroExitoso.startswith('fallo:'):
                    mensaje = registroExitoso[6:]
                    ui.notify('Error en registro: ' + mensaje, type='negative')
                registroExitoso = None
                timer.clear()

            timer = ui.timer(0.1, revisarResultado)

        register_button = ui.button(
            'Agregar', 
            on_click=on_register_click
        ).props('w-full py-3 bg-[#486142] text-white font-bold rounded')

        register_button.disable()

    Footer()