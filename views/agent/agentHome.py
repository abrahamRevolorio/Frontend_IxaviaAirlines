from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer
from utils.apiClient import logout

def homePageAgent():
    opcionesNavbar = [
        {
            'texto': 'Logout',
            'onClickJs': "localStorage.clear(); window.location.href = '/'",
            'onClickPy': logout,
            'clases': 'mx-2 py-2 px-6 rounded border border-[#486142] transition font-bold text-base hover:bg-[#1E4DBB] hover:text-[#F0F4FF]',
            'bgColor': "#AA0000",
            'textColor': '#F0F4FF'
        }
    ]

    Navbar(opcionesNavbar)

    def mostrarCrudModal(titulo, botones):
        with ui.dialog() as modal, ui.card().classes('!w-full !max-w-2xl !p-8 !rounded-xl !bg-white !shadow-2xl !relative !flex !flex-col !gap-6'):
            ui.button('✕', on_click=modal.close).classes('absolute top-2 right-2 text-xl font-bold text-gray-500 hover:text-red-600 cursor-pointer').props('flat')
            ui.label(titulo).classes('!text-2xl !font-bold !text-center !mb-4')
            for texto, color, ruta in botones:
                ui.button(texto).props(f'onclick="window.location.href = \'{ruta}\'"').classes(f'!w-full !bg-{color}-700 !text-white !rounded !py-2')

        modal.props('persistent')
        modal.open()

    def handleCardClick(link):
        if link == '/reportes':
            mostrarCrudModal('Reportes y Auditoría', [
                ('📄 Ver Reportes', 'blue', '/ver_reportes'),
                ('📥 Descargar Logs', 'yellow', '/descargar_logs'),
                ('📊 Exportar CSV', 'green', '/exportar_csv'),
                ('🗑️ Eliminar Logs', 'red', '/eliminar_logs')
            ])
        elif link == '/reservas':
            mostrarCrudModal('Reservas y Boletos', [
                ('📝 Crear Reserva', 'green', '/crear_reserva'),
                ('📋 Ver Reservas', 'blue', '/ver_reservas'),
                ('💳 Confirmar Pago', 'yellow', '/confirmar_pago'),
                ('❌ Cancelar Reserva', 'red', '/cancelar_reserva')
            ])
        elif link == '/clientes':
            mostrarCrudModal('Clientes', [
                ('👤 Registrar Cliente', 'green', '/crearCliente'),
                ('📋 Ver Clientes', 'blue', '/verCliente'),
                ('✏️ Actualizar Cliente', 'yellow', '/editarCliente')
            ])
        else:
            ui.open(link)

    def crearCard(card):
        with ui.card().classes(
            '!bg-white !bg-opacity-70 !rounded-xl !shadow-md !hover:shadow-xl !transition-shadow !duration-300 !p-6 !flex !flex-col !items-center !text-center !cursor-pointer'
        ).on('click', lambda e: handleCardClick(card['link'])):
            ui.image(card['img']).classes('!w-24 !h-24 !mb-5 !object-contain')
            ui.label(card['titulo']).classes('!text-2xl !font-semibold !text-[#486142] !mb-3 !font-sans !tracking-tight')
            ui.label(card['descripcion']).classes('!text-[#1E4DBB] !text-base !mb-6 !px-4 !font-medium')
            ui.button('Acceder').classes(
                '!bg-[#486142] !hover:bg-[#37522C] !text-white !font-semibold !py-2 !px-8 !rounded-full !shadow-md !transition-colors !duration-300'
            )

    with ui.column().classes('!w-full !max-w-7xl !mx-auto !my-10 !px-6 !sm:px-12 !rounded-lg !min-h-screen').style('background-color: transparent;'):
        ui.label('Panel de Control - Agente 🧑‍💼').classes(
            '!text-4xl !font-semibold !text-[#486142] !mb-10 !text-center !font-sans !tracking-wide'
        )

        with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-12'):
            cards = [
                {
                    'titulo': 'Clientes',
                    'descripcion': 'Registra y edita la información de los clientes.',
                    'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzZJkMOr4OMV2ZXb_ZaIntWCfu-PI1HImuzA&s',
                    'link': '/clientes'
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
                    'img': 'https://images.vexels.com/media/users/3/220739/isolated/preview/364a8081b080c3b1b1af9abb49ecf40e-icono-plano-de-entradas-de-cine-clasico.png',
                    'link': '/reservas'
                },
            ]

            for card in cards:
                crearCard(card)

    Footer()