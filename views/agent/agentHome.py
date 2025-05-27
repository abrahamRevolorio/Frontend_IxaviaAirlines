from nicegui import ui
from components.navbar import Navbar
from components.footer import Footer

def homePageAgent():
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

    with ui.column().classes(
        '!w-full !max-w-7xl !mx-auto !my-10 !px-6 !sm:px-12 !rounded-lg !min-h-screen'
    ).style('background-color: transparent;'):
        ui.label('Panel de Control - Agente').classes(
            '!text-4xl !font-semibold !text-[#486142] !mb-10 !text-center !font-sans !tracking-wide'
        )

        with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-12'):
            cards = [
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

            for card in cards:
                with ui.card().classes(
                    '!bg-white !bg-opacity-70 !rounded-xl !shadow-md !hover:shadow-xl !transition-shadow !duration-300 !p-6 !flex !flex-col !items-center !text-center !cursor-pointer'
                ).on('click', lambda e, link=card['link']: ui.open(link)):
                    ui.image(card['img']).classes('!w-24 !h-24 !mb-5 !object-contain')
                    ui.label(card['titulo']).classes(
                        '!text-2xl !font-semibold !text-[#486142] !mb-3 !font-sans !tracking-tight'
                    )
                    ui.label(card['descripcion']).classes(
                        '!text-[#1E4DBB] !text-base !mb-6 !px-4 !font-medium'
                    )

                    ui.button('Acceder').classes(
                        '!bg-[#486142] !hover:bg-[#37522C] !text-white !font-semibold !py-2 !px-8 !rounded-full !shadow-md !transition-colors !duration-300'
                    )

    Footer()