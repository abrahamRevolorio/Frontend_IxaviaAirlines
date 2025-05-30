from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import logout, putToBackend
from utils.validators import isNotEmpty

def editRole():
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
            'clases': 'mx-2 py-2 px-6 rounded border-[#486142] transition font-bold text-base hover:bg-[#1E4DBB] hover:text-[#F0F4FF]',
            'bgColor': "#AA0000",
            'textColor': '#F0F4FF'
        }
    ]

    Navbar(opcionesNavbar)

    ui.label('Editar Información del Rol').classes('!text-2xl !font-bold !mb-4 !mt-8')

    with ui.card().classes('max-w-xl w-full mx-auto p-6 shadow-lg'):
        validation_states = {
            'rolid': False,
            'nuevonombrerol': False
        }

        error_labels = {}

        def validate_field(field, value, validator, error_label, error_msg, key):
            valid = validator(value)
            error_label.set_text('' if valid else error_msg)
            validation_states[key] = valid
            update_save_button_state()

        def update_save_button_state():
            guardar_btn.enabled = all(validation_states.values())

        rolid_input = ui.input('ID del Rol').classes('w-full mb-1')
        error_labels['rolid'] = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')

        nuevonombrerol_input = ui.input('Nuevo Nombre del Rol').classes('w-full mb-1')
        error_labels['nuevonombrerol'] = ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')

        rolid_input.on('blur', lambda: validate_field(
            rolid_input, rolid_input.value, isNotEmpty, error_labels['rolid'], 'Este campo no puede estar vacío', 'rolid'
        ))

        nuevonombrerol_input.on('blur', lambda: validate_field(
            nuevonombrerol_input, nuevonombrerol_input.value, isNotEmpty, error_labels['nuevonombrerol'], 'Este campo no puede estar vacío', 'nuevonombrerol'
        ))

        async def guardar_cambios():
            data = {
                "rolid": rolid_input.value.strip(),
                "nuevonombrerol": nuevonombrerol_input.value.strip()
            }

            guardar_btn.props('disable')
            response = await putToBackend('role/update', data)

            print(response)

            if response:
                if response.get('data').get('success') == False:
                    ui.notify('El rol no existe', type='negative')
                else:
                    ui.notify('Rol actualizado correctamente', type='positive')
                    ui.run_javascript("setTimeout(() => window.location.href = '/', 2000)")
            else:
                msg = response.get('message', 'Error al actualizar') if response else 'Error en la conexión'
                errors = response.get('errors') if response else None
                if errors:
                    msg += ": " + ", ".join(errors)
                ui.notify(msg, type='negative')

            guardar_btn.props(remove='disable')

        guardar_btn = ui.button('Guardar Cambios', on_click=guardar_cambios).classes(
            '!bg-[#002678] !text-white !font-bold !py-2 !px-6 !rounded mt-4'
        ).props('disable')

    Footer()