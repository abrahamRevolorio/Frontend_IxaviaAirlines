from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import logout, putToBackend
from utils.validators import isNotEmpty

def editFlight():
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

    ui.label('Editar Información del Vuelo').classes('!text-2xl !font-bold !mb-4 !mt-8')

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

        vueloid_input = ui.input('ID del Vuelo').classes('w-full mb-1')

        with ui.column().classes('w-full mb-2'):
            ui.label('Fecha De Vuelo')
            with ui.input() as fecha:
                with ui.menu().props('no-parent-event') as menu:
                    with ui.date().bind_value(fecha):
                        with ui.row().classes('justify-end'):
                            ui.button('Cerrar', on_click=menu.close).props('flat')
                with fecha.add_slot('append'):
                    ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')

        with ui.input('Hora salida') as horaSalidaInput:
            with ui.menu().props('no-parent-event') as menu:
                with ui.time().bind_value(horaSalidaInput):
                    with ui.row().classes('justify-end'):
                        ui.button('Cerrar', on_click=menu.close).props('flat')
            with horaSalidaInput.add_slot('append'):
                ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')

        with ui.input('Hora Llegada') as horaLlegadaInput:
            with ui.menu().props('no-parent-event') as menu:
                with ui.time().bind_value(horaLlegadaInput):
                    with ui.row().classes('justify-end'):
                        ui.button('Cerrar', on_click=menu.close).props('flat')
            with horaLlegadaInput.add_slot('append'):
                ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')

        with ui.row():
            dropdownDestino = ui.select(
                {1: 'Guatemala', 2: 'Peten'},
                label='Destino',
                with_input=True
            )

        with ui.row():
            dropdownAvion = ui.select(
                {1: 'Avion TG-IxaI', 2: 'Avion TG-IxaII'},
                label='Avión',
                with_input=True
            )

        async def guardar_cambios():
            data = {'vueloid': int(vueloid_input.value.strip())}

            if fecha.value and fecha.value != '':
                data['fecha'] = str(fecha.value)

            if horaSalidaInput.value and horaSalidaInput.value != '':
                data['hora_salida'] = f'{horaSalidaInput.value}:00'

            if horaLlegadaInput.value and horaLlegadaInput.value != '':
                data['hora_llegada'] = f'{horaLlegadaInput.value}:00'

            if dropdownDestino.value:
                data['destino_id'] = dropdownDestino.value

            if dropdownAvion.value:
                data['avion_id'] = dropdownAvion.value

            response = await putToBackend('flight/update', data)

            print(response)

            if response:
                if response.get('data').get('success') == False:
                    ui.notify(f'Error: {response.get("data").get("message")}', type='negative')
                else:
                    ui.notify('Vuelo actualizado correctamente', type='positive')
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
        )

    Footer()