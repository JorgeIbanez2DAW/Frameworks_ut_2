import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from modelo.Usuario import Usuario
from modelo.BBDD_Error import BBDD_Error


# Script de creación de la tabla
# CREATE TABLE `usuarios` (
#   `cod` int(11) NOT NULL,
#   `nombre` varchar(255) NOT NULL,
#   `apellido_1` varchar(255) NOT NULL,
#   `apellido_2` varchar(255) NOT NULL,
#   `fecha_nacimiento` varchar(255) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;
# ALTER TABLE `usuarios`
#   ADD PRIMARY KEY (`cod`);
# ALTER TABLE `usuarios`
#   MODIFY `cod` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
# COMMIT;


def coneccion(config: dict[str, str]) -> PooledMySQLConnection | MySQLConnectionAbstract | None:
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
    if usuario:
        try:
            cursor = cnx.cursor()
            sql = "INSERT INTO usuarios (nombre, apellido_1, apellido_2, fecha_nacimiento) VALUES (%s, %s, %s, %s)"
            data = (usuario.nombre, usuario.apellido_1, usuario.apellido_2, usuario.fecha_nacimiento)
            cursor.execute(sql, data)
            cnx.commit()
            cursor.close()
        except mysql.connector.Error:
            raise BBDD_Error("Error al insertar usuario")


def descargar_usuarios(cnx: MySQLConnectionAbstract, formato: str = "csv") -> str:
    formato = formato if formato in ["json", "csv", "yaml", "toml"] else "csv"
    salida: str = ""
    usuarios: list[Usuario] = []  # es más rápido al crear la cadena de texto pero consume más memoria
    try:
        cursor = cnx.cursor()
        query = "SELECT * FROM usuarios"
        cursor.execute(query)
        for cod, nombre, apellido_1, apellido_2, fecha_nacimiento in cursor:
            usuarios.append(Usuario(str(cod), nombre, apellido_1, apellido_2, fecha_nacimiento))
        cursor.close()
    except mysql.connector.Error:
        raise BBDD_Error("Error al descargar la bbdd")
    match formato:
        case "csv":
            return "\n".join([usu.to_csv() for usu in usuarios])
        case "json":
            return "\n".join([usu.to_json() for usu in usuarios])
        case "yaml":
            return "\n".join([usu.to_yaml() for usu in usuarios])
        case "toml":
            return "\n".join([usu.to_toml() for usu in usuarios])
    return salida


# borrar usuario ejemplo
# cnx.autocommit = True
# cursor = cnx.cursor()
# del_persona = "DELETE FROM personas WHERE cod = 1"
# print(del_persona)
# cursor.execute(del_persona)
# emp_no = cursor.lastrowid
# print(emp_no)
#  cnx.commit()  Ya no es necesario por el autocommit
# cursor.close()
