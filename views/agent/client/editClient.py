from nicegui import ui
import asyncio
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import logout, putToBackend, findFromBackend

def editClient():
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

    ui.label('Editar Información del Usuario').classes('text-2xl font-bold mb-4 mt-8')

    with ui.card().classes('max-w-3xl w-full mx-auto p-6 shadow-lg'):
        dpi_input = None
        fields = {}
        guardar_btn = None
        buscar_btn = None

        async def buscar_usuario():
            nonlocal dpi_input, fields, guardar_btn, buscar_btn
            dpi = dpi_input.value.strip()
            if not dpi:
                ui.notify('Por favor ingresa un DPI', type='negative')
                return

            buscar_btn.props('disable')
            dpi_input.props('disable')

            data = {"dpi": dpi}
            response = await findFromBackend('user/find', data)

            if response and response.get("success") and response.get("data", {}).get("success"):
                user_info = response["data"]["user_info"]
                for key, inputWidget in fields.items():
                    if key in user_info:
                        if key != "password":
                            inputWidget.value = str(user_info[key])
                        inputWidget.props(remove='disable')
                
                fields["password"].value = ''
                guardar_btn.props(remove='disable')
                ui.notify('Datos cargados', type='positive')
            else:
                error_msg = response.get("data", {}).get("message", "Usuario no encontrado") if response else "Error en la conexión"
                ui.notify(error_msg, type='negative')
                for inputWidget in fields.values():
                    inputWidget.value = ''
                    inputWidget.props('disable')
                guardar_btn.props('disable')

            buscar_btn.props(remove='disable')
            dpi_input.props(remove='disable')

        async def editar():
            nonlocal dpi_input, fields, guardar_btn

            dpi = dpi_input.value.strip()
            if not dpi:
                ui.notify('Por favor ingresa un DPI para editar', type='negative')
                return

            guardar_btn.props('disable')

            data = {}
            for k, v in fields.items():
                valor = v.value.strip()
                if k == "password":
                    if valor:
                        data[k] = valor
                else:
                    if valor:
                        data[k] = valor

            data["dpi"] = dpi

            data["nombre"] = data["nombres"]
            data["apellido"] = data["apellidos"]

            print(data)

            response = await putToBackend('user/update', data)

            if response and response.get('success'):
                ui.notify('Usuario actualizado correctamente', type='positive')
                asyncio.sleep(2)
                ui.run_javascript("window.location.href = '/'")
            else:
                msg = response.get('message', 'Error al actualizar') if response else 'Error en la conexión'
                errors = response.get('errors') if response else None
                if errors:
                    msg += ": " + ", ".join(errors)
                ui.notify(msg, type='negative')

            guardar_btn.props(remove='disable')

        with ui.row().classes('w-full items-center mb-4'):
            dpi_input = ui.input('DPI').classes('flex-grow')
            buscar_btn = ui.button('Buscar Usuario', on_click=buscar_usuario).classes(
                'bg-[#1E4DBB] text-white font-bold py-2 px-6 rounded ml-2'
            )

        fields = {
            "nombres": ui.input('Nombres').classes('w-full mb-4').props('disable'),
            "apellidos": ui.input('Apellidos').classes('w-full mb-4').props('disable'),
            "email": ui.input('Email').classes('w-full mb-4').props('disable'),
            "telefono": ui.input('Teléfono').classes('w-full mb-4').props('disable'),
            "direccion": ui.input('Dirección').classes('w-full mb-4').props('disable'),
            "fechadenacimiento": ui.input('Fecha de Nacimiento (YYYY-MM-DD)').classes('w-full mb-4').props('disable'),
            "nacionalidad": ui.input('Nacionalidad').classes('w-full mb-4').props('disable'),
            "edad": ui.input('Edad').classes('w-full mb-4').props('disable'),
            "telefonoemergencia": ui.input('Teléfono de Emergencia').classes('w-full mb-4').props('disable'),
            "password": ui.input('Nueva Contraseña (opcional)').classes('w-full mb-4').props('disable'),
        }

        guardar_btn = ui.button('Guardar Cambios', on_click=editar).classes(
            'bg-[#002678] text-white font-bold py-2 px-6 rounded'
        ).props('disable')

    Footer()
