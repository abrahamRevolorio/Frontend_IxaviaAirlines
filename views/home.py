from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer

def homePage():
    opcionesNavbar = [
        {
            'texto': 'Login',
            'navigate_to': '/login',
            'clases': '!mx-1 !py-2 !px-6 !rounded !border !border-[#486142] !transition !font-bold !text-[14px] !hover:bg-[#1E4DBB] !hover:text-[#F0F4FF] !bg-[#013691] !text-[#F0F4FF]',
        },
        {
            'texto': 'Registrarte',
            'navigate_to': '/register',
            'clases': '!mx-1 !py-2 !px-6 !rounded !transition !font-bold !text-[14px] !hover:bg-[#B96328] !hover:text-[#F0F4FF] !bg-[#B54B00] !text-[#F0F4FF]',
        }
    ]

    Navbar(opcionesNavbar)

    with ui.element('main').classes('flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex flex-col gap-16'):
        with ui.element('section').classes('flex flex-col md:flex-row items-center gap-10'):
            with ui.column().classes('flex-1 text-center md:text-left'):
                ui.label('Vuela Seguro y Cómodo con Ixavia Airlines').classes('text-3xl md:text-5xl font-extrabold text-[#2e4e2f] mb-4 md:mb-6')
                ui.label(
                    'Ofrecemos vuelos directos entre Ciudad de Guatemala y Petén con puntualidad y calidad. '
                    'Reserva tu asiento y prepárate para una experiencia inolvidable.'
                ).classes('text-base md:text-lg text-gray-700 mb-6 md:mb-8')
                with ui.row().classes('flex-col sm:flex-row justify-center md:justify-start gap-4 sm:gap-6'):
                    ui.button('Buscar vuelos CDG → Petén').classes(
                        '!w-full !sm:w-auto !min-w-[220px] !bg-[#1A5AC8] !text-white !font-semibold !px-6 !py-3 !rounded-lg !shadow-md !hover:bg-[#0F4AA6] !transition-colors'
                    )
                    ui.button('Buscar vuelos Petén → CDG').classes(
                        '!w-full !sm:w-auto !min-w-[220px] !bg-[#486142] !text-white !font-semibold !px-6 !py-3 !rounded-lg !shadow-md !hover:bg-[#2e4e2f] !transition-colors'
                    )
            ui.image('./assets/tikal.jpg').classes('flex-1 rounded-lg shadow-lg max-w-full w-full md:max-w-none').style('object-fit: cover; height: 320px;')

        with ui.element('section').classes('bg-[#f0f4ef] rounded-lg p-8 md:p-12 grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-10 text-center'):
            for icon, title, desc in [
                ('✈️', 'Rutas Directas', 'Viaja sin escalas entre Ciudad de Guatemala y Petén, ahorrando tiempo y molestias.'),
                ('🛡️', 'Seguridad Garantizada', 'Contamos con estrictos protocolos para que tu viaje sea seguro y confiable.'),
                ('💺', 'Comodidad a Bordo', 'Disfruta de asientos espaciosos y un servicio atento durante todo el vuelo.')
            ]:
                with ui.column():
                    ui.label(icon).classes('text-4xl md:text-5xl mb-3 md:mb-4')
                    ui.label(title).classes('font-bold text-lg md:text-xl mb-1 md:mb-2 text-[#2e4e2f]')
                    ui.label(desc).classes('text-gray-700 text-sm md:text-base')

        with ui.element('section').classes('bg-[#2e4e2f] rounded-lg p-8 md:p-12 text-center text-white'):
            ui.label('Reserva tu vuelo hoy y vive la experiencia Ixavia Airlines').classes('text-2xl md:text-3xl font-extrabold mb-4 md:mb-6')
            ui.button('Reservar Ahora').classes(
                '!w-full !sm:w-auto !min-w-[220px] !bg-[#d97d3a] !hover:bg-[#b3631f] !px-8 !py-3 !rounded-lg !font-bold !text-lg !shadow-md !transition-colors'
            ).on('click', lambda e: ui.run_javascript('window.location.href = "/login"'))

    Footer()