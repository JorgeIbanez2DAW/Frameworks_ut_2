import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection
from modelo.Usuario import Usuario
from modelo.BBDD_Error import BBDD_Error


def connection(config: dict[str, str]) -> PooledMySQLConnection | MySQLConnectionAbstract | None:
    try:
        return mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["usuario"],
            password=config["password"],
            database=config["database"]
        )
    except mysql.connector.Error:
        raise BBDD_Error("Error al conectarse a la base de datos")


def close(cnx: MySQLConnectionAbstract) -> None:
    try:
        cnx.close()
    except mysql.connector.Error:
        raise BBDD_Error("Error al desconectarse de la base de datos")


def add_usuario(cnx: MySQLConnectionAbstract, usuario: Usuario) -> None:
    cursor: None | MySQLCursorAbstract = None
    if usuario:
        try:
            cursor = cnx.cursor()
            sql = "INSERT INTO usuarios (nombre, apellido_1, apellido_2, fecha_nacimiento) VALUES (%s, %s, %s, %s)"
            data = (usuario.nombre, usuario.apellido_1, usuario.apellido_2, usuario.fecha_nacimiento)
            cursor.execute(sql, data)
            cnx.commit()
        except mysql.connector.Error:
            raise BBDD_Error("Error al insertar usuario")
        finally:
            if cursor is not None:
                cursor.close()


def get_usuario(cnx: MySQLConnectionAbstract, codigo: str) -> Usuario | None:
    cursor: None | MySQLCursorAbstract = None
    try:
        cursor = cnx.cursor()
        sql = "SELECT nombre, apellido_1, apellido_2, fecha_nacimiento FROM usuarios WHERE cod = %s"
        data = (int(codigo),)
        cursor.execute(sql, data)
        datos = cursor.fetchone()
        if datos is not None:
            return Usuario(str(codigo), datos[0], datos[1], datos[2], datos[3])
    except mysql.connector.Error:
        raise BBDD_Error("Error al obtener usuario")
    finally:
        if cursor is not None:
            cursor.close()


def get_usuarios(cnx: MySQLConnectionAbstract, limit: int, offset: int) -> list[Usuario]:
    cursor: None | MySQLCursorAbstract = None
    usuarios: list = []
    try:
        cursor = cnx.cursor()
        sql = "SELECT * FROM usuarios ORDER BY cod LIMIT %s OFFSET %s"
        data = (limit, offset)
        cursor.execute(sql, data)
        for cod, nombre, apellido_1, apellido_2, fecha_nacimiento in cursor:
            usuarios.append(Usuario(str(cod), nombre, apellido_1, apellido_2, fecha_nacimiento))
        return usuarios
    except mysql.connector.Error:
        raise BBDD_Error("Error al obtener usuario")
    finally:
        if cursor is not None:
            cursor.close()


def update_usuario(cnx: MySQLConnectionAbstract, usuario: Usuario) -> None:
    cursor: None | MySQLCursorAbstract = None
    try:
        cursor = cnx.cursor()
        sql = "UPDATE usuarios SET nombre = %s, apellido_1 = %s, apellido_2 = %s, fecha_nacimiento = %s WHERE cod = %s"
        data = (usuario.nombre, usuario.apellido_1, usuario.apellido_2, usuario.fecha_nacimiento, usuario.cod)
        cursor.execute(sql, data)
        cnx.commit()
    except mysql.connector.Error:
        raise BBDD_Error("Error al actualizar usuario")
    finally:
        if cursor is not None:
            cursor.close()


def descargar_usuarios(cnx: MySQLConnectionAbstract, formato: str = "csv", limit: int = 10) -> str:
    formato = formato if formato in ["json", "csv", "yaml", "toml"] else "csv"
    cursor: None | MySQLCursorAbstract = None
    salida: str = ""
    offset: int = 0
    fin: bool = False
    usuarios: list[Usuario] = []

    try:
        cursor = cnx.cursor()
        while not fin:
            sql = "SELECT * FROM usuarios LIMIT %s OFFSET %s"
            data = (limit, offset)
            cursor.execute(sql, data)
            lista = cursor.fetchall()
            if not lista:
                fin = True
            else:
                for cod, nombre, apellido_1, apellido_2, fecha_nacimiento in lista:
                    usuarios.append(Usuario(str(cod), nombre, apellido_1, apellido_2, fecha_nacimiento))
            offset += limit
    except mysql.connector.Error:
        raise BBDD_Error("Error al descargar la bbdd")
    finally:
        if cursor is not None:
            cursor.close()

    match formato:
        case "csv":
            return "\n".join([usu.to_csv() for usu in usuarios])
        case "json":
            return "\n".join([usu.to_json() for usu in usuarios])
        case "yaml":
            return "\n".join([usu.to_yaml() for usu in usuarios])
        case "toml":
            return "\n".join([usu.to_toml() for usu in usuarios])


def borrar_usuario(cnx: MySQLConnectionAbstract, codigo: int) -> int:
    cursor: None | MySQLCursorAbstract = None
    try:
        cursor = cnx.cursor()
        sql = "DELETE FROM usuarios WHERE cod = %s"
        data = (int(codigo),)
        cursor.execute(sql, data)
        cnx.commit()
        return cursor.rowcount
    except mysql.connector.Error:
        raise BBDD_Error("Error al eliminar usuario")
    finally:
        if cursor is not None:
            cursor.close()
