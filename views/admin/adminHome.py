from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer

def homePageAdmin():
    opcionesNavbar = [
        {
            'texto': 'Logout',
            'onClickJs': "localStorage.clear(); window.location.href = '/'",
            'clases': 'mx-2 py-2 px-6 rounded border border-[#486142] transition font-bold text-base hover:bg-[#1E4DBB] hover:text-[#F0F4FF]',
            'bgColor': "#AA0000",
            'textColor': '#F0F4FF'
        }
    ]

    Navbar(opcionesNavbar)

    def mostrarCrudModal(titulo, botones):
        with ui.dialog() as modal, ui.card().classes('!w-full !max-w-2xl !p-8 !rounded-xl !bg-white !shadow-2xl !relative !flex !flex-col !gap-6'):
            ui.button('✕', on_click=modal.close).classes(
                'absolute top-2 right-2 text-xl font-bold text-gray-500 hover:text-red-600 cursor-pointer'
            ).props('flat')
            ui.label(titulo).classes('!text-2xl !font-bold !text-center !mb-4')
            for texto, color in botones:
                ui.button(texto).classes(f'!w-full !bg-{color}-600 !text-white !rounded !py-2')

        modal.props('persistent')
        modal.open()

    with ui.column().classes('!w-full !max-w-7xl !mx-auto !my-10 !px-6 !sm:px-12 !rounded-lg !min-h-screen').style('background-color: transparent;'):
        ui.label('Panel de Control - Administrador').classes(
            '!text-4xl !font-semibold !text-[#486142] !mb-10 !text-center !font-sans !tracking-wide'
        )

        with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-12'):
            cards = [
                {
                    'titulo': 'Usuarios y Roles',
                    'descripcion': 'Administra usuarios y asigna roles con facilidad.',
                    'img': 'https://cdn-icons-png.flaticon.com/512/1077/1077063.png',
                    'link': 'modal_usuarios'
                },
                {
                    'titulo': 'Gestión de Vuelos',
                    'descripcion': 'Crea, edita y elimina vuelos disponibles.',
                    'img': 'https://cdn-icons-png.flaticon.com/512/2666/2666404.png',
                    'link': '/vuelos'
                },
                {
                    'titulo': 'Capacidad de Aviones',
                    'descripcion': 'Modifica la capacidad máxima de asientos.',
                    'img': 'https://cdn-icons-png.flaticon.com/512/1350/1350120.png',
                    'link': '/aviones'
                },
                {
                    'titulo': 'Reportes y Auditoría',
                    'descripcion': 'Visualiza reportes operativos y logs del sistema.',
                    'img': 'https://cdn-icons-png.flaticon.com/512/942/942748.png',
                    'link': '/reportes'
                },
                {
                    'titulo': 'Reservas y Boletos',
                    'descripcion': 'Gestiona reservas, pagos simulados y emisión de boletos.',
                    'img': 'https://cdn-icons-png.flaticon.com/512/2942/2942993.png',
                    'link': '/reservas'
                },
                {
                    'titulo': 'Clientes',
                    'descripcion': 'Registra y edita la información de los clientes.',
                    'img': 'https://cdn-icons-png.flaticon.com/512/2922/2922510.png',
                    'link': '/clientes'
                }
            ]

            def handleCardClick(link):
                if link == 'modal_usuarios':
                    mostrarCrudModal('Usuarios y Roles', [
                        ('Crear Usuario', 'green'),
                        ('Ver Usuarios', 'blue'),
                        ('Actualizar Usuario', 'yellow'),
                        ('Eliminar Usuario', 'red')
                    ])
                elif link == '/vuelos':
                    mostrarCrudModal('Gestión de Vuelos', [
                        ('Crear Vuelo', 'green'),
                        ('Ver Vuelos', 'blue'),
                        ('Actualizar Vuelo', 'yellow'),
                        ('Eliminar Vuelo', 'red')
                    ])
                elif link == '/aviones':
                    mostrarCrudModal('Capacidad de Aviones', [
                        ('Crear Avión', 'green'),
                        ('Ver Aviones', 'blue'),
                        ('Actualizar Avión', 'yellow'),
                        ('Eliminar Avión', 'red')
                    ])
                elif link == '/reportes':
                    mostrarCrudModal('Reportes y Auditoría', [
                        ('Ver Reportes', 'blue'),
                        ('Descargar Logs', 'yellow'),
                        ('Exportar CSV', 'green'),
                        ('Eliminar Logs', 'red')
                    ])
                elif link == '/reservas':
                    mostrarCrudModal('Reservas y Boletos', [
                        ('Crear Reserva', 'green'),
                        ('Ver Reservas', 'blue'),
                        ('Confirmar Pago', 'yellow'),
                        ('Cancelar Reserva', 'red')
                    ])
                elif link == '/clientes':
                    mostrarCrudModal('Clientes', [
                        ('Registrar Cliente', 'green'),
                        ('Ver Clientes', 'blue'),
                        ('Actualizar Cliente', 'yellow'),
                        ('Eliminar Cliente', 'red')
                    ])
                else:
                    ui.open(link)

            for card in cards:
                with ui.card().classes(
                    '!bg-white !bg-opacity-70 !rounded-xl !shadow-md !hover:shadow-xl !transition-shadow !duration-300 !p-6 !flex !flex-col !items-center !text-center !cursor-pointer'
                ).on('click', lambda e, l=card['link']: handleCardClick(l)):
                    ui.image(card['img']).classes('!w-24 !h-24 !mb-5 !object-contain')
                    ui.label(card['titulo']).classes('!text-2xl !font-semibold !text-[#486142] !mb-3 !font-sans !tracking-tight')
                    ui.label(card['descripcion']).classes('!text-[#1E4DBB] !text-base !mb-6 !px-4 !font-medium')
                    ui.button('Acceder').classes(
                        '!bg-[#486142] !hover:bg-[#37522C] !text-white !font-semibold !py-2 !px-8 !rounded-full !shadow-md !transition-colors !duration-300'
                    )

    Footer()