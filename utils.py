import re

# Función para validar la contraseña
def validar_contrasena(contrasena):
    if len(contrasena) < 8:
        return False
    if not re.search("[a-zA-Z]", contrasena):
        return False
    if not re.search("[0-9]", contrasena):
        return False
    return True
