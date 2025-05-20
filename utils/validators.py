import re

def isNotEmpty(value: str) -> bool:
    return bool(value and value.strip())

def isValidEmail(email: str) -> tuple[bool, str]:
    if "@" not in email:
        return False, "El correo debe contener '@'"

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        return False, "Formato de correo inválido"
    
    return True, ""

def isSamePassword(pw1: str, pw2: str) -> bool:
    return pw1 == pw2


def isValidDpi(dpi: str) -> bool:
    return re.fullmatch(r"\d{13}", dpi) is not None

def isValidPhone(phone: str) -> bool:
    return re.fullmatch(r"\d{8}", phone) is not None
