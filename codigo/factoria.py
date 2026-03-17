import os

from equipo import Equipo
from jugador import Jugador
from liga import Liga
from temporada import Temporada
from utilidades import NormalizadorColumnas
from validaciones import ValidadorDatos


class Factoria:
    def __init__(self):
        self.normalizador = NormalizadorColumnas()
        self.validador = ValidadorDatos()
        self.trazabilidad = {}
        self.filas_normalizadas = []
        self._ultima_ruta = ""

    def cargar_excel(self, ruta_excel):
        if not os.path.exists(ruta_excel):
            return False, "No existe el archivo: {0}".format(ruta_excel)
        self._ultima_ruta = ruta_excel
        try:
            import xlrd
        except Exception:
            return False, "No se encontró la librería 'xlrd'. Instale dependencias con: pip install -r requirements.txt"

        try:
            libro = xlrd.open_workbook(ruta_excel)
        except Exception as ex:
            return False, "Error al abrir .xls: {0}".format(ex)

        filas = []
        trazabilidad = {}
        for hoja in libro.sheets():
            if hoja.nrows == 0:
                continue
            encabezados = hoja.row_values(0)
            columnas = []
            for cabecera in encabezados:
                nombre = self.normalizador.normalizar_nombre_columna(cabecera)
                columnas.append(nombre)
                trazabilidad[nombre] = str(cabecera)

            for i in range(1, hoja.nrows):
                valores = hoja.row_values(i)
                fila = {}
                for indice, nombre_columna in enumerate(columnas):
                    valor = valores[indice] if indice < len(valores) else ""
                    fila[nombre_columna] = self._normalizar_valor(valor)
                if str(fila.get("jugador", "")).strip() == "":
                    continue
                if str(fila.get("equipo", "")).strip() == "":
                    continue
                if str(fila.get("temporada", "")).strip() == "":
                    continue
                filas.append(fila)

        self.trazabilidad = trazabilidad
        self.filas_normalizadas = filas
        return True, "Archivo leído correctamente. Filas válidas detectadas: {0}".format(len(filas))

    def _normalizar_valor(self, valor):
        if isinstance(valor, float):
            if int(valor) == valor:
                return int(valor)
            return valor
        if isinstance(valor, str):
            return valor.strip()
        return valor

    def validar_datos(self):
        if not self.filas_normalizadas:
            return False, ["No hay filas cargadas para validar."]
        return self.validador.validar(self.filas_normalizadas)

    def construir_liga(self):
        ok, errores = self.validar_datos()
        if not ok:
            return False, errores, None

        liga = Liga()
        for fila in self.filas_normalizadas:
            id_temporada = str(fila.get("temporada", ""))
            nombre_equipo = str(fila.get("equipo", ""))

            if id_temporada not in liga.temporadas:
                liga.agregar_temporada(Temporada(id_temporada))
            temporada = liga.temporadas[id_temporada]

            if nombre_equipo not in temporada.equipos:
                temporada.agregar_equipo(Equipo(nombre_equipo, id_temporada))
            equipo = temporada.equipos[nombre_equipo]

            equipo.partidos_temporada = max(equipo.partidos_temporada, int(fila.get("partidos_temporada", 0) or 0))
            equipo.descendido = bool(int(fila.get("descendido", 0) or 0)) or equipo.descendido
            equipo.ascendido = bool(int(fila.get("ascendido", 0) or 0)) or equipo.ascendido

            jugador = Jugador(fila, self.trazabilidad)
            equipo.agregar_jugador(jugador)

        return True, ["Liga construida correctamente con {0} temporadas.".format(liga.num_temporadas)], liga

    def resumen_inspeccion(self):
        if not self.filas_normalizadas:
            return "No se ha cargado ningún .xls todavía."

        columnas = sorted(list(self.trazabilidad.keys()))
        vacios = {}
        for col in columnas:
            vacios[col] = 0
        for fila in self.filas_normalizadas:
            for col in columnas:
                valor = fila.get(col, "")
                if valor == "" or valor is None:
                    vacios[col] += 1

        lineas = []
        lineas.append("Archivo inspeccionado: {0}".format(self._ultima_ruta))
        lineas.append("Columnas detectadas (normalizadas -> original):")
        for col in columnas:
            lineas.append("- {0} -> {1}".format(col, self.trazabilidad.get(col, "")))
        lineas.append("Valores vacíos por columna:")
        for col in columnas:
            lineas.append("- {0}: {1}".format(col, vacios[col]))
        return "\n".join(lineas)
