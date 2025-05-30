from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import getFromBackend

async def fetchFlightPeten():    
    try:
        response = await getFromBackend('flight/view/peten')
        print(response)
        if response and response.get('success') and response['data'].get('success'):
            return response['data'].get('flights_info', [])
        return []
    except Exception as e:
        ui.notify(f'Error al obtener los vuelos: {str(e)}', type='negative')
        return []

def viewFlightPeten():
    Navbar([
        {
            'texto': 'Regresar',
            'onClickJs': "window.location.href = '/'",
            'clases': '!mx-2 !py-2 !px-6 !rounded !border !transition !font-bold !text-base hover:!bg-[#1E4DBB] hover:!text-[#F0F4FF]',
            'bgColor': "#002678",
            'textColor': '#F0F4FF'
        }
    ])

    with ui.element('div').classes('!w-full !min-h-screen !bg-gray-50 !pt-20 !pb-16'):
        tableRef = None

        with ui.card().classes('!w-full !max-w-6xl !mx-auto !mt-8 !shadow-lg !rounded-lg !border !border-gray-200 !px-6'):
            ui.label('Listado de Vuelos Peten').classes('!text-2xl !font-bold !text-gray-800 !mb-4 text-center')

            tableRef = ui.table(
                columns=[
                    {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True, 'align': 'center'},
                    {'name': 'fecha', 'label': 'Fecha', 'field': 'fecha', 'sortable': True, 'align': 'center'},
                    {'name': 'hora_salida', 'label': 'Hora Salida', 'field': 'hora_salida', 'sortable': True, 'align': 'center'},
                    {'name': 'hora_llegada', 'label': 'Hora Llegada', 'field': 'hora_llegada', 'sortable': True, 'align': 'center'},
                    {'name': 'destino_id', 'label': 'Destino', 'field': 'destino_id', 'sortable': True, 'align': 'center'},
                    {'name': 'avion_id', 'label': 'Avión ID', 'field': 'avion_id', 'sortable': True, 'align': 'center'},
                ],
                rows=[],
                row_key='id',
                pagination={'rowsPerPage': 10}
            ).classes('!w-full text-center')

            async def cargarVuelos():
                data = await fetchFlightPeten()

                destinoMap = {
                    "1": "Guatemala",
                    "2": "Petén"
                }

                for vuelo in data:
                    destino_id = str(vuelo.get('destino_id', ''))
                    vuelo['destino_id'] = destinoMap.get(destino_id, f"ID {destino_id}")

                tableRef.rows = data

                statsRow.clear()
                with statsRow:
                    ui.label(f'Total Vuelos: {len(data)}')

            ui.button('Refrescar', icon='refresh', on_click=cargarVuelos).classes(
                '!bg-blue-600 !text-white hover:!bg-blue-700 !px-4 !py-2 !rounded !transition !my-4'
            )

        statsRow = ui.row().classes('!w-full !justify-end !space-x-4 !text-sm !text-gray-600 !px-4 !mt-2')

        ui.timer(0.1, cargarVuelos, once=True)

    Footer()
