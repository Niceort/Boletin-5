import glob
import os

from factoria import Factoria
from utilidades import GestorBenchmark


class ProgramaPrincipal:
    def __init__(self):
        self.factoria = Factoria()
        self.benchmark = GestorBenchmark()
        self.liga = None

    def _buscar_xls(self):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        candidatos = sorted(glob.glob(os.path.join(base, "*.xls")))
        if not candidatos:
            return ""
        return candidatos[0]

    def ejecutar(self):
        ruta = self._buscar_xls()
        if not ruta:
            return False, "No se encontró ningún .xls dentro de data/."

        ok, msg = self.factoria.cargar_excel(ruta)
        if not ok:
            return False, msg

        ok, errores = self.factoria.validar_datos()
        if not ok:
            return False, "Errores de validación:\n- " + "\n- ".join(errores)

        ok, mensajes, liga = self.factoria.construir_liga()
        if not ok:
            return False, "No se pudo construir la liga."

        self.liga = liga
        salida = liga.ejecutar_todos()
        difs = self.benchmark.comparar(salida)
        texto = [mensajes[0], "", salida, "", "Comparación benchmark:"]
        if difs:
            texto.append("Diferencias detectadas: {0}".format(len(difs)))
            texto.extend(difs[:50])
        else:
            texto.append("Sin diferencias.")
        return True, "\n".join(texto)


if __name__ == "__main__":
    programa = ProgramaPrincipal()
    estado, salida = programa.ejecutar()
    print(salida)
    raise SystemExit(0 if estado else 1)
