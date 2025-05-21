from nicegui import ui
from views.home import homePage
from views.login import login

ui.add_head_html('''
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.4.1/dist/tailwind.min.css" rel="stylesheet">        
''')

@ui.page('/')
def mainPage():
    homePage()

@ui.page('/login')
def loginPage():
    login()


ui.run(title="Ixavia Airline", favicon='./assets/logoIxavia.png')