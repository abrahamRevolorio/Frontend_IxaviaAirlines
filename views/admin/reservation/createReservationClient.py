from nicegui import ui
from utils.apiClient import getFromBackend, postToBackend
from components.navbar import Navbar
from components.footer import Footer
import asyncio

async def fetchFlight():
    response = await getFromBackend('flight/view')
    if response and response.get('success') and response['data'].get('success'):
        return response['data'].get('flights_info', [])
    return []

async def createReservationClient():
    selectedFlightId = None

    Navbar([
        {'texto': 'Regresar', 'onClickJs': "window.location.href = '/'", 'clases': 'mx-2 py-2 px-6 rounded', 'bgColor': "#002678", 'textColor': '#F0F4FF'},
        {'texto': 'Logout', 'onClickJs': "localStorage.clear(); window.location.href = '/'", 'onClickPy': lambda: print("logout"), 'clases': 'mx-2 py-2 px-6 rounded', 'bgColor': "#AA0000", 'textColor': '#F0F4FF'}
    ])

    with ui.column().classes('items-center justify-center w-full'):
        container = ui.column().classes('w-full max-w-3xl bg-white p-8 my-8 rounded-lg shadow-md items-center')

        tabla = await crearTablaSeleccionarVuelo(container)

        async def seleccionarAsiento(flight_id):
            nonlocal selectedFlightId
            selectedFlightId = flight_id
            container.clear()
            with container:
                ui.label(f'🛫 Vuelo seleccionado: ID {flight_id}').classes('text-xl font-bold mb-6 text-blue-800 text-center')

        def onFlightSelected(flight_id):
            ui.notify(f'Vuelo seleccionado: {flight_id}', type='positive')
            asyncio.create_task(seleccionarAsiento(flight_id))

        await tabla(onFlightSelected)

        ui.separator().classes('my-6 w-full')

        ui.label('✈️ Asientos').classes('text-2xl font-bold mb-4 text-blue-900 text-center')

        with ui.row().classes('w-full justify-center items-center gap-4'):
            dropdownDestino = ui.select(
                {
                    1: 'A1', 2: 'A2', 3: "A3",
                    4: "B1", 5: "B2", 6: "B3",
                    7: "C1", 8: "C2", 9: "C3",
                    10: "D1", 11: "D2", 12: "D3",
                    13: "E1", 14: "E2", 15: "E3",
                    16: "F1", 17: "F2", 18: "F3"
                },
                label='Selecciona tu asiento',
                with_input=True
            ).classes('w-64')

        ui.button('Reservar', on_click=lambda: addReservation(dropdownDestino, selectedFlightId)) \
            .classes('bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 mt-6')

    Footer()

async def addReservation(dropdownDestino, selectedFlightId):
    data = {
        'asiento_id': dropdownDestino.value,
        'vuelo_id': selectedFlightId
    }

    try:
        response = await postToBackend('reservation/create/client', data)

        if response:
            if response.get("data", {}).get("success"):
                ui.notify('Vuelo creado exitosamente', type='positive')
                ui.timer(2.0, lambda: ui.run_javascript("window.location.href='/'"), once=True)
            else:
                mensaje = response.get("data", {}).get("message", "Error desconocido")
                ui.notify(f'Error al crear el vuelo: {mensaje}', type='negative')
        else:
            ui.notify("No se recibió respuesta del servidor", type='negative')

    except Exception as e:
        ui.notify(f'Error inesperado: {str(e)}', type='negative')

async def crearTablaSeleccionarVuelo(container):
    async def mostrarTabla(onSelected):
        vuelos = await fetchFlight()
        destinoMap = {"1": "Guatemala", "2": "Petén"}

        for vuelo in vuelos:
            destino_id = str(vuelo.get('destino_id', ''))
            vuelo['destino_id'] = destinoMap.get(destino_id, f"ID {destino_id}")

        with container:
            ui.label('✈️ Selecciona un vuelo').classes('text-2xl font-bold mb-6 text-center text-blue-900')

            for vuelo in vuelos:
                with ui.row().classes('items-center justify-between w-full border p-4 rounded shadow mb-4'):
                    ui.label(f"{vuelo['fecha']} | {vuelo['hora_salida']} - {vuelo['hora_llegada']} | Destino: {vuelo['destino_id']}").classes('text-md text-gray-800')
                    ui.button('Seleccionar', on_click=lambda v=vuelo['id']: onSelected(v)) \
                        .classes('bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700')

    return mostrarTabla
