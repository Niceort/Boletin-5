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
        equipos = self.num_equipos
        if equipos <= 1:
            return 0
        return equipos * (equipos - 1)

    @property
    def goles_totales(self):
        total = 0
        for equipo in self.equipos.values():
            total += equipo.goles_marcados
        return total

    @property
    def media_goles_por_partido(self):
        partidos = self.num_partidos
        if partidos <= 0:
            return 0.0
        return float(self.goles_totales) / float(partidos)

    @property
    def año_inicio(self):
        valor = str(self.identificador)
        try:
            return int(valor.split("-")[0])
        except Exception:
            return 0
