from modelo.Usuario import Usuario
from modelo.BBDD_Error import BBDD_Error
import modelo.bbdd as bbdd


def dar_de_alta(configuracion: dict[str, str], usuario: Usuario = None) -> None:
    try:
        cnx = bbdd.conecction(configuracion)
        bbdd.add_usuario(cnx, usuario)
        bbdd.close(cnx)
        print("Añadido correctamente")
    except BBDD_Error as e:
        print(e)


def descargar_bbdd(configuracion: dict[str, str], formato: str = "csv"):
    try:
        cnx = bbdd.coneccion(configuracion)
        print(bbdd.descargar_usuarios(cnx, formato))
        bbdd.close(cnx)
        print("Descargado correctamente")
    except BBDD_Error as e:
        print(e)


def visualizar(configuracion: dict[str, str]):
    print("Ver")


def dar_de_baja(configuracion: dict[str, str], usuario: Usuario):
    print("Baja")


def modificar(configuracion: dict[str, str], usuario: Usuario, usuario_modificado: Usuario):
    print("Modificar")
