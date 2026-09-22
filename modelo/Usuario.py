class Usuario:
    def __init__(self, cod, nombre, apellido_1, apellido_2, fecha_nacimiento):
        self._cod = Usuario._satnize(cod)
        self._nombre = Usuario._satnize(nombre)
        self._apellido_1 = Usuario._satnize(apellido_1)
        self._apellido_2 = Usuario._satnize(apellido_2)
        self._fecha_nacimiento = Usuario._satnize(fecha_nacimiento)

    def propiedades():
        pass

    def __seriealize__():
        pass

    def to_json():
        pass

    def to_csv():
        pass

    def to_yaml():
        pass

    def to_topml():
        pass
