import vista.menus as v_menus
from controlador.gestion_menu import dar_de_alta, dar_de_baja, descargar_bbdd, modificar, obtener, visualizar

FILE_PATH: str = "conf.txt"
DEBUG: bool = True
ERROR_KEY: str = "error"


def cargar_configuracion() -> dict[str, str]:
    try:
        with open(FILE_PATH, "r") as f:
            return {
                "usuario": f.readline().strip().split("=")[1],
                "password": f.readline().strip().split("=")[1],
                "host": f.readline().strip().split("=")[1],
                "port": f.readline().strip().split("=")[1],
                "database": f.readline().strip().split("=")[1],
                "admin_pw": f.readline().strip().split("=")[1]
            }
    except FileExistsError:
        return {"error": "error de fichero"}
    except Exception:
        return {"error": "error inesperado"}


def run_app(configuracion: dict[str, str]) -> None:
    fin: bool = False
    opcion: int = -1

    if DEBUG:
        print(configuracion)
    if ERROR_KEY in configuracion:
        print(configuracion["error"])
        return None

    while not fin:
        v_menus.imprimir_menu()
        opcion = v_menus.pedir_opcion()
        if opcion == v_menus.OPCIONES_MENU["Salir"]:
            fin = True
        elif opcion == v_menus.OPCIONES_MENU["Alta"]:
            usuario = v_menus.get_usuario()
            dar_de_alta(configuracion, usuario)
        elif opcion == v_menus.OPCIONES_MENU["Modificar"]:
            codigo = v_menus.get_codigo_usuario()
            usuario = obtener(configuracion, codigo)
            usuario_modificado = v_menus.get_modificar_usuario(usuario)
            modificar(configuracion, usuario_modificado)
        elif opcion == v_menus.OPCIONES_MENU["Baja"]:
            codigo1 = v_menus.get_codigo_usuario()
            print("Por seguridad, confirme el usuario a dar de baja")
            codigo2 = v_menus.get_codigo_usuario()
            if codigo1 == codigo2:
                dar_de_baja(configuracion, codigo1)
            else:
                print("Los usuarios no coinciden")
        elif opcion == v_menus.OPCIONES_MENU["Ver"]:
            visualizar(configuracion)
        elif opcion == v_menus.OPCIONES_MENU["Descarga"]:
            formato = v_menus.get_formato()
            descargar_bbdd(configuracion, formato)
            return None
