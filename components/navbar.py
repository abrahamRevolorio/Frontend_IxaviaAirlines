from nicegui import ui
from components.button import Button

def Navbar(opciones=None):
    if opciones is None:
        opciones = [
            {'texto': 'Inicio', 'navigate_to': '/', 'clases': 'mx-2 py-2 px-4'},
            {'texto': 'Acerca', 'navigate_to': '/profile', 'clases': 'mx-2 py-2 px-4'}
        ]

    with ui.header().classes(
        'bg-[#233d24] p-4 shadow-lg flex flex-col items-center md:flex-row md:justify-between md:items-center gap-4 md:gap-0'
    ):
        with ui.link(target='/').classes(
            'no-underline cursor-pointer flex items-center gap-2'
        ):
            ui.image('./assets/logoIxaviaSinFondo.png').classes('w-10 h-10 hidden md:block')
            ui.label('Ixavia Airlines').classes('font-bold text-2xl text-[#eeeee4] text-center')

        with ui.row().classes('flex-wrap justify-center md:justify-start gap-4'):
            for opcion in opciones:
                Button(opcion)
