from modelo.Usuario import Usuario


def imprimir_menu() -> None:
    opciones_menu: dict[str, int] = {
        "Alta": 1,
        "Modificar": 2,
        "Baja": 3,
        "Ver": 4,
        "Descarga": 5,
        "Salir": 6
    }

    print("\n*  MENU  *")
    print("_" * 10)
    for opcion, valor in opciones_menu.items():
        print(f"{valor}: {opcion}")
    print("_" * 10, "\n")


def pedir_opcion() -> int:
    return int(input("¿Opción? > "))


def imprimir_mensajes(opcion: int) -> None:
    match opcion:
        case 1:
            print("Añadido correctamente")
        case 2:
            print("Modificado correctamente")
        case 3:
            print("Descargado correctamente")
        case 4:
            print("Se ha dado de baja correctamente")
        case 5:
            print("No existe el usuario")


def imprimir(informacion: str | Usuario) -> None:
    print(informacion)


def get_opcion(opcion: str) -> int:
    return OPCIONES_MENU[opcion] if opcion in OPCIONES_MENU else NO_OPCION


def get_usuario() -> Usuario:
    print("Introduce los datos del usuario:")
    nombre = input("Nombre: ")
    apellido_1 = input("Primer Apellido: ")
    apellido_2 = input("Segundo Apellido: ")
    fecha_nacimiento = input("Fecha de Nacimiento (DD/MM/AAAA): ")
    return Usuario("-", nombre, apellido_1, apellido_2, fecha_nacimiento)


def get_codigo_usuario() -> str:
    cod = input("Introduce el código del usuario: ")
    return cod


def pedir_confirmacion(usuario: Usuario) -> bool:
    print("Usuario indicado:", usuario)
    opcion = input("¿Desea confirmar la acción? (s/n): ").lower()
    return opcion == "s" or opcion == "si"


def get_continuar() -> bool:
    opcion = input("¿Desear visualizar los siguientes? (s/n): ").lower()
    return opcion == "s" or opcion == "si"


def get_modificar_usuario(usuario: Usuario) -> Usuario:
    print("Introduce los datos a cambiar del usuario, en caso de no querer modificarlo, pulse enter:")
    nombre = input(f"Nombre actual: {usuario.nombre} "
                   f"-> Nuevo nombre: ") or usuario.nombre
    apellido_1 = input(f"Primer apellido actual: {usuario.apellido_1} "
                       f"-> Nuevo primer apellido: ") or usuario.apellido_1
    apellido_2 = input(f"Segundo apellido actual: {usuario.apellido_2} "
                       f"-> Nuevo segundo apellido: ") or usuario.apellido_2
    fecha_nacimiento = input(f"Fecha de nacimiento actual: {usuario.fecha_nacimiento} "
                             f"-> Nueva fecha (DD/MM/AAAA): ") or usuario.fecha_nacimiento

    return Usuario(usuario.cod, nombre, apellido_1, apellido_2, fecha_nacimiento)


def get_formato() -> str:
    formato: str = ""
    while (formato := input("Formato (json/csv/yaml/toml): ").lower()) not in ["json", "csv", "yaml", "toml"]:
        print("Introduce el formato deseado (json/csv/yaml/toml)")
    return formato
