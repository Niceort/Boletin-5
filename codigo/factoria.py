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
        self.columnas_presentes = set()
        self._ultima_ruta = ""

    def cargar_excel(self, ruta_excel):
        if not os.path.exists(ruta_excel):
            return False, "No existe el archivo: {0}".format(ruta_excel)

        self._ultima_ruta = ruta_excel

        try:
            import xlrd
        except Exception:
            mensaje = "No se encontró la librería 'xlrd'. Instale dependencias con: pip install -r requirements.txt"
            return False, mensaje

        try:
            libro = xlrd.open_workbook(ruta_excel)
        except Exception as error:
            return False, "Error al abrir .xls: {0}".format(error)

        filas_normalizadas = []
        trazabilidad = {}

        for hoja in libro.sheets():
            if hoja.nrows == 0:
                continue

            encabezados = hoja.row_values(0)
            columnas_normalizadas = []

            for cabecera in encabezados:
                nombre_normalizado = self.normalizador.normalizar_nombre_columna(cabecera)
                columnas_normalizadas.append(nombre_normalizado)
                trazabilidad[nombre_normalizado] = str(cabecera)

            for indice_fila in range(1, hoja.nrows):
                valores = hoja.row_values(indice_fila)
                fila_normalizada = {}

                for indice_columna in range(len(columnas_normalizadas)):
                    nombre_columna = columnas_normalizadas[indice_columna]
                    if indice_columna < len(valores):
                        valor_original = valores[indice_columna]
                    else:
                        valor_original = ""
                    fila_normalizada[nombre_columna] = self._normalizar_valor(valor_original)

                # Filtro básico para no construir basura desde el Excel.
                if str(fila_normalizada.get("jugador", "")).strip() == "":
                    continue
                if str(fila_normalizada.get("equipo", "")).strip() == "":
                    continue
                if str(fila_normalizada.get("temporada", "")).strip() == "":
                    continue

                filas_normalizadas.append(fila_normalizada)

        self.trazabilidad = trazabilidad
        self.filas_normalizadas = filas_normalizadas
        self.columnas_presentes = set(trazabilidad.keys())

        mensaje = "Archivo leído correctamente. Filas válidas detectadas: {0}".format(len(filas_normalizadas))
        return True, mensaje

    def _normalizar_valor(self, valor):
        if isinstance(valor, float):
            if int(valor) == valor:
                return int(valor)
            return valor

        if isinstance(valor, str):
            return valor.strip()

        return valor

    def validar_datos(self):
        if len(self.filas_normalizadas) == 0:
            return False, ["No hay filas cargadas para validar."]

        return self.validador.validar(self.filas_normalizadas, self.columnas_presentes)

    def construir_liga(self):
        datos_validos, errores = self.validar_datos()
        if not datos_validos:
            return False, errores, None

        liga = Liga()

        for fila in self.filas_normalizadas:
            identificador_temporada = str(fila.get("temporada", ""))
            nombre_equipo = str(fila.get("equipo", ""))

            if identificador_temporada not in liga.temporadas:
                nueva_temporada = Temporada(identificador_temporada)
                liga.agregar_temporada(nueva_temporada)

            temporada = liga.temporadas[identificador_temporada]

            if nombre_equipo not in temporada.equipos:
                nuevo_equipo = Equipo(nombre_equipo, identificador_temporada)
                temporada.agregar_equipo(nuevo_equipo)

            equipo = temporada.equipos[nombre_equipo]

            partidos_temporada = self._a_entero(fila.get("partidos_temporada", 0))
            if partidos_temporada > equipo.partidos_temporada:
                equipo.partidos_temporada = partidos_temporada

            if bool(self._a_entero(fila.get("descendido", 0))):
                equipo.descendido = True

            if bool(self._a_entero(fila.get("ascendido", 0))):
                equipo.ascendido = True

            jugador = Jugador(fila, self.trazabilidad)
            equipo.agregar_jugador(jugador)

        mensaje = "Liga construida correctamente con {0} temporadas.".format(liga.num_temporadas)
        return True, [mensaje], liga

    def resumen_inspeccion(self):
        if len(self.filas_normalizadas) == 0:
            return "No se ha cargado ningún .xls todavía."

        columnas = sorted(list(self.trazabilidad.keys()))
        vacios_por_columna = {}

        for columna in columnas:
            vacios_por_columna[columna] = 0

        for fila in self.filas_normalizadas:
            for columna in columnas:
                valor = fila.get(columna, "")
                if valor == "" or valor is None:
                    vacios_por_columna[columna] = vacios_por_columna[columna] + 1

        lineas = []
        lineas.append("Archivo inspeccionado: {0}".format(self._ultima_ruta))
        lineas.append("Columnas detectadas (normalizadas -> original):")

        for columna in columnas:
            original = self.trazabilidad.get(columna, "")
            lineas.append("- {0} -> {1}".format(columna, original))

        lineas.append("Valores vacíos por columna:")
        for columna in columnas:
            lineas.append("- {0}: {1}".format(columna, vacios_por_columna[columna]))

        return "\n".join(lineas)

    def _a_entero(self, valor):
        if valor in (None, ""):
            return 0

        try:
            return int(float(valor))
        except Exception:
            return 0
