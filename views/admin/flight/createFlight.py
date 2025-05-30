from nicegui import ui
import asyncio
from datetime import datetime

from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import postToBackend, logout

def createFlight():
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
        ui.label('Agregar Nuevo Vuelo').classes('text-2xl font-bold text-center mb-8 text-[#486142]')

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

        async def handle_register():
            if not fecha.value or not horaSalidaInput.value or not horaLlegadaInput.value or not dropdownDestino.value or not dropdownAvion.value:
                ui.notify('Por favor llena todos los campos', type='negative')
                return

            data = {
                'fecha': fecha.value if isinstance(fecha.value, str) else str(fecha.value),
                'hora_salida': f'{horaSalidaInput.value}:00',
                'hora_llegada': f'{horaLlegadaInput.value}:00',
                'destino_id': dropdownDestino.value,
                'avion_id': dropdownAvion.value
            }

            try:
                response = await postToBackend('flight/add', data)
                if response:
                    if response.get('data').get('success'):
                        ui.notify('Vuelo creado exitosamente', type='positive')
                        ui.timer(2.0, lambda: ui.run_javascript("window.location.href='/'"), once=True)
                    else:
                        ui.notify(f'Error al crear el vuelo: {response.get("data").get("message")}', type='negative')
                else:
                    ui.notify(f'Error al crear el vuelo: {response.get("message")}', type='negative')
            except Exception as e:
                ui.notify(f'Excepción: {e}', type='negative')

        register_button = ui.button(
            'Agregar',
            on_click=handle_register
        ).props('w-full py-3 bg-[#486142] text-white font-bold rounded')

    Footer()
