import requests
import os
import time
import base64
import json

url = "http://127.0.0.1:8000/"

def limpiarPantalla():
    os.system("cls" if os.name == "nt" else "clear")

def BannerPrincipal():
    print("* " * 40)
    print("IXAVIA AIRLINES".center(80))
    print("* " * 40)
    print("")

def bannerAdmin():
    print("* " * 40)
    print("Administrador".center(80))
    print("* " * 40)
    print("")

def bannerClient():
    print("* " * 40)
    print("Usuario".center(80))
    print("* " * 40)
    print("")

def bannerAgent():
    print("* " * 40)
    print("Agente".center(80))
    print("* " * 40)
    print("")

def decode_jwt(token):
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')

        def fix_padding(b64_string):
            return b64_string + '=' * (-len(b64_string) % 4)

        payload_json = base64.urlsafe_b64decode(fix_padding(payload_b64)).decode()
        payload = json.loads(payload_json)

        return payload

    except Exception as e:
        print("❌ Error al decodificar el token:", e)
        return None

def login():
    while True:
        try:
            limpiarPantalla()

            email = input("Ingrese su email: ")
            password = input("Ingrese su contraseña: ")

            response = requests.post(url + "auth/login", json={
                "email": email,
                "password": password
            })

            if response.status_code == 200:
                print("✅ Login exitoso")
                data = response.json()
                token = data.get("accessToken")

                if token:
                    payload = decode_jwt(token)

                    if payload:
                        rol = payload.get("rol")

                        if rol == "Administrador":
                            return 1
                        elif rol == "Cliente":
                            return 2
                        elif rol == "Agente":
                            return 3
                        else:
                            print("⚠️ Rol no reconocido:", rol)
                            time.sleep(4)
                            return
                    else:
                        print("❌ Error al decodificar el token")
                        time.sleep(4)
                        return
                else:
                    print("❌ Token no encontrado")
                    time.sleep(4)
                    return

            elif response.status_code == 401:
                print("❌", response.json()["detail"])
            elif response.status_code == 422:
                print("⚠️ Correo no tiene un formato válido")
            elif response.status_code == 500:
                print("❌ Error interno del servidor")
            else:
                print("❌ Error desconocido")

            time.sleep(4)

        except Exception as e:
            print("❌ No se pudo conectar al servidor. Verifica si está encendido.")
            time.sleep(4)
            return

def main():
    while True:
        try:
            limpiarPantalla()
            BannerPrincipal()

            print("1. Login")
            print("2. Register")
            print("3. Salir")

            opcion = int(input("\nIngrese una opción: "))

            match opcion:
                case 1:
                    opcionRol = login()

                    if opcionRol == 1:
                        bannerAdmin()
                        time.sleep(2)
                    elif opcionRol == 2:
                        bannerClient()
                        time.sleep(2)
                    elif opcionRol == 3:
                        bannerAgent()
                        time.sleep(2)

                case 2:
                    print("Funcionalidad de registro aún no implementada.")
                    time.sleep(2)

                case 3:
                    print("👋 Saliendo del sistema...")
                    break

        except ValueError:
            print("⚠️ No se ingresó un número válido")
            time.sleep(2)

if __name__ == "__main__":
    main()
