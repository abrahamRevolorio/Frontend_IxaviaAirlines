from nicegui import ui
from views.home import homePage
from views.login import login
from views.register import register
from views.admin.adminHome import homePageAdmin
from views.client.clientHome import homePageClient
from views.agent.agentHome import homePageAgent

# Tailwind CSS
ui.add_head_html('''
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.4.1/dist/tailwind.min.css" rel="stylesheet">
<style>body{display:none;}</style>  <!-- Oculta el body inicialmente -->
''')

def js_parse_jwt():
    return """
    function pJ(t){try{return JSON.parse(decodeURIComponent(atob(t.split('.')[1]).split('').map(c=>'%'+('00'+c.charCodeAt(0).toString(16)).slice(-2)).join('')))}catch{return null}}
    """

def verificarAcceso(roles):
    roles_js = '[' + ','.join(f'"{r}"' for r in roles) + ']'
    return f"""
    <script>
    {js_parse_jwt()}
    const t=localStorage.getItem('accessToken'), r={roles_js};
    if(!t) window.location.href='/login';
    else {{
      let p=pJ(t);
      if(!p || !r.includes(p.rol)) {{
        window.nicegui.notify('No tienes acceso.', {{type:'negative', position:'top'}});
        setTimeout(() => window.location.href='/', 2000);
      }} else document.body.style.display='block';
    }}
    </script>
    """

def redirigirSiToken(rutas_rol):
    roles_js = '[' + ','.join(f'"{r}"' for r in rutas_rol.keys()) + ']'
    rutas_js = '{' + ','.join(f'"{r}":"{path}"' for r, path in rutas_rol.items()) + '}'
    return f"""
    <script>
    {js_parse_jwt()}
    const t=localStorage.getItem('accessToken');
    if(t) {{
      const p=pJ(t);
      if(p && {roles_js}.includes(p.rol)) {{
        window.location.href = {rutas_js}[p.rol];
      }} else {{
        document.body.style.display='block';
      }}
    }} else {{
      document.body.style.display='block';
    }}
    </script>
    """

@ui.page('/ping')
def pingPage():
    print('Pinged!')

@ui.page('/')
def mainPage():
    ui.add_head_html(redirigirSiToken({'Administrador':'/admin','Agente':'/agente','Cliente':'/cliente'}))
    homePage()

@ui.page('/login')
def loginPage():
    ui.add_head_html(redirigirSiToken({'Administrador':'/admin','Agente':'/agente','Cliente':'/cliente'}))
    login()

@ui.page('/register')
def registerPage():
    ui.add_head_html(redirigirSiToken({'Administrador':'/admin','Agente':'/agente','Cliente':'/cliente'}))
    register()

@ui.page('/admin')
def adminPage():
    ui.add_head_html(verificarAcceso(['Administrador']))
    homePageAdmin()

@ui.page('/agente')
def agentePage():
    ui.add_head_html(verificarAcceso(['Agente']))
    homePageAgent()

@ui.page('/cliente')
def clientePage():
    ui.add_head_html(verificarAcceso(['Cliente']))
    homePageClient()

ui.run(title="Ixavia Airline", favicon='./assets/logoIxavia.png')