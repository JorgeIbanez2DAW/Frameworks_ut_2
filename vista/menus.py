from modelo.Usuario import Usuario

OPCIONES_MENU: dict[str, int] = {
    "Alta": 1,
    "Modificar": 2,
    "Baja": 3,
    "Ver": 4,
    "Descarga": 5,
    "Salir": 6
}

NO_OPCION: int = -1


def imprimir_menu() -> None:
    print("*  MENU  *")
    print("_" * 10)
    for opcion, valor in OPCIONES_MENU.items():
        print(f"{valor}: {opcion}")
    print("_" * 10, "\n")


def pedir_opcion() -> int:
    return int(input("¿Opcion?"))


def get_opcion(opcion: str) -> int:
    return OPCIONES_MENU[opcion] if opcion in OPCIONES_MENU else NO_OPCION


def get_usuario() -> Usuario:
    print("Introduce los datos del usuario:")
    nombre = input("Nombre: ")
    apellido_1 = input("Primer Apellido: ")
    apellido_2 = input("Segundo Apellido: ")
    fecha_nacimiento = input("Fecha de Nacimiento (DD/MM/AAAA): ")
    return Usuario("-", nombre, apellido_1, apellido_2, fecha_nacimiento)


def get_formato() -> str:
    formato: str = ""
    while (formato := input("Formato (json/csv/yaml/toml): ").lower()) not in ["json", "csv", "yaml", "toml"]:
        print("Introduce el formato deseado (json/csv/yaml/toml)")
    return formato
