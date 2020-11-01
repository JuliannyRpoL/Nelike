class Series:

    def __init__(self, nombre, puntuacion, descripcion, vista, link):
        self.nombre = nombre
        self.puntuacion = puntuacion
        self.descripcion = descripcion
        self.vista = vista
        self.link= link

    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())