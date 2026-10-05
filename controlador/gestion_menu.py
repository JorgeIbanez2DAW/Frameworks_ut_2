from modelo.Usuario import Usuario
from modelo.BBDD_Error import BBDD_Error
import modelo.bbdd as bbdd
import vista.menus as v_menus


def dar_de_alta(configuracion: dict[str, str], usuario: Usuario = None) -> None:
    cnx = None
    try:
        cnx = bbdd.connection(configuracion)
        bbdd.add_usuario(cnx, usuario)
        print("Añadido correctamente")
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def modificar(configuracion: dict[str, str], usuario_modificado: Usuario):
    cnx = None
    try:
        cnx = bbdd.connection(configuracion)
        bbdd.update_usuario(cnx, usuario_modificado)
        print("Modificado correctamente")
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def obtener(configuracion: dict[str, str], codigo: str) -> Usuario | None:
    cnx = None
    try:
        cnx = bbdd.connection(configuracion)
        usuario = bbdd.get_usuario(cnx, codigo)
        print("Obtenido correctamente")
        return usuario
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def descargar_bbdd(configuracion: dict[str, str], formato: str = "csv"):
    cnx = None
    try:
        cnx = bbdd.connection(configuracion)
        print(bbdd.descargar_usuarios(cnx, formato))
        bbdd.close(cnx)
        print("Descargado correctamente")
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def visualizar(configuracion: dict[str, str], limit: int = 10):
    cnx = None
    offset = 0
    fin = False

    try:
        cnx = bbdd.connection(configuracion)

        while not fin:
            usuarios = bbdd.get_usuarios(cnx, limit, offset)

            if len(usuarios) == 0:
                fin = True
            else:
                for usuario in usuarios:
                    print(usuario)

                if len(usuarios) < limit or not v_menus.get_continuar():
                    fin = True
                else:
                    offset += limit
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def dar_de_baja(configuracion: dict[str, str], codigo: str):
    cnx = None
    try:
        cnx = bbdd.connection(configuracion)
        lineas = bbdd.borrar_usuario(cnx, codigo)
        if lineas == 1:
            print("Se ha dado de baja correctamente")
        else:
            print("No existe el usuario")
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)
