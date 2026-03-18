import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from factoria import Factoria


class InterfazLiga:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Analizador histórico La Liga (.xls)")
        self.raiz.geometry("1350x850")

        self.factoria = Factoria()
        self.liga = None

        self.estado = tk.StringVar(value="Listo.")
        self.ruta_actual = tk.StringVar(value="data/")

        self._crear_layout()

    def _crear_layout(self):
        barra = ttk.Frame(self.raiz)
        barra.pack(side=tk.TOP, fill=tk.X, padx=8, pady=8)

        ttk.Button(barra, text="Cargar .xls", command=self.cargar_xls).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Validar datos", command=self.validar).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Construir liga", command=self.construir).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Ejecutar ejercicio", command=self.ejecutar_uno).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Ejecutar todos", command=self.ejecutar_todos).pack(side=tk.LEFT, padx=4)
        ttk.Label(barra, text="Ejercicio:").pack(side=tk.LEFT, padx=(16, 4))

        valores_combo = []
        for numero in range(1, 34):
            valores_combo.append(str(numero))

        self.combo = ttk.Combobox(barra, values=valores_combo, width=5, state="readonly")
        self.combo.set("1")
        self.combo.pack(side=tk.LEFT)

        ttk.Label(barra, textvariable=self.ruta_actual).pack(side=tk.RIGHT)

        panel = ttk.Frame(self.raiz)
        panel.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(0, weight=19)
        panel.rowconfigure(1, weight=2)

        self.txt_resultados = self._crear_bloque_texto(panel, fila=0, titulo="Resultados")
        self.txt_logs = self._crear_bloque_texto(panel, fila=1, titulo="Logs")

        barra_estado = ttk.Label(self.raiz, textvariable=self.estado, relief=tk.SUNKEN, anchor="w")
        barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

    def _crear_bloque_texto(self, contenedor, fila, titulo):
        frame = ttk.LabelFrame(contenedor, text=titulo)

        if fila == 0:
            padding_vertical = (0, 8)
        else:
            padding_vertical = 0

        frame.grid(row=fila, column=0, sticky="nsew", pady=padding_vertical)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        texto = tk.Text(frame, wrap="none")
        barra_vertical = ttk.Scrollbar(frame, orient="vertical", command=texto.yview)
        barra_horizontal = ttk.Scrollbar(frame, orient="horizontal", command=texto.xview)
        texto.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)

        texto.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        return texto

    def _notificar(self, mensaje, error=False):
        self.estado.set(mensaje)
        self.txt_logs.insert(tk.END, mensaje + "\n")
        self.txt_logs.see(tk.END)

        if error:
            messagebox.showerror("Error", mensaje)
        else:
            messagebox.showinfo("Información", mensaje)

    def cargar_xls(self):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        ruta = filedialog.askopenfilename(initialdir=base, filetypes=[("Excel 97-2003", "*.xls")])

        if ruta == "":
            self._notificar("Carga cancelada por el usuario.")
            return

        correcto, mensaje = self.factoria.cargar_excel(ruta)
        self.ruta_actual.set(ruta)
        self._notificar(mensaje, error=not correcto)

        if correcto:
            resumen = self.factoria.resumen_inspeccion()
            self.txt_logs.insert(tk.END, resumen + "\n")
            self.txt_logs.see(tk.END)

    def validar(self):
        correcto, errores = self.factoria.validar_datos()

        if correcto:
            self._notificar("Validación superada sin errores.")
            return

        mensaje = "Validación fallida. Errores detectados: {0}".format(len(errores))
        self._notificar(mensaje, error=True)

        for error in errores:
            self.txt_logs.insert(tk.END, "- " + error + "\n")

        self.txt_logs.see(tk.END)

    def construir(self):
        correcto, mensajes, liga = self.factoria.construir_liga()

        if correcto:
            self.liga = liga
            self._notificar(mensajes[0])
            return

        self._notificar("No se puede construir la liga. Revise validaciones.", error=True)
        for mensaje in mensajes:
            self.txt_logs.insert(tk.END, "- " + mensaje + "\n")
        self.txt_logs.see(tk.END)

    def ejecutar_uno(self):
        if self.liga is None:
            self._notificar("Debe construir la liga antes de ejecutar ejercicios.", error=True)
            return

        numero = int(self.combo.get())
        resultado = self.liga.ejecutar_ejercicio(numero)

        bloque = []
        bloque.append("Ejercicio {0}".format(numero))
        bloque.append(resultado)
        bloque.append("")

        self.txt_resultados.insert(tk.END, "\n".join(bloque) + "\n")
        self.txt_resultados.see(tk.END)
        self._notificar("Ejercicio {0} ejecutado correctamente.".format(numero))

    def ejecutar_todos(self):
        if self.liga is None:
            self._notificar("Debe construir la liga antes de ejecutar ejercicios.", error=True)
            return

        resultado = self.liga.ejecutar_todos()
        self.txt_resultados.delete("1.0", tk.END)
        self.txt_resultados.insert(tk.END, resultado)
        self.txt_resultados.see(tk.END)
        self._notificar("Ejecución completa finalizada.")
