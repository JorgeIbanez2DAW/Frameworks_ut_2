import vista.menus as v_menus
from controlador.gestion_menu import dar_de_alta, dar_de_baja, descargar_bbdd, modificar, obtener, visualizar


def cargar_configuracion() -> dict[str, str]:
    file_path: str = "conf.txt"

    try:
        with open(file_path, "r") as f:
            return {
                "usuario": f.readline().strip().split("=")[1],
                "password": f.readline().strip().split("=")[1],
                "host": f.readline().strip().split("=")[1],
                "port": f.readline().strip().split("=")[1],
                "database": f.readline().strip().split("=")[1],
                "admin_pw": f.readline().strip().split("=")[1],
                "debug": f.readline().strip().split("=")[1]
            }
    except FileNotFoundError:
        return {"error": "error de fichero"}
    except Exception:
        return {"error": "error inesperado"}


def run_app(configuracion: dict[str, str]) -> None:
    fin: bool = False

    if configuracion["debug"].lower() == "true":
        conf_debug = configuracion.copy()
        conf_debug["admin_pw"] = "[OCULTO]"
        conf_debug["password"] = "[OCULTO]"
        print(conf_debug)
    if "error" in configuracion:
        print(configuracion["error"])
        return None

    while not fin:
        v_menus.imprimir_menu()
        opcion = v_menus.pedir_opcion()
        if opcion == 6:
            fin = True
        elif opcion == 1:
            usuario = v_menus.get_usuario()
            if usuario is not None and v_menus.pedir_confirmacion(usuario):
                dar_de_alta(configuracion, usuario)
        elif opcion == 2:
            codigo = v_menus.get_codigo_usuario()
            usuario = obtener(configuracion, codigo)
            if usuario is not None and v_menus.pedir_confirmacion(usuario):
                usuario_modificado = v_menus.get_modificar_usuario(usuario)
                modificar(configuracion, usuario_modificado)
        elif opcion == 3:
            codigo = v_menus.get_codigo_usuario()
            usuario = obtener(configuracion, codigo)
            if usuario is not None and v_menus.pedir_confirmacion(usuario):
                dar_de_baja(configuracion, usuario)
        elif opcion == 4:
            visualizar(configuracion)
        elif opcion == 5:
            formato = v_menus.get_formato()
            descargar_bbdd(configuracion, formato)
    return None
