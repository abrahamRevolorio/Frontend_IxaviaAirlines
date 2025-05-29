from nicegui import ui
import asyncio
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import logout, putToBackend, findFromBackend
from utils.validators import isNotEmpty, isValidEmail, isValidDpi, isValidPhone

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
        error_labels = {}
        guardar_btn = None
        buscar_btn = None

        validation_states = {
            'dpi': False,
            'nombres': False,
            'apellidos': False,
            'email': False,
            'telefono': False,
            'direccion': False,
            'fechadenacimiento': False,
            'nacionalidad': False,
            'telefonoemergencia': False
        }

        def validate_field(field, value, validator, error_label, error_msg=None, field_name=None):
            valid = validator(value)
            error_label.set_text('' if valid else (error_msg if error_msg else 'Campo inválido'))
            if field_name:
                validation_states[field_name] = valid
                update_save_button_state()
            return valid

        def update_save_button_state():
            if guardar_btn:
                guardar_btn.enabled = all(validation_states.values())

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
                for field_name in validation_states:
                    if field_name in fields and fields[field_name].value:
                        validation_states[field_name] = True
                update_save_button_state()
            else:
                msg = response.get("data", {}).get("message", "Usuario no encontrado") if response else "Error en la conexión"
                ui.notify(msg, type='negative')
                for inputWidget in fields.values():
                    inputWidget.value = ''
                    inputWidget.props('disable')
                guardar_btn.props('disable')
                for field_name in validation_states:
                    validation_states[field_name] = False
                update_save_button_state()

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

            response = await putToBackend('user/update', data)

            if response and response.get('success'):
                ui.notify('Usuario actualizado correctamente', type='positive')
                await asyncio.sleep(2)
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
            error_labels['dpi'] = ui.label('').classes('text-red-500 text-xs')
            buscar_btn = ui.button('Buscar Usuario', on_click=buscar_usuario).classes(
                'bg-[#1E4DBB] text-white font-bold py-2 px-6 rounded ml-2'
            )

        fields = {
            "nombres": ui.input('Nombres').classes('w-full mb-1').props('disable'),
            "apellidos": ui.input('Apellidos').classes('w-full mb-1').props('disable'),
            "email": ui.input('Email').classes('w-full mb-1').props('disable'),
            "telefono": ui.input('Teléfono').classes('w-full mb-1').props('disable'),
            "direccion": ui.input('Dirección').classes('w-full mb-1').props('disable'),
            "fechadenacimiento": ui.input('Fecha de Nacimiento (YYYY-MM-DD)').classes('w-full mb-1').props('disable'),
            "nacionalidad": ui.input('Nacionalidad').classes('w-full mb-1').props('disable'),
            "edad": ui.input('Edad').classes('w-full mb-1').props('disable'),
            "telefonoemergencia": ui.input('Teléfono de Emergencia').classes('w-full mb-1').props('disable'),
            "password": ui.input('Nueva Contraseña (opcional)').classes('w-full mb-1').props('disable'),
        }

        error_labels.update({
            "nombres": ui.label('').classes('text-red-500 text-xs -mt-2 mb-2'),
            "apellidos": ui.label('').classes('text-red-500 text-xs -mt-2 mb-2'),
            "email": ui.label('').classes('text-red-500 text-xs -mt-2 mb-2'),
            "telefono": ui.label('').classes('text-red-500 text-xs -mt-2 mb-2'),
            "direccion": ui.label('').classes('text-red-500 text-xs -mt-2 mb-2'),
            "fechadenacimiento": ui.label('').classes('text-red-500 text-xs -mt-2 mb-2'),
            "nacionalidad": ui.label('').classes('text-red-500 text-xs -mt-2 mb-2'),
            "telefonoemergencia": ui.label('').classes('text-red-500 text-xs -mt-2 mb-2')
        })

        dpi_input.on('blur', lambda: validate_field(
            dpi_input, dpi_input.value, isValidDpi, error_labels['dpi'], 
            'DPI debe tener 13 dígitos', 'dpi'
        ))

        fields["nombres"].on('blur', lambda: validate_field(
            fields["nombres"], fields["nombres"].value, isNotEmpty, error_labels["nombres"],
            'Este campo no puede estar vacío', 'nombres'
        ))

        fields["apellidos"].on('blur', lambda: validate_field(
            fields["apellidos"], fields["apellidos"].value, isNotEmpty, error_labels["apellidos"],
            'Este campo no puede estar vacío', 'apellidos'
        ))

        fields["email"].on('blur', lambda: validate_field(
            fields["email"], fields["email"].value, isValidEmail, error_labels["email"],
            'Correo electrónico inválido', 'email'
        ))

        fields["telefono"].on('blur', lambda: validate_field(
            fields["telefono"], fields["telefono"].value, isValidPhone, error_labels["telefono"],
            'Teléfono debe tener 8 dígitos', 'telefono'
        ))

        fields["direccion"].on('blur', lambda: validate_field(
            fields["direccion"], fields["direccion"].value, isNotEmpty, error_labels["direccion"],
            'Este campo no puede estar vacío', 'direccion'
        ))

        fields["nacionalidad"].on('blur', lambda: validate_field(
            fields["nacionalidad"], fields["nacionalidad"].value, isNotEmpty, error_labels["nacionalidad"],
            'Este campo no puede estar vacío', 'nacionalidad'
        ))

        fields["telefonoemergencia"].on('blur', lambda: validate_field(
            fields["telefonoemergencia"], fields["telefonoemergencia"].value, isValidPhone, 
            error_labels["telefonoemergencia"], 'Teléfono debe tener 8 dígitos', 'telefonoemergencia'
        ))

        guardar_btn = ui.button('Guardar Cambios', on_click=editar).classes(
            'bg-[#002678] text-white font-bold py-2 px-6 rounded'
        ).props('disable')

    Footer()