from nicegui import ui
import asyncio
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import logout, deleteFromBackend

def deleteFlight():
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

    ui.label('Eliminar Vuelo').classes('text-4xl font-bold text-center mt-12 mb-8')

    with ui.card().classes('w-3/4 max-w-3xl mx-auto p-10 shadow-2xl rounded-2xl bg-white'):
        vueloIdInput = ui.input('Ingrese el id del Vuelo a eliminar').classes('w-full text-lg mb-4')
        errorLabel = ui.label('').classes('text-red-500 text-sm mb-4')
        deleteButton = ui.button('Eliminar Vuelo').classes(
            '!bg-red-600 hover:!bg-red-700 transition-all duration-200 !text-white !font-bold !text-lg !py-3 !px-8 !rounded-lg w-full'
        )

        def validate():
            roleid = vueloIdInput.value.strip()
            if not roleid:
                errorLabel.text = 'Este campo no puede estar vacío.'
                return False
            errorLabel.text = ''
            return True

        async def eliminar():
            if not validate():
                ui.notify('Corrige los errores antes de continuar.', type='warning')
                return

            deleteButton.props('disable')
            
            data = {"vueloid": int(vueloIdInput.value.strip())}
            response = await deleteFromBackend('flight/delete', data)

            print(response)

            if response:
                if response.get('data').get('success') == False:
                    ui.notify(f'Error: {response.get("data").get("message")}', type='negative')
                else:
                    ui.notify('Vuelo eliminado correctamente.', type='positive')
                    vueloIdInput.value = ''
                    await asyncio.sleep(2)
                    ui.run_javascript("window.location.href = '/'")
            else:
                msg = response.get('message', 'Error al eliminar') if response else 'Error en la conexión'
                ui.notify(msg, type='negative')

            deleteButton.props(remove='disable')

        vueloIdInput.on('blur', lambda: validate())
        deleteButton.on('click', eliminar)

    Footer()