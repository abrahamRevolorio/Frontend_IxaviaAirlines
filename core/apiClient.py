import requests

BASE_URL = "http://localhost:8000"

def loginUser(email: str, password: str) -> dict:
    url = f"{BASE_URL}/auth/login"
    try:
        response = requests.post(url, json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "rol": data.get("rol", "usuario")}
        else:
            return {"success": False, "message": response.json().get("detail", "Error al iniciar sesión")}
    except Exception as e:
        return {"success": False, "message": f"Error de conexión: {e}"}

def registerUser(nombres: str, apellidos: str, email: str, password: str, dpi: str,
                 telefono: str, direccion: str, nacimiento: str,
                 nacionalidad: str, telefonoEmergencia: str) -> dict:
    url = f"{BASE_URL}/auth/register"
    payload = {
        "nombres": nombres,
        "apellidos": apellidos,
        "email": email,
        "password": password,
        "dpi": dpi,
        "telefono": telefono,
        "direccion": direccion,
        "nacimiento": nacimiento,
        "nacionalidad": nacionalidad,
        "telefonoEmergencia": telefonoEmergencia
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            return {"success": True}
        else:
            return {"success": False, "message": response.json().get("detail", "Error al registrar usuario")}
    except Exception as e:
        return {"success": False, "message": f"Error de conexión: {e}"}
