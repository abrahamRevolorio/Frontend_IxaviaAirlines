from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import getFromBackend
import asyncio

async def fetchReservation():
    try:
        response = await getFromBackend('view/client')
        print(response)
        if response and response.get('success') and response['data'].get('success'):
            return response['data'].get('reservation_info', [])
        return []
    except Exception as e:
        ui.notify(f'Error al obtener las reservaciones: {str(e)}', type='negative')
        return []

async def viewReservation():
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

        with ui.card().classes('!w-full !max-w-4xl !mx-auto !mt-8 !shadow-lg !rounded-lg !border !border-gray-200 !px-6'):
            ui.label('Tus Reservaciones').classes('!text-2xl !font-bold !text-gray-800 !mb-4 text-center')

            tableRef = ui.table(
                columns=[
                    {'name': 'vuelo_id', 'label': 'Vuelo ID', 'field': 'vuelo_id', 'sortable': True, 'align': 'center'},
                    {'name': 'asiento_id', 'label': 'Asiento ID', 'field': 'asiento_id', 'sortable': True, 'align': 'center'},
                    {'name': 'cliente_id', 'label': 'Cliente ID', 'field': 'cliente_id', 'sortable': True, 'align': 'center'},
                ],
                rows=[],
                row_key='asiento_id',
                pagination={'rowsPerPage': 10}
            ).classes('!w-full text-center')

            async def cargarReservaciones():
                data = await fetchReservation()
                tableRef.rows = data

                statsRow.clear()
                with statsRow:
                    ui.label(f'Total Reservaciones: {len(data)}')

            ui.button('Refrescar', icon='refresh', on_click=cargarReservaciones).classes(
                '!bg-blue-600 !text-white hover:!bg-blue-700 !px-4 !py-2 !rounded !transition !my-4'
            )

        statsRow = ui.row().classes('!w-full !justify-end !space-x-4 !text-sm !text-gray-600 !px-4 !mt-2')

        ui.timer(0.1, lambda: asyncio.create_task(cargarReservaciones()), once=True)

    Footer()