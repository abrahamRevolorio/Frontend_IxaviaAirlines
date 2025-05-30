from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import logout, getFromBackend

async def fetchRoles():    
    try:
        response = await getFromBackend('role/view')
        print(response)
        if response and response.get('success') and response['data'].get('success'):
            roles = response['data'].get('roles', {})
            return [
                {"rolid": int(rolId), "nombrerol": nombre}
                for rolId, nombre in roles.items()
            ]
        return []
    except Exception as e:
        ui.notify(f'Error al obtener los roles: {str(e)}', type='negative')
        return []

def viewRole():
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

        with ui.card().classes('!w-full !max-w-4xl !mx-auto !mt-8 !shadow-lg !rounded-lg !border !border-gray-200 !px-6'):
            ui.label('Listado de Roles').classes('!text-2xl !font-bold !text-gray-800 !mb-4 text-center')

            tableRef = ui.table(
                columns=[
                    {'name': 'rolid', 'label': 'ID', 'field': 'rolid', 'sortable': True, 'align': 'center'},
                    {'name': 'nombrerol', 'label': 'Rol', 'field': 'nombrerol', 'sortable': True, 'align': 'center'},
                ],
                rows=[],
                row_key='rolid',
                pagination={'rowsPerPage': 10}
            ).classes('!w-full text-center')

            async def cargarRoles():
                data = await fetchRoles()
                tableRef.rows = data
                statsRow.clear()
                with statsRow:
                    ui.label(f'Total Roles: {len(data)}')

            ui.button('Refrescar', icon='refresh', on_click=cargarRoles).classes(
                '!bg-blue-600 !text-white hover:!bg-blue-700 !px-4 !py-2 !rounded !transition !my-4'
            )

        statsRow = ui.row().classes('!w-full !justify-end !space-x-4 !text-sm !text-gray-600 !px-4 !mt-2')

        ui.timer(0.1, cargarRoles, once=True)

    Footer()