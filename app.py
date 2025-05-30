from nicegui import ui
from views.home import homePage
from views.login import login
from views.register import register
from views.admin.adminHome import homePageAdmin
from views.client.clientHome import homePageClient
from views.agent.agentHome import homePageAgent
from views.agent.client.createClient import createClient
from views.agent.client.editClient import editClient
from views.agent.client.viewClient import viewClient
from views.agent.client.deleteClient import deleteClient
from views.admin.agent.createAgent import createAgent
from views.admin.agent.viewAgent import viewAgent
from views.admin.agent.editAgent import editAgent
from views.admin.agent.deleteAgent import deleteAgent
from views.admin.role.createRol import createRole
from views.admin.role.viewRol import viewRole
from views.admin.role.editarRol import editRole
from views.admin.role.deleteRol import deleteRole

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

@ui.page('/crearCliente')
def createClientPage():
    ui.add_head_html(verificarAcceso(['Agente', 'Administrador']))
    createClient()

@ui.page('/editarCliente')
def editClientPage():
    ui.add_head_html(verificarAcceso(['Agente', 'Administrador']))
    editClient()

@ui.page('/verCliente')
def viewClientPage():
    ui.add_head_html(verificarAcceso(['Agente', 'Administrador']))
    viewClient()

@ui.page('/eliminarCliente')
def deleteClientPage():
    ui.add_head_html(verificarAcceso(['Agente', 'Administrador']))
    deleteClient()

@ui.page('/crearAgente')
def createAgentPage():
    ui.add_head_html(verificarAcceso(['Administrador']))
    createAgent()

@ui.page('/verAgentes')
def viewAgentPage():
    ui.add_head_html(verificarAcceso(['Administrador']))
    viewAgent()

@ui.page('/editarAgente')
def editAgentPage():
    ui.add_head_html(verificarAcceso(['Administrador']))
    editAgent()

@ui.page('/eliminarAgente')
def deleteAgentPage():
    ui.add_head_html(verificarAcceso(['Administrador']))
    deleteAgent()

@ui.page('/crearRol')
def createRolePage():
    ui.add_head_html(verificarAcceso(['Administrador']))
    createRole()

@ui.page('/verRoles')
def viewRolePage():
    ui.add_head_html(verificarAcceso(['Administrador']))
    viewRole()

@ui.page('/actualizarRol')
def editRolePage():
    ui.add_head_html(verificarAcceso(['Administrador']))
    editRole()

@ui.page('/eliminarRol')
def deleteRolePage():
    ui.add_head_html(verificarAcceso(['Administrador']))
    deleteRole()

ui.run(title="Ixavia Airline", favicon='./assets/logoIxavia.png')