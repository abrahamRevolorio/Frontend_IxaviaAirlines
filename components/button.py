from nicegui import ui

def Button(config: dict):
    text = config.get('texto', 'Botón')
    clases = config.get('clases', '')
    bg_color = config.get('bgColor', '')
    text_color = config.get('textColor', '')

    navigate_to = config.get('navigate_to', '')

    on_click_js = config.get('onClickJs', '')
    on_click_py = config.get('onClickPy', None)

    style = ''
    if bg_color:
        style += f'background-color: {bg_color} !important;'
    if text_color:
        style += f'color: {text_color} !important;'

    if on_click_js and on_click_py:
        btn = ui.button(text).classes(clases).style(style).on('click', on_click_py)
        btn._props['onclick'] = on_click_js
        return btn

    if on_click_js:
        ui.html(f'''
            <button onclick="{on_click_js}" class="{clases}" style="{style}">
                {text}
            </button>
        ''')

    elif on_click_py:
        return ui.button(text).classes(clases).style(style).on('click', on_click_py)

    elif navigate_to:
        with ui.link(target=navigate_to):
            return ui.button(text).classes(clases).style(style)

    else:
        return ui.button(text).classes(clases).style(style)