from nicegui import ui
import asyncio
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import logout, deleteFromBackend
from utils.validators import isValidDpi

def deleteClient():
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

    ui.label('Eliminar Usuario').classes('text-4xl font-bold text-center mt-12 mb-8')

    with ui.card().classes('w-3/4 max-w-3xl mx-auto p-10 shadow-2xl rounded-2xl bg-white'):
        dpiInput = ui.input('Ingrese el DPI del usuario a eliminar').classes('w-full text-lg mb-4')
        errorLabel = ui.label('').classes('text-red-500 text-sm mb-4')
        deleteButton = ui.button('Eliminar Usuario').classes(
            '!bg-red-600 hover:!bg-red-700 transition-all duration-200 !text-white !font-bold !text-lg !py-3 !px-8 !rounded-lg w-full'
        )

        def validate():
            dpi = dpiInput.value.strip()
            if not dpi:
                errorLabel.text = 'Este campo no puede estar vacío.'
                return False
            elif not isValidDpi(dpi):
                errorLabel.text = 'DPI inválido. Debe contener exactamente 13 dígitos.'
                return False
            errorLabel.text = ''
            return True

        async def eliminar():
            if not validate():
                ui.notify('Corrige los errores antes de continuar.', type='warning')
                return

            deleteButton.props('disable')
            data = {"dpi": dpiInput.value.strip()}
            response = await deleteFromBackend('user/delete', data)

            if response and response.get('success'):
                ui.notify('Usuario eliminado correctamente.', type='positive')
                dpiInput.value = ''
                await asyncio.sleep(2)
                ui.run_javascript("window.location.href = '/'")
            else:
                msg = response.get('message', 'Error al eliminar') if response else 'Error en la conexión'
                ui.notify(msg, type='negative')

            deleteButton.props(remove='disable')

        dpiInput.on('blur', lambda: validate())
        deleteButton.on('click', eliminar)

    Footer()
