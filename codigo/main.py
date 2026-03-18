import os
import tkinter as tk

from interfaz import InterfazLiga


# Punto de entrada sencillo para arrancar la interfaz.
def main():
    raiz = tk.Tk()
    aplicacion = InterfazLiga(raiz)

    # Dejamos un mensaje útil nada más abrir la app.
    ruta_datos = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    if os.path.isdir(ruta_datos):
        aplicacion.estado.set("Aplicación iniciada. Cargue un archivo .xls desde data/.")
    else:
        aplicacion.estado.set("Aplicación iniciada. La carpeta data/ no está disponible.")

    raiz.mainloop()


if __name__ == "__main__":
    main()
