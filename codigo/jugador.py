class Jugador:
    """Entidad de jugador para una temporada y equipo concretos."""

    def __init__(self, datos, trazabilidad):
        self._trazabilidad = trazabilidad
        self.nombre = str(datos.get("jugador", "")).strip()
        self.equipo = str(datos.get("equipo", "")).strip()
        self.temporada = str(datos.get("temporada", "")).strip()

        self.partidos_jugados = int(datos.get("partidos_jugados", 0) or 0)
        self.partidos_titular = int(datos.get("partidos_titular", 0) or 0)
        self.partidos_suplente = int(datos.get("partidos_suplente", 0) or 0)
        self.partidos_completos = int(datos.get("partidos_completos", 0) or 0)
        self.minutos = int(datos.get("minutos", 0) or 0)
        self.goles = int(datos.get("goles", 0) or 0)
        self.amarillas = int(datos.get("amarillas", 0) or 0)
        self.rojas = int(datos.get("rojas", 0) or 0)
        self.cambios = int(datos.get("cambios", 0) or 0)

    @property
    def tarjetas_totales(self):
        return self.amarillas + self.rojas

    @property
    def veces_sustituido(self):
        return self.cambios

    @property
    def goles_por_minuto(self):
        if self.minutos <= 0:
            return 0.0
        return float(self.goles) / float(self.minutos)

    @property
    def es_revulsivo(self):
        return self.partidos_suplente > self.partidos_titular

    @property
    def partidos_impolutos(self):
        # Si no vio tarjetas, contamos todos sus partidos como limpios.
        if self.tarjetas_totales == 0:
            return self.partidos_jugados
        return 0

    def resumen(self):
        return "{0} ({1} {2})".format(self.nombre, self.equipo, self.temporada)
