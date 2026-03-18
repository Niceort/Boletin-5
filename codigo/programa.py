import glob
import os

from factoria import Factoria


class ProgramaPrincipal:
    def __init__(self):
        self.factoria = Factoria()
        self.liga = None

    def _buscar_xls(self):
        base_datos = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        patron = os.path.join(base_datos, "*.xls")
        candidatos = sorted(glob.glob(patron))

        if len(candidatos) == 0:
            return ""

        return candidatos[0]

    def ejecutar(self):
        ruta_excel = self._buscar_xls()
        if ruta_excel == "":
            return False, "No se encontró ningún .xls dentro de data/."

        carga_correcta, mensaje_carga = self.factoria.cargar_excel(ruta_excel)
        if not carga_correcta:
            return False, mensaje_carga

        validacion_correcta, errores = self.factoria.validar_datos()
        if not validacion_correcta:
            texto_error = "Errores de validación:\n- " + "\n- ".join(errores)
            return False, texto_error

        construccion_correcta, mensajes, liga = self.factoria.construir_liga()
        if not construccion_correcta:
            return False, "No se pudo construir la liga."

        self.liga = liga
        salida_ejercicios = self.liga.ejecutar_todos()

        partes = []
        partes.append(mensajes[0])
        partes.append("")
        partes.append(salida_ejercicios)

        return True, "\n".join(partes)


if __name__ == "__main__":
    programa = ProgramaPrincipal()
    estado, salida = programa.ejecutar()
    print(salida)
    raise SystemExit(0 if estado else 1)
