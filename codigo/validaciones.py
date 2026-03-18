import re


class ValidadorDatos:
    def __init__(self):
        self.errores = []
        self.columnas_presentes = set()

    def _agregar_error(self, mensaje):
        self.errores.append(mensaje)

    def validar(self, filas, columnas_presentes=None):
        self.errores = []
        if columnas_presentes is None:
            self.columnas_presentes = set()
        else:
            self.columnas_presentes = set(columnas_presentes)

        partidos_maximos_por_temporada = {}

        for indice, fila in enumerate(filas):
            etiqueta = "Fila {0}".format(indice + 1)
            temporada = str(fila.get("temporada", ""))

            if not self._temporada_valida(temporada):
                self._agregar_error("{0}: temporada inválida '{1}'".format(etiqueta, temporada))

            self._validar_positivos(fila, etiqueta)
            self._validar_relaciones_jugador(fila, etiqueta)

            if temporada not in partidos_maximos_por_temporada:
                partidos_maximos_por_temporada[temporada] = 0

            if self._tiene_columna("partidos_temporada"):
                partidos_fila = self._a_entero(fila.get("partidos_temporada", 0))
            else:
                partidos_fila = self._a_entero(fila.get("partidos_jugados", 0))

            if partidos_fila > partidos_maximos_por_temporada[temporada]:
                partidos_maximos_por_temporada[temporada] = partidos_fila

        for indice, fila in enumerate(filas):
            temporada = str(fila.get("temporada", ""))
            partidos_jugados = self._a_entero(fila.get("partidos_jugados", 0))
            partidos_maximos = partidos_maximos_por_temporada.get(temporada, 0)

            if self._tiene_columna("partidos_jugados") and partidos_maximos > 0:
                if partidos_jugados > partidos_maximos:
                    mensaje = "Fila {0}: partidos_jugados ({1}) > partidos_temporada ({2})"
                    self._agregar_error(mensaje.format(indice + 1, partidos_jugados, partidos_maximos))

        return len(self.errores) == 0, self.errores

    def _temporada_valida(self, temporada):
        patron = re.compile(r"^(\d{4})-(\d{2})$")
        resultado = patron.match(temporada)
        if resultado is None:
            return False

        anio_inicio = int(resultado.group(1))
        anio_fin = int(resultado.group(2))
        esperado = (anio_inicio + 1) % 100
        return anio_fin == esperado

    def _validar_positivos(self, fila, etiqueta):
        campos_numericos = [
            "partidos_jugados",
            "partidos_titular",
            "partidos_suplente",
            "partidos_completos",
            "minutos",
            "goles",
            "amarillas",
            "rojas",
            "cambios",
            "partidos_temporada",
        ]

        for campo in campos_numericos:
            if not self._tiene_columna(campo):
                continue

            valor = fila.get(campo, 0)
            if valor in (None, ""):
                numero = 0
            else:
                try:
                    numero = float(valor)
                except Exception:
                    self._agregar_error("{0}: {1} no numérico ('{2}')".format(etiqueta, campo, valor))
                    continue

            if numero < 0:
                self._agregar_error("{0}: {1} negativo ({2})".format(etiqueta, campo, valor))

    def _validar_relaciones_jugador(self, fila, etiqueta):
        partidos_jugados = self._a_entero(fila.get("partidos_jugados", 0))
        partidos_titular = self._a_entero(fila.get("partidos_titular", 0))
        partidos_suplente = self._a_entero(fila.get("partidos_suplente", 0))
        partidos_completos = self._a_entero(fila.get("partidos_completos", 0))
        minutos = self._a_entero(fila.get("minutos", 0))

        if self._tiene_columna("partidos_completos") and self._tiene_columna("partidos_titular"):
            if partidos_completos > partidos_titular:
                mensaje = "{0}: partidos_completos ({1}) > partidos_titular ({2})"
                self._agregar_error(mensaje.format(etiqueta, partidos_completos, partidos_titular))

        tiene_titular = "partidos_titular" in fila
        tiene_suplente = "partidos_suplente" in fila
        if self._tiene_columna("partidos_jugados") and tiene_titular and tiene_suplente:
            if partidos_jugados < partidos_titular + partidos_suplente:
                mensaje = "{0}: partidos_jugados ({1}) < titular+suplente ({2}+{3})"
                self._agregar_error(mensaje.format(etiqueta, partidos_jugados, partidos_titular, partidos_suplente))

        # Esta parte es importante: evitamos falsos positivos absurdos del dataset.
        if self._tiene_columna("partidos_jugados") and self._tiene_columna("minutos"):
            if partidos_jugados == 0 and minutos > 0:
                self._agregar_error("{0}: minutos ({1}) > 0 con partidos_jugados=0".format(etiqueta, minutos))
            elif partidos_jugados > 0 and minutos > partidos_jugados * 120:
                limite = partidos_jugados * 120
                self._agregar_error("{0}: minutos ({1}) > partidos_jugados*120 ({2})".format(etiqueta, minutos, limite))

    def _a_entero(self, valor):
        if valor in (None, ""):
            return 0

        try:
            return int(float(valor))
        except Exception:
            return 0

    def _tiene_columna(self, nombre):
        if len(self.columnas_presentes) == 0:
            return True
        return nombre in self.columnas_presentes
