class Equipo:
    def __init__(self, nombre, temporada):
        self.nombre = nombre
        self.temporada = temporada
        self.jugadores = []
        self.descendido = False
        self.ascendido = False
        self.partidos_temporada = 0

    def agregar_jugador(self, jugador):
        self.jugadores.append(jugador)

    @property
    def goles_marcados(self):
        total_goles = 0
        for jugador in self.jugadores:
            total_goles = total_goles + jugador.goles
        return total_goles

    @property
    def num_jugadores(self):
        return len(self.jugadores)

    @property
    def partidos_jugados(self):
        mayor_partidos = 0

        # Aquí buscamos el mayor valor para tener una referencia del equipo.
        for jugador in self.jugadores:
            if jugador.partidos_jugados > mayor_partidos:
                mayor_partidos = jugador.partidos_jugados

        if self.partidos_temporada > mayor_partidos:
            return self.partidos_temporada

        return mayor_partidos

    @property
    def total_tarjetas(self):
        total_tarjetas = 0
        for jugador in self.jugadores:
            total_tarjetas = total_tarjetas + jugador.tarjetas_totales
        return total_tarjetas
