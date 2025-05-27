from nicegui import ui

def Button(config: dict):
    text = config.get('texto', 'Botón')
    clases = config.get('clases', '')

    bg_color = config.get('bgColor', '')
    text_color = config.get('textColor', '')

    navigate_to = config.get('navigate_to', '')

    on_click_js = config.get('onClickJs', '')

    style = ''
    if bg_color:
        style += f'background-color: {bg_color} !important;'
    if text_color:
        style += f'color: {text_color} !important;'

    if on_click_js:
        ui.html(f'''
            <button onclick="{on_click_js}" class="{clases}" style="{style}">
                {text}
            </button>
        ''')

    if navigate_to:
        with ui.link(target=navigate_to):
            return ui.button(text).classes(clases).style(style)