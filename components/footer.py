from nicegui import ui

def Footer():
    with ui.footer().classes(
        'bg-[#12210f] text-[#eeeee4] p-4 mt-auto w-full flex justify-center items-center border-t border-[#486142]'
    ):
        ui.label('© 2025 Ixavia Airline. Proyecto por Universidad Mesoamericana').classes('text-sm md:text-base text-center')