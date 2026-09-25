class Usuario:
    def __init__(self, cod: str, nombre: str, apellido_1: str, apellido_2: str, fecha_nacimiento: str):
        self._cod = Usuario._satinize(cod)
        self._nombre = Usuario._satinize(nombre)
        self._apellido_1 = Usuario._satinize(apellido_1)
        self._apellido_2 = Usuario._satinize(apellido_2)
        self._fecha_nacimiento = Usuario._satinize(fecha_nacimiento)

    def __str__(self):
        return f"{self._cod} {self._nombre} {self._apellido_1} {self._apellido_2} {self._fecha_nacimiento}"

    @staticmethod
    def _satinize(value: str):
        return value.replace(";", "")

    @property
    def cod(self):
        return self._cod

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido_1(self):
        return self._apellido_1

    @property
    def apellido_2(self):
        return self._apellido_2

    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento

    def __serialize__(self):
        return {
            "cod": self._cod,
            "nombre": self._nombre,
            "apellido_1": self._apellido_1,
            "apellido_2": self._apellido_2,
            "fecha_nacimiento": self._fecha_nacimiento
        }

    def to_json(self) -> str:
        return str(self.__serialize__())

    def to_csv(self) -> str:
        return f"{self.cod};{self.nombre};{self.apellido_1};{self.apellido_2};{self.fecha_nacimiento}"

    def to_yaml(self) -> str:
        return f"cod: {self.cod}\nnombre: {self.nombre}\napellido_1: {self.apellido_1}\napellido_2: {self.apellido_2}" \
               f"\nfecha_nacimiento: {self.fecha_nacimiento}"

    def to_toml(self) -> str:
        return f'cod = "{self.cod}"\nnombre = "{self.nombre}"\napellido_1 = "{self.apellido_1}"'\
               '\napellido_2 = "{self.apellido_2}"\nfecha_nacimiento = "{self.fecha_nacimiento}"'
