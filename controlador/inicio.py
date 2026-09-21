
# Variables constantes de configuración (No vienen en el libro)
FILE_PATH: str = "conf.txt"
DEBUG: bool = True
ERROR_KEY: str = "error"


def run_app(configuracion: dict[str, str]) -> None:
    fin: bool = False

    if DEBUG:
        print(configuracion)
    if ERROR_KEY in configuracion.keys():
        print(configuracion["error"])
        return None
    return None


def cargar_configuracion() -> dict[str, str]:
    try:
        with open(FILE_PATH, "r") as f:
            return {
                "usuario": f.readline().strip().split("=")[1],
                "password": f.readline().strip().split("=")[1],
                "host": f.readline().strip().split("=")[1],
                "database": f.readline().strip().split("=")[1],
                "admin_pw": f.readline().strip().split("=")[1]
            }
    except FileExistsError as e:
        return {"error": "error de fichero"}
    except Exception:
        return {"error": "error inesperado"}
