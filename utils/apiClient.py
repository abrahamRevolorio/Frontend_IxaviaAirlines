import requests
import jwt
import httpx
import json

BASE_URL = "https://backend-ixaviaairlines.onrender.com"

tokenGlobal = None

def decodeToken(token):
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except Exception as e:
        print("Error al decodificar el token:", e)
        return None

def loginUser(email: str, password: str) -> dict:
    global tokenGlobal
    url = f"{BASE_URL}/auth/login"
    try:
        response = requests.post(url, json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            accessToken = data.get("accessToken")

            tokenGlobal = data.get("accessToken")

            if not accessToken:
                return {"success": False, "message": "Error al obtener el token de acceso"}
            
            userData = decodeToken(accessToken)

            if not userData:
                return {"success": False, "message": "Error al decodificar el token"}

            if userData.get("rol") in ["Administrador", "Empleado"]:
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
                return {
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


async def postToBackend(endpoint: str, payload: dict) -> dict:
    url = f"{BASE_URL}/{endpoint}"

    global tokenGlobal

    token = tokenGlobal

    headers = {}

    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            success = response.status_code in [200, 201]
            return {
                "success": success,
                "data": response.json() if success else None,
                "message": response.json().get("detail", "Éxito" if success else "Error")
            }
        except Exception as e:
            return {"success": False, "message": f"Error de conexión: {e}"}

async def putToBackend(endpoint: str, payload: dict) -> dict:
    url = f"{BASE_URL}/{endpoint}"

    global tokenGlobal
    token = tokenGlobal

    headers = {}
    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, json=payload, headers=headers)
            success = response.status_code in [200, 204]
            return {
                "success": success,
                "data": response.json() if success and response.content else None,
                "message": response.json().get("detail", "Éxito" if success else "Error")
            }
        except Exception as e:
            return {"success": False, "message": f"Error de conexión: {e}"}

async def getFromBackend(endpoint: str, params: dict = None) -> dict:
    url = f"{BASE_URL}/{endpoint}"

    global tokenGlobal
    token = tokenGlobal

    headers = {}

    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            success = response.status_code == 200
            return {
                "success": success,
                "data": response.json() if success else None,
                "message": response.json().get("detail", "Éxito" if success else "Error")
            }
        except Exception as e:
            return {"success": False, "message": f"Error de conexión: {e}"}
        
async def findFromBackend(url: str, payload: dict) -> dict:
    global tokenGlobal
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    if tokenGlobal:
        headers["Authorization"] = f"Bearer {tokenGlobal}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method="GET",
                url=f'{BASE_URL}/{url}',
                content=json.dumps(payload).encode("utf-8"),
                headers=headers
            )

            success = response.status_code == 200
            try:
                response_data = response.json() if success else None
                message = response_data.get("detail", "Éxito" if success else "Error del servidor")
            except ValueError:
                response_data = None
                message = "Respuesta no es JSON válido"

            return {
                "success": success,
                "data": response_data,
                "message": message
            }

        except httpx.ConnectError as e:
            return {"success": False, "data": None, "message": f"Error de conexión: {str(e)}"}
        except Exception as e:
            return {"success": False, "data": None, "message": f"Error inesperado: {str(e)}"}

async def deleteFromBackend(endpoint: str) -> dict:
    url = f"{BASE_URL}/{endpoint}"

    global tokenGlobal
    token = tokenGlobal

    headers = {}
    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(url, headers=headers)
            success = response.status_code in [200, 204]
            return {
                "success": success,
                "data": response.json() if success and response.content else None,
                "message": response.json().get("detail", "Éxito" if success else "Error")
            }
        except Exception as e:
            return {"success": False, "message": f"Error de conexión: {e}"}
        
def logout():
    global tokenGlobal
    print("Se ha cerrado la sesión")
    tokenGlobal = None
