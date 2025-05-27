from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer

def homePageClient():
    opcionesNavbar = [
        {
            'texto': 'Logout',
            'onClickJs': "localStorage.clear(); window.location.href = '/'",
            'clases': '!mx-2 !py-2 !px-6 !rounded !border !border-[#486142] !transition !font-bold !text-base !hover:bg-[#1E4DBB] !hover:text-[#F0F4FF]',
            'bgColor': "#AA0000",
            'textColor': '#F0F4FF'
        }
    ]

    Navbar(opcionesNavbar)

    with ui.element('main').classes('flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex flex-col gap-16'):
        with ui.element('section').classes('flex flex-col md:flex-row items-center gap-10'):
            with ui.column().classes('flex-1 text-center md:text-left'):
                ui.label('Panel de Control - Cliente 👤').classes(
                    'text-4xl md:text-4xl font-extrabold text-[#486142] mb-6'
                )
                ui.label(
                    '✨ Gestiona tus reservas a través de nuestra plataforma. Accede a tus boletos y comprobantes en un solo lugar. 📂'
                ).classes('text-base md:text-lg text-gray-700 mb-8 md:mb-10')
                ui.button('Acceder a Gestión de Reservas').classes(
                    '!w-full !sm:w-auto !min-w-[240px] !bg-[#486142] !text-white !font-semibold !px-8 !py-4 !rounded-lg !shadow-md !hover:bg-[#37522C] !transition-colors'
                ).on('click', lambda e: ui.run_javascript('window.location.href = "/reservas"'))

            ui.image('https://media.istockphoto.com/id/490523573/es/foto/tranquilo-lago-peten-en-guatemala.jpg?s=612x612&w=0&k=20&c=HS6dTsRmg3Gga07R8lFBEdcwX5YRzN2E1GWPvJw_WJA=').classes(
                'flex-1 rounded-lg shadow-lg max-w-full w-full md:max-w-none'
            ).style('object-fit: cover; max-height: 340px;')

        with ui.element('section').classes('flex flex-col md:flex-row-reverse items-center gap-10 mt-8'):
            with ui.column().classes('flex-1 text-center md:text-right'):
                ui.label('Tus Boletos Digitales').classes(
                    'text-3xl md:text-4xl font-extrabold text-[#486142] mb-6'
                )
                ui.label(
                    '📲 Visualiza y descarga todos tus boletos adquiridos. ¡Llévalos siempre contigo en tu dispositivo móvil! 📥'
                ).classes('!text-base !md:text-lg !text-gray-700 !mb-8 !md:mb-10')
                ui.button('Ver Mis Boletos').classes(
                    '!w-full !sm:w-auto !min-w-[240px] !bg-[#486142] !text-white !font-semibold !px-8 !py-4 !rounded-lg !shadow-md !hover:bg-[#153B8B] !transition-colors'
                ).on('click', lambda e: ui.run_javascript('window.location.href = "/boletos"'))
            
            ui.image('https://www.laprensagrafica.com/__export/1722536858506/sites/prensagrafica/img/2024/08/01/boletos-de-avixn-1280x720.jpg_423682103.jpg').classes(
                'flex-1 rounded-lg shadow-lg max-w-full w-full md:max-w-none'
            ).style('object-fit: cover; max-height: 340px;')

        with ui.element('section').classes(
            'bg-[#f0f4ef] rounded-lg p-8 md:p-12 grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-10 text-center'
        ):
            for icon, title, desc in [
                ('🛎️', 'Atención Prioritaria 24/7', 'Soporte creado para Reservas de manera segura y personalizada. 📞💬'),
                ('💳', 'Pagos 100% Seguros', 'Tus transacciones protegidas con los más altos estándares. 🔒🛡️'),
                ('📚', 'Documentación Fácil', 'Tus boletas se te enviarán automáticamente por correo electrónico. ✉️📎')
            ]:
                with ui.column():
                    ui.label(icon).classes('text-4xl md:text-5xl mb-3 md:mb-4')
                    ui.label(title).classes('font-bold text-lg md:text-xl mb-1 md:mb-2 text-[#486142]')
                    ui.label(desc).classes('text-gray-700 text-sm md:text-base')

    Footer()
