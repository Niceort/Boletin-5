import os
import tkinter as tk

from interfaz import InterfazLiga


def main():
    raiz = tk.Tk()
    app = InterfazLiga(raiz)

    ruta_default = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    if os.path.isdir(ruta_default):
        app.estado.set("Aplicación iniciada. Cargue un archivo .xls desde data/.")

    raiz.mainloop()


if __name__ == "__main__":
    main()
