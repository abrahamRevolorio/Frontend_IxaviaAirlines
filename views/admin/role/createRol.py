from nicegui import ui
import asyncio


from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import postToBackend, logout
from utils.validators import isNotEmpty


def createRole():
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
        ui.label('Agregar Nuevo Role').classes('text-2xl font-bold text-center mb-8 text-[#486142]')
        
        nombreRol = ui.input(label='Nombre Rol').classes('w-full mb-2')
        error_nombreRol = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')

        validation_states = {
            'nombreRol': False
        }

        def validate_field(field, value, validator, error_label, error_msg=None, field_name=None):
            if validator == isNotEmpty:
                valid = validator(value)
                error_label.set_text('' if valid else 'Este campo no puede estar vacío')
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

        nombreRol.on('blur', lambda: validate_field(nombreRol, nombreRol.value, isNotEmpty, error_nombreRol, 'Este campo no puede estar vacío', 'nombreRol'))

        async def handle_register():
            global registroExitoso
            registroExitoso = None

            if not all(validation_states.values()):
                registroExitoso = 'validacion'
                return

            data = {
                'nombrerol': nombreRol.value.strip()
            }

            try:
                response = await postToBackend('role/add', data)
                if response and response.get('success'):
                    registroExitoso = True
                else:
                    registroExitoso = f'fallo {response.get('message', 'Error desconocido')}'
            except Exception as e:
                registroExitoso = 'fallo:' + str(e)

        def on_register_click():
            asyncio.create_task(handle_register())

            def revisarResultado():
                global registroExitoso
                if registroExitoso is None:
                    return
                if registroExitoso == True:
                    ui.notify('Role Creado', type='positive')
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