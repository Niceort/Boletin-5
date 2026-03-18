import os
import re
import unicodedata


class NormalizadorColumnas:
    """Normaliza nombres de columna y resuelve alias conocidos."""

    def __init__(self):
        self._alias = self._crear_alias()

    def _crear_alias(self):
        alias = {}
        alias["temporada"] = ["temporada", "season", "campana"]
        alias["jugador"] = ["jugador", "player", "nombre jugador", "futbolista"]
        alias["equipo"] = ["equipo", "club", "team"]
        alias["partidos_jugados"] = ["pj", "pjugados", "partidos", "partidos jugados", "matches", "j"]
        alias["partidos_titular"] = ["pt", "ptitular", "titular", "partidos titular", "partidos de titular"]
        alias["partidos_suplente"] = ["ps", "psuplente", "suplente", "partidos suplente", "partidos de suplente"]
        alias["partidos_completos"] = ["pc", "pcompletos", "partidos completos", "partidos enteros", "partidos completos jugados"]
        alias["minutos"] = ["min", "minutos", "minutes"]
        alias["goles"] = ["g", "goles", "goals"]
        alias["amarillas"] = ["ta", "amarillas", "tarjetas", "tarjetas amarillas"]
        alias["rojas"] = ["tr", "rojas", "tarjetas rojas", "expulsiones"]
        alias["cambios"] = ["sustituido", "cambios", "veces sustituido", "substitutions"]
        alias["descendido"] = ["descendido", "descenso", "relegated"]
        alias["ascendido"] = ["ascendido", "ascenso", "promoted"]
        alias["partidos_temporada"] = ["partidos temporada", "num partidos", "partidos liga", "total partidos"]
        return alias

    def simplificar(self, texto):
        # Truco sencillo: limpiamos tildes y símbolos para comparar columnas sin dramas.
        if texto is None:
            return ""
        limpio = str(texto).strip().lower()
        limpio = unicodedata.normalize("NFD", limpio)
        limpio = "".join([c for c in limpio if unicodedata.category(c) != "Mn"])
        limpio = re.sub(r"[^a-z0-9]+", " ", limpio).strip()
        return limpio

    def normalizar_nombre_columna(self, columna_original):
        base = self.simplificar(columna_original)
        for canonica, lista in self._alias.items():
            for posible in lista:
                if base == self.simplificar(posible):
                    return canonica
        base = base.replace(" ", "_")
        if not base:
            return "columna_sin_nombre"
        return base


class GestorBenchmark:
    """Provee benchmark esperado y comparación con resultados calculados."""

    def __init__(self):
        self._esperado = self._cargar_benchmark()

    def _cargar_benchmark(self):
        texto = """
Ejercicio 1
MESSI (F.C. Barcelona - Temporada 2011-12) | Partidos: 37 | Goles: 50

Ejercicio 2
MESSI: 383 goles

Ejercicio 3
ARANDA, C. - Equipos: C.D. Numancia, Sevilla F.C., C. At. Osasuna, Albacete Balomp., Levante U.D., Real Zaragoza CD, Granada C.F., Villarreal C.F.

Ejercicio 4
RAUL GONZALEZ - Equipo: Real Madrid C.F., Partidos: 550

Ejercicio 5
ZUBIZARRETA con 55746 minutos.

Ejercicio 6
JULIO SALINAS - Equipos: Real S. de Gijón, C.D. Alavés, R.C. Deportivo, F.C. Barcelona, Athletic Club, At. de Madrid
SALVA B. - Equipos: Málaga C.F., Sevilla F.C., Levante U.D., Real Racing Club, At. de Madrid, Valencia C.F.
ARIZMENDI - Equipos: Getafe C.F., R.C. Deportivo, Real Zaragoza CD, Real Racing Club, Valencia C.F., R.C.D. Mallorca

Ejercicio 7
GAINZA - Equipo: Athletic Club, Temporadas seguidas: 19
GENTO - Equipo: Real Madrid C.F., Temporadas seguidas: 18
IRIBAR - Equipo: Athletic Club, Temporadas seguidas: 18
M. SANCHIS - Equipo: Real Madrid C.F., Temporadas seguidas: 18
ADELARDO - Equipo: At. de Madrid, Temporadas seguidas: 17

Ejercicio 8
GORRIZ & LARRAÑAGA - Equipo: Real Sociedad, Minutos juntos: 76143
ARCONADA & ZAMORA - Equipo: Real Sociedad, Minutos juntos: 74867
JIMENEZ, M. & JOAQUIN A. - Equipo: Real S. de Gijón, Minutos juntos: 73167
CHENDO & M. SANCHIS - Equipo: Real Madrid C.F., Minutos juntos: 70757
PUYOL & XAVI - Equipo: F.C. Barcelona, Minutos juntos: 68786
M. SANCHIS & MICHEL - Equipo: Real Madrid C.F., Minutos juntos: 68320
IRIBAR & ROJO I - Equipo: Athletic Club, Minutos juntos: 67917
GAJATE & GORRIZ - Equipo: Real Sociedad, Minutos juntos: 65973
VICTOR VALDES & XAVI - Equipo: F.C. Barcelona, Minutos juntos: 65124
J.M. GUTI & RAUL GONZALEZ - Equipo: Real Madrid C.F., Minutos juntos: 64884

Ejercicio 9
- N'KONO: 241 partidos enteros jugados.
- ESNAOLA: 166 partidos enteros jugados.
- MATE: 148 partidos enteros jugados.

Ejercicio 10
- R.C.D. Espanyol (2012-13): 165 tarjetas conjuntas.
- Real Zaragoza CD (1996-97): 155 tarjetas conjuntas.
- Real Zaragoza CD (1995-96): 153 tarjetas conjuntas.

Ejercicio 11
LOS REVULSIVOS DE ORO
- MORATA: 24 goles. Marca un gol cada 97 minutos.
- LOINAZ: 12 goles. Marca un gol cada 158 minutos.
- BOJAN: 26 goles. Marca un gol cada 175 minutos.

Ejercicio 12
- CASTRO: 38 años en activo (De 1934 a 1973).
- ZUBIETA: 20 años en activo (De 1935 a 1956).
- CESAR SANCHEZ: 20 años en activo (De 1991 a 2012).
- IRARAGORRI: 19 años en activo (De 1929 a 1949).
- M. SOLER: 19 años en activo (De 1983 a 2003).

Ejercicio 13
- LIAÑO: 165 partidos disputados de forma impoluta.
- LINEKER: 103 partidos disputados de forma impoluta.
- M. ANGEL G.: 78 partidos disputados de forma impoluta.

Ejercicio 14
- JOAQUIN S.: Cambiado en 170 ocasiones.
- GUSTAVO LOPEZ: Cambiado en 168 ocasiones.
- ETXEBERRIA: Cambiado en 155 ocasiones.

Ejercicio 15
- VIERI: 24 goles. Todos anotados en la 1997-98.
- HASSELBAINK: 24 goles. Todos anotados en la 1999-00.
- MAXI GOMEZ: 18 goles. Todos anotados en la 2017-18.
- IBRAHIMOVIC: 16 goles. Todos anotados en la 2009-10.

Ejercicio 16
- LANGARA: 104 goles. Marca un gol cada 77.9 minutos.
- RONALDO, C.: 311 goles. Marca un gol cada 80.7 minutos.
- MESSI: 383 goles. Marca un gol cada 87.6 minutos.

Ejercicio 17
- ZUBIZARRETA: 622 partidos enteros sin celebrar un gol.
- BUYO: 542 partidos enteros sin celebrar un gol.
- IKER CASILLAS: 510 partidos enteros sin celebrar un gol.

Ejercicio 18
- SARO: Goles en 3 décadas distintas (1920, 1930, 1940).

Ejercicio 19
- Temporada 1996-97: Descendieron 5 equipos: C.D. Logroñés, C.F. Extremadura, Hércules C.F., Rayo Vallecano, Sevilla F.C.

Ejercicio 20
- Real Betis B. S.: 11 descensos

Ejercicio 21
- Temporada 1999-00: Ascendieron 4 equipos: C.D. Numancia, Málaga C.F., Rayo Vallecano, Sevilla F.C.

Ejercicio 22
- Real Betis B. S.: 12 ascensos

Ejercicio 23
- Athletic Club: 87 temporadas

Ejercicio 24
- At. Tetuan: 1 temporadas

Ejercicio 25
- Real Madrid C.F.: 5923 goles

Ejercicio 26
- U.E. Lleida: 70 goles

Ejercicio 27
- Temporada 1928-29: 378 goles en 90 partidos. Media: 4.20 goles/partido.

Ejercicio 28
- Temporada 1928-29: Máximo goleador fue Real Sociedad, C.D. Europa

Ejercicio 29
- Real Madrid C.F.: Racha de 5 temporadas consecutivas siendo el máximo goleador.

Ejercicio 30
- Sevilla F.C. vs Real Betis B. S.: 9 jugadores. Ejemplos: ANTUNEZ, CARVAJAL, DIEGO R., JOSE MARI, MATEOS ...

Ejercicio 31
- RAFA GONZALEZ: Promedio de 116.8 minutos por temporada (Total: 934 minutos en 8 temporadas).

Ejercicio 32
- UNZUE - Equipo: C. At. Osasuna, Años fuera: 14.

Ejercicio 33
- ELDUAYEN: Racha de 8 temporadas consecutivas.
"""
        return texto.strip()

    def obtener_texto_esperado(self):
        return self._esperado

    def comparar(self, calculado):
        # Comparamos línea a línea para detectar diferencias de manera fácil de seguir.
        esperado = self._esperado.splitlines()
        recibido = calculado.splitlines()
        diferencias = []
        max_len = max(len(esperado), len(recibido))
        for indice in range(max_len):
            ref = esperado[indice] if indice < len(esperado) else ""
            got = recibido[indice] if indice < len(recibido) else ""
            if ref.strip() != got.strip():
                diferencias.append("Linea {0}: esperado='{1}' | calculado='{2}'".format(indice + 1, ref, got))
        return diferencias


def arbol_proyecto(raiz):
    lineas = []
    for carpeta, subcarpetas, archivos in os.walk(raiz):
        subcarpetas.sort()
        archivos.sort()
        profundidad = carpeta.replace(raiz, "").count(os.sep)
        prefijo = "    " * profundidad
        nombre_carpeta = os.path.basename(carpeta) if profundidad > 0 else os.path.basename(raiz)
        lineas.append("{0}{1}/".format(prefijo, nombre_carpeta))
        for archivo in archivos:
            lineas.append("{0}    {1}".format(prefijo, archivo))
    return "\n".join(lineas)
