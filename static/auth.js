function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64).split('').map(c =>
        '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
      ).join('')
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

(function checkAuth() {
  const token = localStorage.getItem('accessToken');
  const path = window.location.pathname;

  const routePermissions = {
    '/admin': ['Administrador'],
    '/agente': ['Agente'],
    '/cliente': ['Cliente'],
    '/reporte': ['Administrador', 'Agente'],
    '/perfil': ['Administrador', 'Agente', 'Cliente'],
    '/login': [],
    '/register': [],
    '/': [],
  };

  const redirectMap = {
    'Administrador': '/admin',
    'Agente': '/agente',
    'Cliente': '/cliente'
  };

  function showToastAndRedirect(message, target) {
    Toastify({
      text: message,
      duration: 3000,
      gravity: "top",
      position: "center",
      backgroundColor: "#DC2626",
      stopOnFocus: true,
    }).showToast();
    setTimeout(() => {
      window.location.href = target;
    }, 3200);
  }

  function showContent() {
    const loader = document.querySelector('.h-screen');
    const content = document.querySelector('.page-content');
    if (loader) loader.style.display = 'none';
    if (content) content.classList.remove('hidden');
  }

  // Lógica
  if (token) {
    const payload = parseJwt(token);
    if (!payload || !payload.rol) {
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
      return;
    }

    const userRole = payload.rol;
    const allowedRoles = routePermissions[path];

    if (!allowedRoles || !allowedRoles.includes(userRole)) {
      showToastAndRedirect("No tienes permiso para acceder a esta página.", redirectMap[userRole] || '/');
      return;
    }

    // ✅ Tiene permiso
    showContent();
  } else {
    const allowedRoles = routePermissions[path];
    if (allowedRoles && allowedRoles.length > 0) {
      window.location.href = '/login';
    } else {
      showContent();
    }
  }
})();
