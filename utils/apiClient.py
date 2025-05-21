import requests
import jwt

BASE_URL = "http://localhost:8000"

def decodeToken(token):
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except Exception as e:
        print("Error al decodificar el token:", e)
        return None

def loginUser(email: str, password: str) -> dict:
    url = f"{BASE_URL}/auth/login"
    try:
        response = requests.post(url, json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            accessToken = data.get("accessToken")

            if not accessToken:
                return {"success": False, "message": "Error al obtener el token de acceso"}
            
            userData = decodeToken(accessToken)

            if not userData:
                return {"success": False, "message": "Error al decodificar el token"}
            
            if userData.get("rol") == "Administrador" or userData.get("rol") == "Empleado":
                return {
                    "success": True, 
                    "accessToken": accessToken, 
                    "userId": userData.get("userId"),
                    "rol": userData.get("rol"), 
                    "nombre": userData.get("nombre"), 
                    "apellido": userData.get("apellido"),
                    "dpi": userData.get("dpi"),
                    "nit": userData.get("nit"),
                    "telefono": userData.get("telefono"),
                    "edad": userData.get("edad"),
                }
            else:

                return{

                    "success": True, 
                    "accessToken": accessToken, 
                    "userId": userData.get("userId"),
                    "rol": userData.get("rol"), 
                    "nombre": userData.get("nombre"), 
                    "apellido": userData.get("apellido"),
                    "dpi": userData.get("dpi"),
                    "telefono": userData.get("telefono"),
                    "direccion": userData.get("direccion"),
                    "fechadenacimiento": userData.get("fechadenacimiento"),
                    "nacionalidad": userData.get("nacionalidad"),
                    "edad": userData.get("edad"),
                    "telefonoEmergencia": userData.get("telefonoEmergencia"),

                }

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