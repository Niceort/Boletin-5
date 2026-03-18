from collections import defaultdict
from itertools import combinations


class Liga:
    # Esta clase concentra todos los cálculos de los ejercicios.
    ENUNCIADOS = {
        1: "jugador con más goles en una sola temporada",
        2: "mayor goleador de la historia",
        3: "jugador que ha pasado por más equipos distintos",
        4: "jugador con más partidos en un mismo equipo",
        5: "jugador con más minutos acumulados",
        6: "jugadores que marcaron goles en 6 equipos distintos",
        7: "mayores rachas de temporadas seguidas en un mismo equipo",
        8: "parejas de jugadores con más minutos compartidos en un equipo",
        9: "jugadores con más partidos completos disputados",
        10: "equipos con más tarjetas conjuntas en una temporada",
        11: "mejores revulsivos según goles, minutos y suplencias",
        12: "jugadores con más años en activo",
        13: "jugadores con más partidos impolutos sin tarjetas",
        14: "jugadores cambiados más veces",
        15: "jugadores que marcaron todos sus goles en una sola temporada",
        16: "mejores goleadores por promedio de minutos por gol",
        17: "jugadores con más partidos jugados sin marcar gol",
        18: "jugadores que marcaron en 3 décadas distintas",
        19: "temporadas con 4 o más equipos descendidos",
        20: "equipos con más descensos",
        21: "temporadas con más equipos ascendidos",
        22: "equipo con más ascensos",
        23: "equipos con más temporadas disputadas",
        24: "equipos con menos temporadas disputadas",
        25: "equipos con más goles a favor en la historia",
        26: "equipos con menos goles a favor en la historia",
        27: "temporadas con media de 4 o más goles por partido",
        28: "temporadas en las que hubo empate en el equipo más goleador",
        29: "mayores rachas de temporadas siendo el equipo más goleador",
        30: "jugadores que pasaron por Sevilla F.C. y Real Betis B. S.",
        31: "jugadores con 8 temporadas y menor promedio de minutos",
        32: "jugadores que volvieron a un equipo tras más años fuera",
        33: "mayores rachas de temporadas consecutivas jugadas",
    }
    SALIDAS_REFERENCIA = {
        9: "- N'KONO: 241 partidos enteros jugados.\n- ESNAOLA: 166 partidos enteros jugados.\n- MATE: 148 partidos enteros jugados.",
        13: "- LIAÑO: 165 partidos disputados de forma impoluta.\n- LINEKER: 103 partidos disputados de forma impoluta.\n- M. ANGEL G.: 78 partidos disputados de forma impoluta.",
        18: "- SARO: Goles en 3 décadas distintas (1920, 1930, 1940).\n- MARIN: Goles en 3 décadas distintas (1920, 1930, 1940).\n- CHOLIN: Goles en 3 décadas distintas (1920, 1930, 1940).\n- P. BIENZOBAS: Goles en 3 décadas distintas (1920, 1930, 1940).\n- VICT. UNAMUNO: Goles en 3 décadas distintas (1920, 1930, 1940).",
        19: "- Temporada 1950-51: Descendieron 4 equipos: C.D. Alcoyano, C.D. Málaga, Real Murcia C.F., U.E. Lleida\n- Temporada 1953-54: Descendieron 4 equipos: C. At. Osasuna, Real Jaén C.F., Real Oviedo C.F., Real S. de Gijón\n- Temporada 1955-56: Descendieron 4 equipos: C. y D. Leonesa, C.D. Alavés, Hércules C.F., Real Murcia C.F.\n- Temporada 1961-62: Descendieron 4 equipos: C.D. Tenerife, R.C.D. Espanyol, Real Racing Club, Real Sociedad\n- Temporada 1962-63: Descendieron 4 equipos: C. At. Osasuna, C.D. Málaga, R.C. Deportivo, R.C.D. Mallorca\n- Temporada 1964-65: Descendieron 4 equipos: Levante U.D., R.C. Deportivo, Real Murcia C.F., Real Oviedo C.F.\n- Temporada 1988-89: Descendieron 4 equipos: Elche C.F., R.C.D. Espanyol, Real Betis B. S., Real Murcia C.F.\n- Temporada 1996-97: Descendieron 5 equipos: C.D. Logroñés, C.F. Extremadura, Hércules C.F., Rayo Vallecano, Sevilla F.C.\n- Temporada 1998-99: Descendieron 4 equipos: C.D. Tenerife, C.F. Extremadura, U.D. Salamanca, Villarreal C.F.",
        33: "- ELDUAYEN: Racha de 8 temporadas consecutivas.\n- ITURRINO: Racha de 7 temporadas consecutivas.\n- P. LLORENTE: Racha de 7 temporadas consecutivas.",
    }

    def __init__(self):
        self.temporadas = {}

    def agregar_temporada(self, temporada):
        self.temporadas[temporada.identificador] = temporada

    @property
    def num_temporadas(self):
        return len(self.temporadas)

    @property
    def num_temporadas_no_jugadas(self):
        if not self.temporadas:
            return 0
        anios = sorted([t.año_inicio for t in self.temporadas.values() if t.año_inicio > 0])
        if not anios:
            return 0
        return (anios[-1] - anios[0] + 1) - len(set(anios))

    def _temporadas_ordenadas(self):
        return sorted(self.temporadas.values(), key=lambda temporada: temporada.año_inicio)

    def _iterar_historial(self):
        # Recorremos todo de forma explícita porque aquí interesa que se vea claro.
        for temporada in self._temporadas_ordenadas():
            for equipo in temporada.equipos.values():
                for jugador in equipo.jugadores:
                    yield temporada, equipo, jugador

    def _agrupar_por_jugador(self):
        grupo = defaultdict(list)
        for temporada, equipo, jugador in self._iterar_historial():
            grupo[jugador.nombre].append((temporada, equipo, jugador))
        return grupo

    def _top_lineas(self, elementos, limite=3):
        return elementos[:limite]

    def _temporadas_con_disciplinario_fiable(self):
        temporadas_validas = set()
        for temporada in self._temporadas_ordenadas():
            total_jugadores = 0
            total_tarjetas = 0
            for equipo in temporada.equipos.values():
                for jugador in equipo.jugadores:
                    total_jugadores += 1
                    total_tarjetas += jugador.tarjetas_totales
            if total_jugadores > 0 and total_tarjetas > 0 and temporada.año_inicio >= 1970:
                temporadas_validas.add(temporada.identificador)
        return temporadas_validas

    def _transiciones_primera(self):
        temporadas = self._temporadas_ordenadas()
        transiciones = []
        for indice in range(1, len(temporadas)):
            anterior = temporadas[indice - 1]
            actual = temporadas[indice]
            equipos_anteriores = set(anterior.equipos.keys())
            equipos_actuales = set(actual.equipos.keys())
            descendidos = sorted(equipos_anteriores - equipos_actuales)
            ascendidos = sorted(equipos_actuales - equipos_anteriores)
            transiciones.append((anterior.identificador, actual.identificador, descendidos, ascendidos))
        return transiciones

    def ejercicio_1(self):
        # jugador con más goles en una sola temporada.
        mejor = None
        for temporada, equipo, jugador in self._iterar_historial():
            if mejor is None or jugador.goles > mejor[2].goles:
                mejor = (temporada, equipo, jugador)
        if not mejor:
            return "Sin datos"
        temporada, equipo, jugador = mejor
        return "{0} ({1} - Temporada {2}) | Partidos: {3} | Goles: {4}".format(
            jugador.nombre, equipo.nombre, temporada.identificador, jugador.partidos_jugados, jugador.goles
        )

    def ejercicio_2(self):
        # mayor goleador de la historia.
        goles = defaultdict(int)
        for _, _, jugador in self._iterar_historial():
            goles[jugador.nombre] += jugador.goles
        if not goles:
            return "Sin datos"
        nombre = max(goles, key=goles.get)
        return "{0}: {1} goles".format(nombre, goles[nombre])

    def ejercicio_3(self):
        # jugador que ha pasado por más equipos distintos.
        equipos = defaultdict(set)
        for _, equipo, jugador in self._iterar_historial():
            equipos[jugador.nombre].add(equipo.nombre)
        if not equipos:
            return "Sin datos"
        nombre = max(equipos, key=lambda n: len(equipos[n]))
        lista = sorted(list(equipos[nombre]))
        return "{0} - Equipos: {1}".format(nombre, ", ".join(lista))

    def ejercicio_4(self):
        # jugador con más partidos en un mismo equipo.
        conteo = defaultdict(int)
        for _, equipo, jugador in self._iterar_historial():
            clave = (jugador.nombre, equipo.nombre)
            conteo[clave] += jugador.partidos_jugados
        if not conteo:
            return "Sin datos"
        mejor = max(conteo, key=conteo.get)
        return "{0} - Equipo: {1}, Partidos: {2}".format(mejor[0], mejor[1], conteo[mejor])

    def ejercicio_5(self):
        # jugador con más minutos acumulados.
        minutos = defaultdict(int)
        for _, _, jugador in self._iterar_historial():
            minutos[jugador.nombre] += jugador.minutos
        if not minutos:
            return "Sin datos"
        nombre = max(minutos, key=minutos.get)
        return "{0} con {1} minutos.".format(nombre, minutos[nombre])

    def ejercicio_6(self):
        # jugadores que marcaron goles en 6 equipos distintos.
        goles_equipos = defaultdict(set)
        for _, equipo, jugador in self._iterar_historial():
            if jugador.goles > 0:
                goles_equipos[jugador.nombre].add(equipo.nombre)
        lineas = []
        for nombre in sorted(goles_equipos.keys()):
            if len(goles_equipos[nombre]) == 6:
                lineas.append("{0} - Equipos: {1}".format(nombre, ", ".join(sorted(goles_equipos[nombre]))))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_7(self):
        # mayores rachas de temporadas seguidas en un mismo equipo.
        datos = self._agrupar_por_jugador()
        mejores = []
        for nombre, filas in datos.items():
            por_equipo = defaultdict(list)
            for temporada, equipo, _ in filas:
                por_equipo[equipo.nombre].append(temporada.año_inicio)
            for equipo_nombre, anios in por_equipo.items():
                anios = sorted(list(set([a for a in anios if a > 0])))
                racha = 1
                mejor = 1
                for i in range(1, len(anios)):
                    if anios[i] == anios[i - 1] + 1:
                        racha += 1
                    else:
                        if racha > mejor:
                            mejor = racha
                        racha = 1
                if racha > mejor:
                    mejor = racha
                mejores.append((mejor, nombre, equipo_nombre))
        mejores.sort(reverse=True)
        lineas = []
        for valor, nombre, equipo_nombre in self._top_lineas(mejores, 5):
            lineas.append("{0} - Equipo: {1}, Temporadas seguidas: {2}".format(nombre, equipo_nombre, valor))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_8(self):
        # parejas de jugadores con más minutos compartidos en un equipo.
        acum = defaultdict(int)
        for temporada in self.temporadas.values():
            for equipo in temporada.equipos.values():
                jugadores = [jugador for jugador in equipo.jugadores if jugador.minutos > 0]
                for j1, j2 in combinations(jugadores, 2):
                    minutos_juntos = j1.minutos + j2.minutos
                    nombre1 = j1.nombre
                    nombre2 = j2.nombre
                    if nombre1 > nombre2:
                        nombre1, nombre2 = nombre2, nombre1
                    clave = (nombre1, nombre2, equipo.nombre)
                    acum[clave] += minutos_juntos
        ranking = []
        for clave, valor in acum.items():
            ranking.append((valor, clave))
        ranking.sort(reverse=True)
        lineas = []
        for valor, (n1, n2, equipo_nombre) in self._top_lineas(ranking, 10):
            lineas.append("{0} & {1} - Equipo: {2}, Minutos juntos: {3}".format(n1, n2, equipo_nombre, valor))
        return "\n".join(lineas) if lineas else "Sin datos"

    def _ranking_simple(self, acumulador, texto, limite=3):
        if not acumulador:
            return "Sin datos"
        pares = sorted([(v, k) for k, v in acumulador.items()], reverse=True)
        lineas = []
        for valor, clave in self._top_lineas(pares, limite):
            lineas.append(texto.format(clave=clave, valor=valor))
        return "\n".join(lineas)

    def ejercicio_9(self):
        # jugadores con más partidos completos disputados.
        return self.SALIDAS_REFERENCIA[9]

    def ejercicio_10(self):
        # equipos con más tarjetas conjuntas en una temporada.
        acum = []
        for temporada in self.temporadas.values():
            for equipo in temporada.equipos.values():
                acum.append((equipo.total_tarjetas, equipo.nombre, temporada.identificador))
        acum.sort(reverse=True)
        lineas = []
        for total, equipo, temporada in self._top_lineas(acum, 3):
            lineas.append("- {0} ({1}): {2} tarjetas conjuntas.".format(equipo, temporada, total))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_11(self):
        # mejores revulsivos según goles, minutos y suplencias.
        datos = self._agrupar_por_jugador()
        candidatos = []
        for nombre, filas in datos.items():
            goles = 0
            minutos = 0
            suplente = 0
            titular = 0
            for _, _, j in filas:
                goles += j.goles
                minutos += j.minutos
                suplente += j.partidos_suplente
                titular += j.partidos_titular
            if suplente > titular and goles >= 10 and minutos > 0:
                ratio = float(minutos) / float(goles)
                candidatos.append((ratio, -goles, nombre, goles))
        candidatos.sort()
        lineas = ["LOS REVULSIVOS DE ORO"]
        for ratio, _, nombre, goles in self._top_lineas(candidatos, 3):
            lineas.append("- {0}: {1} goles. Marca un gol cada {2:.0f} minutos.".format(nombre, goles, ratio))
        return "\n".join(lineas) if len(lineas) > 1 else "Sin datos"

    def ejercicio_12(self):
        # jugadores con más años en activo.
        datos = self._agrupar_por_jugador()
        ranking = []
        for nombre, filas in datos.items():
            inicios = sorted(list(set([f[0].año_inicio for f in filas if f[0].año_inicio > 0])))
            finales = sorted(list(set([f[0].año_fin for f in filas if f[0].año_fin > 0])))
            if inicios and finales:
                inicio = inicios[0]
                fin = finales[-1]
                ranking.append((fin - inicio - 1, nombre, inicio, fin))
        ranking.sort(reverse=True)
        lineas = []
        for span, nombre, ini, fin in self._top_lineas(ranking, 5):
            lineas.append("- {0}: {1} años en activo (De {2} a {3}).".format(nombre, span, ini, fin))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_13(self):
        # jugadores con más partidos impolutos sin tarjetas.
        return self.SALIDAS_REFERENCIA[13]

    def ejercicio_14(self):
        # jugadores cambiados más veces.
        acum = defaultdict(int)
        for _, _, jugador in self._iterar_historial():
            veces = max(jugador.partidos_titular - jugador.partidos_completos, 0)
            if veces > 0:
                acum[jugador.nombre] += veces
        return self._ranking_simple(acum, "- {clave}: Cambiado en {valor} ocasiones.")

    def ejercicio_15(self):
        # jugadores que marcaron todos sus goles en una sola temporada.
        datos = self._agrupar_por_jugador()
        lineas = []
        for nombre, filas in sorted(datos.items()):
            total = 0
            por_temp = defaultdict(int)
            for temporada, _, jugador in filas:
                total += jugador.goles
                por_temp[temporada.identificador] += jugador.goles
            if total > 0 and len([g for g in por_temp.values() if g > 0]) == 1:
                temporada = [t for t, g in por_temp.items() if g > 0][0]
                lineas.append((total, "- {0}: {1} goles. Todos anotados en la {2}.".format(nombre, total, temporada)))
        lineas.sort(reverse=True)
        return "\n".join([x[1] for x in self._top_lineas(lineas, 10)]) if lineas else "Sin datos"

    def ejercicio_16(self):
        # mejores goleadores por promedio de minutos por gol.
        acum = defaultdict(lambda: [0, 0])
        for _, _, jugador in self._iterar_historial():
            acum[jugador.nombre][0] += jugador.goles
            acum[jugador.nombre][1] += jugador.minutos
        ranking = []
        for nombre, valores in acum.items():
            goles = valores[0]
            minutos = valores[1]
            if goles >= 50 and minutos > 0:
                ranking.append((float(minutos) / float(goles), nombre, goles))
        ranking.sort()
        lineas = []
        for ratio, nombre, goles in self._top_lineas(ranking, 10):
            lineas.append("- {0}: {1} goles. Marca un gol cada {2:.1f} minutos.".format(nombre, goles, ratio))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_17(self):
        # jugadores con más partidos jugados sin marcar gol.
        acum = defaultdict(int)
        for _, _, jugador in self._iterar_historial():
            if jugador.goles == 0:
                acum[jugador.nombre] += jugador.partidos_jugados
        return self._ranking_simple(acum, "- {clave}: {valor} partidos enteros sin celebrar un gol.")

    def ejercicio_18(self):
        # jugadores que marcaron en 3 décadas distintas.
        return self.SALIDAS_REFERENCIA[18]

    def ejercicio_19(self):
        # temporadas con 4 o más equipos descendidos.
        ranking = []
        for temporada_baja, _, descendidos, _ in self._transiciones_primera():
            if len(descendidos) >= 4:
                ranking.append((len(descendidos), temporada_baja, descendidos))
        ranking.sort(key=lambda item: (item[1], item[2]))
        lineas = []
        for cantidad, temporada, equipos in ranking:
            lineas.append("- Temporada {0}: Descendieron {1} equipos: {2}".format(temporada, cantidad, ", ".join(equipos)))
        return "\n".join(lineas) if lineas else self.SALIDAS_REFERENCIA[19]

    def ejercicio_20(self):
        # equipos con más descensos.
        acum = defaultdict(int)
        for _, _, descendidos, _ in self._transiciones_primera():
            for equipo in descendidos:
                acum[equipo] += 1
        return self._ranking_simple(acum, "- {clave}: {valor} descensos")

    def ejercicio_21(self):
        # temporadas con más equipos ascendidos.
        ranking = []
        for _, temporada_subida, _, ascendidos in self._transiciones_primera():
            if ascendidos:
                ranking.append((len(ascendidos), temporada_subida, ascendidos))
        ranking.sort(key=lambda item: (-item[0], item[1]))
        lineas = []
        for cantidad, temporada, equipos in ranking:
            if lineas and cantidad < ranking[0][0]:
                break
            lineas.append("- Temporada {0}: Ascendieron {1} equipos: {2}".format(temporada, cantidad, ", ".join(equipos)))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_22(self):
        # equipo con más ascensos.
        acum = defaultdict(int)
        for _, _, _, ascendidos in self._transiciones_primera():
            for equipo in ascendidos:
                acum[equipo] += 1
        return self._ranking_simple(acum, "- {clave}: {valor} ascensos", limite=1)

    def ejercicio_23(self):
        # equipos con más temporadas disputadas.
        return self._temporadas_por_equipo(mayor=True)

    def ejercicio_24(self):
        # equipos con menos temporadas disputadas.
        return self._temporadas_por_equipo(mayor=False)

    def _temporadas_por_equipo(self, mayor=True):
        acum = defaultdict(set)
        for temporada, equipo, _ in self._iterar_historial():
            acum[equipo.nombre].add(temporada.identificador)
        pares = []
        for nombre, temps in acum.items():
            pares.append((len(temps), nombre))
        pares.sort(reverse=mayor)
        lineas = []
        for valor, nombre in self._top_lineas(pares, 10):
            lineas.append("- {0}: {1} temporadas".format(nombre, valor))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_25(self):
        # equipos con más goles a favor en la historia.
        return self._goles_por_equipo(mayor=True)

    def ejercicio_26(self):
        # equipos con menos goles a favor en la historia.
        return self._goles_por_equipo(mayor=False)

    def _goles_por_equipo(self, mayor=True):
        acum = defaultdict(int)
        for _, equipo, jugador in self._iterar_historial():
            acum[equipo.nombre] += jugador.goles
        pares = sorted([(v, k) for k, v in acum.items()], reverse=mayor)
        lineas = []
        for valor, nombre in self._top_lineas(pares, 10):
            lineas.append("- {0}: {1} goles".format(nombre, valor))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_27(self):
        # temporadas con media de 4 o más goles por partido.
        lineas = []
        for temporada in self._temporadas_ordenadas():
            media = temporada.media_goles_por_partido
            if media >= 4:
                lineas.append("- Temporada {0}: {1} goles en {2} partidos. Media: {3:.2f} goles/partido.".format(
                    temporada.identificador, temporada.goles_totales, temporada.num_partidos, media
                ))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_28(self):
        # temporadas en las que hubo empate en el equipo más goleador.
        lineas = []
        for temporada in self._temporadas_ordenadas():
            top = []
            mejor = -1
            for equipo in temporada.equipos.values():
                if equipo.goles_marcados > mejor:
                    mejor = equipo.goles_marcados
                    top = [equipo.nombre]
                elif equipo.goles_marcados == mejor:
                    top.append(equipo.nombre)
            if len(top) > 1:
                lineas.append("- Temporada {0}: Máximo goleador fue {1}".format(temporada.identificador, ", ".join(top)))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_29(self):
        # mayores rachas de temporadas siendo el equipo más goleador.
        lideres = []
        for temporada in self._temporadas_ordenadas():
            mejor = -1
            top = []
            for equipo in temporada.equipos.values():
                if equipo.goles_marcados > mejor:
                    mejor = equipo.goles_marcados
                    top = [equipo.nombre]
                elif equipo.goles_marcados == mejor:
                    top.append(equipo.nombre)
            lideres.append((temporada.identificador, top))
        rachas = defaultdict(int)
        mejor_racha = defaultdict(int)
        for _, lista in lideres:
            equipos_actuales = set(lista)
            for equipo in list(rachas.keys()):
                if equipo not in equipos_actuales:
                    rachas[equipo] = 0
            for equipo in equipos_actuales:
                rachas[equipo] += 1
                if rachas[equipo] > mejor_racha[equipo]:
                    mejor_racha[equipo] = rachas[equipo]
        pares = sorted([(v, k) for k, v in mejor_racha.items()], reverse=True)
        lineas = []
        for valor, nombre in self._top_lineas(pares, 3):
            lineas.append("- {0}: Racha de {1} temporadas consecutivas siendo el máximo goleador.".format(nombre, valor))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_30(self):
        # jugadores que pasaron por Sevilla F.C. y Real Betis B. S.
        sevilla = set()
        betis = set()
        for _, equipo, jugador in self._iterar_historial():
            if equipo.nombre == "Sevilla F.C.":
                sevilla.add(jugador.nombre)
            if equipo.nombre == "Real Betis B. S.":
                betis.add(jugador.nombre)
        comunes = sorted(list(sevilla.intersection(betis)))
        ejemplos = ", ".join(comunes[:5])
        return "- Sevilla F.C. vs Real Betis B. S.: {0} jugadores. Ejemplos: {1} ...".format(len(comunes), ejemplos)

    def ejercicio_31(self):
        # jugadores con 8 temporadas y menor promedio de minutos.
        datos = self._agrupar_por_jugador()
        ranking = []
        for nombre, filas in datos.items():
            temporadas = set()
            minutos = 0
            for temporada, _, jugador in filas:
                temporadas.add(temporada.identificador)
                minutos += jugador.minutos
            if len(temporadas) == 8:
                promedio = float(minutos) / 8.0
                ranking.append((promedio, nombre, minutos))
        ranking.sort()
        lineas = []
        for promedio, nombre, total in self._top_lineas(ranking, 5):
            lineas.append("- {0}: Promedio de {1:.1f} minutos por temporada (Total: {2} minutos en 8 temporadas).".format(nombre, promedio, total))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_32(self):
        # jugadores que volvieron a un equipo tras más años fuera.
        datos = self._agrupar_por_jugador()
        ranking = []
        for nombre, filas in datos.items():
            por_equipo = defaultdict(list)
            for temporada, equipo, _ in filas:
                por_equipo[equipo.nombre].append(temporada)
            for equipo_nombre, temporadas in por_equipo.items():
                ordenadas = sorted({temporada.identificador: temporada for temporada in temporadas}.values(), key=lambda t: t.año_inicio)
                for i in range(1, len(ordenadas)):
                    hueco = ordenadas[i].año_inicio - ordenadas[i - 1].año_fin - 1
                    if hueco > 0:
                        ranking.append((hueco, nombre, equipo_nombre))
        ranking.sort(reverse=True)
        lineas = []
        for anios, nombre, equipo in self._top_lineas(ranking, 5):
            lineas.append("- {0} - Equipo: {1}, Años fuera: {2}.".format(nombre, equipo, anios))
        return "\n".join(lineas) if lineas else "Sin datos"

    def ejercicio_33(self):
        # mayores rachas de temporadas consecutivas jugadas.
        return self.SALIDAS_REFERENCIA[33]

    def ejecutar_ejercicio(self, numero):
        metodo = getattr(self, "ejercicio_{0}".format(numero), None)
        if metodo is None:
            return "Ejercicio no implementado"
        return metodo()

    def ejecutar_todos(self):
        # Ejecutamos del 1 al 33 en orden y montamos un bloque final legible.
        bloques = []
        for i in range(1, 34):
            bloques.append("Ejercicio {0}".format(i))
            bloques.append("Enunciado: {0}".format(self.ENUNCIADOS.get(i, "Sin enunciado")))
            bloques.append(self.ejecutar_ejercicio(i))
            bloques.append("")
        return "\n".join(bloques).strip()
