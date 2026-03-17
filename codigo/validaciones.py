import re


class ValidadorDatos:
    def __init__(self):
        self.errores = []

    def _agregar_error(self, mensaje):
        self.errores.append(mensaje)

    def validar(self, filas):
        self.errores = []
        partidos_temporada = {}
        for indice, fila in enumerate(filas):
            etiqueta = "Fila {0}".format(indice + 1)
            temporada = str(fila.get("temporada", ""))
            if not self._temporada_valida(temporada):
                self._agregar_error("{0}: temporada inválida '{1}'".format(etiqueta, temporada))
            self._validar_positivos(fila, etiqueta)
            self._validar_relaciones_jugador(fila, etiqueta)

            if temporada not in partidos_temporada:
                partidos_temporada[temporada] = 0
            partidos_fila = int(fila.get("partidos_temporada", 0) or 0)
            if partidos_fila > partidos_temporada[temporada]:
                partidos_temporada[temporada] = partidos_fila

        for indice, fila in enumerate(filas):
            temporada = str(fila.get("temporada", ""))
            pj = int(fila.get("partidos_jugados", 0) or 0)
            max_temp = partidos_temporada.get(temporada, 0)
            if max_temp > 0 and pj > max_temp:
                self._agregar_error("Fila {0}: partidos_jugados ({1}) > partidos_temporada ({2})".format(indice + 1, pj, max_temp))

        return len(self.errores) == 0, self.errores

    def _temporada_valida(self, temporada):
        patron = re.compile(r"^(\d{4})-(\d{2})$")
        encontrado = patron.match(temporada)
        if not encontrado:
            return False
        anio = int(encontrado.group(1))
        fin = int(encontrado.group(2))
        esperado = (anio + 1) % 100
        return fin == esperado

    def _validar_positivos(self, fila, etiqueta):
        numericas = [
            "partidos_jugados", "partidos_titular", "partidos_suplente", "partidos_completos",
            "minutos", "goles", "amarillas", "rojas", "cambios", "partidos_temporada"
        ]
        for campo in numericas:
            valor = fila.get(campo, 0)
            try:
                numero = float(valor)
            except Exception:
                self._agregar_error("{0}: {1} no numérico ('{2}')".format(etiqueta, campo, valor))
                continue
            if numero < 0:
                self._agregar_error("{0}: {1} negativo ({2})".format(etiqueta, campo, valor))

    def _validar_relaciones_jugador(self, fila, etiqueta):
        pj = int(fila.get("partidos_jugados", 0) or 0)
        pt = int(fila.get("partidos_titular", 0) or 0)
        ps = int(fila.get("partidos_suplente", 0) or 0)
        pc = int(fila.get("partidos_completos", 0) or 0)
        minutos = int(fila.get("minutos", 0) or 0)

        if pc > pt:
            self._agregar_error("{0}: partidos_completos ({1}) > partidos_titular ({2})".format(etiqueta, pc, pt))
        if pj != pt + ps:
            self._agregar_error("{0}: partidos_jugados ({1}) != titular+suplente ({2}+{3})".format(etiqueta, pj, pt, ps))
        if minutos > pj * 90:
            self._agregar_error("{0}: minutos ({1}) > partidos_jugados*90 ({2})".format(etiqueta, minutos, pj * 90))
