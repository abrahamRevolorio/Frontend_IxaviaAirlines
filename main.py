import requests
import os
import time
import base64
import json
import questionary
from colorama import Fore, Style, init

init(autoreset=True)

url = "http://127.0.0.1:8000/"

def limpiarPantalla():
    os.system("cls" if os.name == "nt" else "clear")

def BannerPrincipal():
    print(Fore.CYAN + "* " * 40)
    print(Fore.YELLOW + "IXAVIA AIRLINES".center(80))
    print(Fore.CYAN + "* " * 40 + "\n")

def bannerAdmin():
    print(Fore.MAGENTA + "* " * 40)
    print(Fore.YELLOW + "Administrador".center(80))
    print(Fore.MAGENTA + "* " * 40 + "\n")

def bannerClient():
    print(Fore.MAGENTA + "* " * 40)
    print(Fore.YELLOW + "Usuario".center(80))
    print(Fore.MAGENTA + "* " * 40 + "\n")

def bannerAgent():
    print(Fore.MAGENTA + "* " * 40)
    print(Fore.YELLOW + "Agente".center(80))
    print(Fore.MAGENTA + "* " * 40 + "\n")

def decode_jwt(token):
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')
        def fix_padding(b64_string):
            return b64_string + '=' * (-len(b64_string) % 4)
        payload_json = base64.urlsafe_b64decode(fix_padding(payload_b64)).decode()
        return json.loads(payload_json)
    except Exception as e:
        print(Fore.RED + "Error al decodificar el token:", e)
        return None

def login():
    while True:
        try:
            limpiarPantalla()
            email = input(Fore.CYAN + "Ingrese su email: ")
            password = input(Fore.CYAN + "Ingrese su contraseña: ")
            response = requests.post(url + "auth/login", json={"email": email, "password": password})

            if response.status_code == 200:
                print(Fore.GREEN + "✔ Login exitoso")
                token = response.json().get("accessToken")
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
                            print(Fore.YELLOW + "Rol no reconocido:", rol)
                            time.sleep(4)
                            return
                    else:
                        print(Fore.RED + "Error al decodificar el token")
                        time.sleep(4)
                        return
                else:
                    print(Fore.RED + "Token no encontrado")
                    time.sleep(4)
                    return
            elif response.status_code == 401:
                print(Fore.RED + "✖", response.json()["detail"])
            elif response.status_code == 422:
                print(Fore.YELLOW + "⚠ Correo no tiene un formato válido")
            elif response.status_code == 500:
                print(Fore.RED + "✖ Error interno del servidor")
                return
            else:
                print(Fore.RED + "✖ Error desconocido")
                return
            time.sleep(4)
        except Exception:
            print(Fore.RED + "✖ No se pudo conectar al servidor. Verifica si está encendido.")
            time.sleep(4)
            return

def register():
    while True:
        try:
            limpiarPantalla()

            while True:
                email = input(Fore.CYAN + "Ingrese su email: ")
                if "@" not in email:
                    print(Fore.YELLOW + "⚠ Correo no tiene un formato válido")
                else:
                    break

            limpiarPantalla()

            password = input(Fore.CYAN + "Ingrese su contraseña: ")

            limpiarPantalla()

            while True:
                dpi = input(Fore.CYAN + "Ingrese su DPI: ")
                if len(dpi) != 13:
                    print(Fore.YELLOW + "⚠ DPI no tiene un formato válido")
                else:
                    break

            limpiarPantalla()

            nombres = input(Fore.CYAN + "Ingrese sus nombres: ")

            limpiarPantalla()

            apellidos = input(Fore.CYAN + "Ingrese sus apellidos: ")

            limpiarPantalla()

            while True:
                telefono = input(Fore.CYAN + "Ingrese su teléfono: ")
                if len(telefono) > 10:
                    print(Fore.YELLOW + "⚠ Teléfono no tiene un formato válido")
                else:
                    break

            limpiarPantalla()

            direccion = input(Fore.CYAN + "Ingrese su dirección: ")

            limpiarPantalla()

            while True:
                yearNacimiento = input(Fore.CYAN + "Ingrese su año de nacimiento (Ej: 2000): ")
                if len(yearNacimiento) != 4 or not yearNacimiento.isdigit():
                    print(Fore.YELLOW + "⚠ Año de nacimiento no válido")
                else:
                    break

            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                     "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            
            mesNacimiento = menuInteractivo("Seleccione su mes de nacimiento", meses)

            if mesNacimiento < 10:
                mesNacimiento = "0" + str(mesNacimiento)

            dias = [str(i) for i in range(1, 32)]

            diaNacimiento = menuInteractivo("Seleccione su día de nacimiento", dias)
            
            nacimiento = f'{yearNacimiento}-{mesNacimiento}-{diaNacimiento}'

            limpiarPantalla()

            nacionalidad = input(Fore.CYAN + "Ingrese su nacionalidad: ")

            limpiarPantalla()

            while True:
                telefonoEmergencia = input(Fore.CYAN + "Ingrese su teléfono de emergencia: ")
                if len(telefonoEmergencia) > 10:
                    print(Fore.YELLOW + "⚠ Teléfono de emergencia no válido")
                else:
                    break

            response = requests.post(url + "auth/register", json={
                "email": email,
                "password": password,
                "dpi": dpi,
                "nombres": nombres,
                "apellidos": apellidos,
                "telefono": telefono,
                "direccion": direccion,
                "nacimiento": nacimiento,
                "nacionalidad": nacionalidad,
                "telefonoEmergencia": telefonoEmergencia
            })
            if response.status_code in [200, 201]:
                print(Fore.GREEN + "✔ Registro exitoso")
            elif response.status_code == 409:
                print(Fore.YELLOW + "⚠ Email ya registrado")
            elif response.status_code == 500:
                print(Fore.RED + "✖ Error interno del servidor")
            else:
                print(Fore.RED + "✖ Error desconocido")
            time.sleep(4)
            return
        except Exception:
            print(Fore.RED + "✖ No se pudo conectar al servidor. Verifica si está encendido.")
            time.sleep(4)
            return

def menuInteractivo(titulo, opciones):
    seleccion = questionary.select(titulo, choices=opciones).ask()
    return opciones.index(seleccion) + 1

def main():
    while True:
        try:
            limpiarPantalla()
            BannerPrincipal()
            opcion = menuInteractivo("Seleccione una opción", ["1.Login", "2.Registro", "3.Salir"])
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
                    register()
                case 3:
                    print(Fore.CYAN + "Saliendo del sistema...")
                    break
        except ValueError:
            print(Fore.YELLOW + "⚠ No se ingresó un número válido")
            time.sleep(2)

if __name__ == "__main__":
    main()