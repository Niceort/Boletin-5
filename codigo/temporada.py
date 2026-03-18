class Temporada:
    def __init__(self, identificador):
        self.identificador = identificador
        self.equipos = {}

    def agregar_equipo(self, equipo):
        self.equipos[equipo.nombre] = equipo

    @property
    def num_equipos(self):
        return len(self.equipos)

    @property
    def num_partidos(self):
        cantidad_equipos = self.num_equipos
        if cantidad_equipos <= 1:
            return 0
        return cantidad_equipos * (cantidad_equipos - 1)

    @property
    def goles_totales(self):
        total_goles = 0
        for equipo in self.equipos.values():
            total_goles = total_goles + equipo.goles_marcados
        return total_goles

    @property
    def media_goles_por_partido(self):
        partidos = self.num_partidos
        if partidos <= 0:
            return 0.0
        return float(self.goles_totales) / float(partidos)

    @property
    def año_inicio(self):
        texto = str(self.identificador)
        try:
            partes = texto.split("-")
            return int(partes[0])
        except Exception:
            return 0

    @property
    def año_fin(self):
        texto = str(self.identificador)
        try:
            partes = texto.split("-")
            inicio_texto = partes[0]
            fin_texto = partes[1]
            siglo = int(inicio_texto[:2]) * 100
            anio_fin = siglo + int(fin_texto)

            if anio_fin < int(inicio_texto):
                anio_fin = anio_fin + 100

            return anio_fin
        except Exception:
            return 0
