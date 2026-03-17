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
        total = 0
        for jugador in self.jugadores:
            total += jugador.goles
        return total

    @property
    def num_jugadores(self):
        return len(self.jugadores)

    @property
    def partidos_jugados(self):
        mayor = 0
        for jugador in self.jugadores:
            if jugador.partidos_jugados > mayor:
                mayor = jugador.partidos_jugados
        if self.partidos_temporada > mayor:
            return self.partidos_temporada
        return mayor

    @property
    def total_tarjetas(self):
        total = 0
        for jugador in self.jugadores:
            total += jugador.tarjetas_totales
        return total
