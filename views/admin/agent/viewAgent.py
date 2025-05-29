from nicegui import ui
from datetime import datetime
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import logout, getFromBackend

async def fetchAgente():
    try:
        response = await getFromBackend('user/view')
        if response and response.get('success'):
            empleados = response.get('data', {}).get('empleados', [])
            return [
                {
                    **empleado['empleado'],
                    'email': empleado['user']['email'],
                    'estado': empleado['user']['estado'],
                    'rol_id': empleado['user']['rol_id'],
                    'usuario_id': empleado['user']['usuario_id'],
                    'fecharegistro': datetime.now().strftime('%Y-%m-%d')
                }
                for empleado in empleados
            ]
        return []
    except Exception as e:
        ui.notify(f'Error al obtener los empleados: {str(e)}', type='negative')
        return []

def viewAgent():
    Navbar([
        {
            'texto': 'Regresar',
            'onClickJs': "window.location.href = '/'",
            'clases': '!mx-2 !py-2 !px-6 !rounded !border !transition !font-bold !text-base hover:!bg-[#1E4DBB] hover:!text-[#F0F4FF]',
            'bgColor': "#002678",
            'textColor': '#F0F4FF'
        },
        {
            'texto': 'Logout',
            'onClickJs': "localStorage.clear(); window.location.href = '/'",
            'onClickPy': logout,
            'clases': '!mx-2 !py-2 !px-6 !rounded !border !transition !font-bold !text-base hover:!bg-[#1E4DBB] hover:!text-[#F0F4FF]',
            'bgColor': "#AA0000",
            'textColor': '#F0F4FF'
        }
    ])

    with ui.element('div').classes('!w-full !min-h-screen !bg-gray-50 !pt-20 !pb-16'):
        tableRef = None

        with ui.card().classes('!w-full !max-w-7xl !mx-auto !mt-8 !shadow-lg !rounded-lg !border !border-gray-200') as card:
            ui.label('Listado de Empleados').classes('!text-2xl !font-bold !text-gray-800 !mb-4')

            tableRef = ui.table(
                columns=[
                    {'name': 'usuario_id', 'label': 'ID', 'field': 'usuario_id', 'sortable': True},
                    {'name': 'nombre', 'label': 'Nombre', 'field': 'nombre', 'sortable': True},
                    {'name': 'apellido', 'label': 'Apellido', 'field': 'apellido'},
                    {'name': 'email', 'label': 'Email', 'field': 'email'},
                    {'name': 'dpi', 'label': 'DPI', 'field': 'dpi'},
                    {'name': 'telefono', 'label': 'Teléfono', 'field': 'telefono'},
                    {'name': 'edad', 'label': 'Edad', 'field': 'edad'},
                    {'name': 'estado', 'label': 'Estado', 'field': 'estado'},
                    {'name': 'fecha_registro', 'label': 'Registro', 'field': 'fecha_registro'}
                ],
                rows=[],
                row_key='usuario_id',
                pagination={'rowsPerPage': 10}
            ).classes('!w-full')

            async def cargarAgente():
                data = await fetchAgente()
                tableRef.rows = data
                statsRow.clear()
                with statsRow:
                    ui.label(f'Total Agentes: {len(data)}')
                    ui.label(f'Activos: {sum(1 for c in data if c["estado"] == "activo")}')
                    ui.label(f'Inactivos: {sum(1 for c in data if c["estado"] == "inactivo")}')
            
            ui.button('Refrescar', icon='refresh', on_click=cargarAgente).classes(
                '!bg-blue-600 !text-white hover:!bg-blue-700 !px-4 !py-2 !rounded !transition !my-4'
            )

        statsRow = ui.row().classes('!w-full !justify-end !space-x-4 !text-sm !text-gray-600 !px-4 !mt-2')

        ui.timer(0.1, cargarAgente, once=True)

    Footer()