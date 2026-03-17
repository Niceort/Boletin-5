import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from factoria import Factoria
from utilidades import GestorBenchmark, arbol_proyecto


class InterfazLiga:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Analizador histórico La Liga (.xls)")
        self.raiz.geometry("1350x850")

        self.factoria = Factoria()
        self.benchmark = GestorBenchmark()
        self.liga = None

        self.estado = tk.StringVar(value="Listo.")
        self.ruta_actual = tk.StringVar(value="data/")

        self._crear_layout()
        self._cargar_codigo_fuente()

    def _crear_layout(self):
        barra = ttk.Frame(self.raiz)
        barra.pack(side=tk.TOP, fill=tk.X, padx=8, pady=8)

        ttk.Button(barra, text="Cargar .xls", command=self.cargar_xls).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Validar datos", command=self.validar).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Construir liga", command=self.construir).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Ejecutar ejercicio", command=self.ejecutar_uno).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Ejecutar todos", command=self.ejecutar_todos).pack(side=tk.LEFT, padx=4)
        ttk.Label(barra, text="Ejercicio:").pack(side=tk.LEFT, padx=(16, 4))

        self.combo = ttk.Combobox(barra, values=[str(i) for i in range(1, 34)], width=5, state="readonly")
        self.combo.set("1")
        self.combo.pack(side=tk.LEFT)

        ttk.Label(barra, textvariable=self.ruta_actual).pack(side=tk.RIGHT)

        notebook = ttk.Notebook(self.raiz)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.txt_resultados = self._crear_pestana_texto(notebook, "Resultados")
        self.txt_logs = self._crear_pestana_texto(notebook, "Validación y logs")
        self.txt_benchmark = self._crear_pestana_texto(notebook, "Benchmark esperado")
        self.txt_comparacion = self._crear_pestana_texto(notebook, "Comparación")
        self.txt_codigo = self._crear_pestana_texto(notebook, "Visor de código")
        self.txt_estructura = self._crear_pestana_texto(notebook, "Estructura proyecto")

        self.txt_benchmark.insert(tk.END, self.benchmark.obtener_texto_esperado())
        self.txt_estructura.insert(tk.END, arbol_proyecto(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))))

        estado_bar = ttk.Label(self.raiz, textvariable=self.estado, relief=tk.SUNKEN, anchor="w")
        estado_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _crear_pestana_texto(self, notebook, titulo):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=titulo)

        texto = tk.Text(frame, wrap="none")
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=texto.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=texto.xview)
        texto.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        texto.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
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
        if not ruta:
            self._notificar("Carga cancelada por el usuario.")
            return
        ok, mensaje = self.factoria.cargar_excel(ruta)
        self.ruta_actual.set(ruta)
        self._notificar(mensaje, error=not ok)
        if ok:
            self.txt_logs.insert(tk.END, self.factoria.resumen_inspeccion() + "\n")

    def validar(self):
        ok, errores = self.factoria.validar_datos()
        if ok:
            self._notificar("Validación superada sin errores.")
        else:
            mensaje = "Validación fallida. Errores detectados: {0}".format(len(errores))
            self._notificar(mensaje, error=True)
            for err in errores:
                self.txt_logs.insert(tk.END, "- " + err + "\n")

    def construir(self):
        ok, mensajes, liga = self.factoria.construir_liga()
        if ok:
            self.liga = liga
            self._notificar(mensajes[0])
        else:
            self._notificar("No se puede construir la liga. Revise validaciones.", error=True)
            for msg in mensajes:
                self.txt_logs.insert(tk.END, "- " + msg + "\n")

    def ejecutar_uno(self):
        if self.liga is None:
            self._notificar("Debe construir la liga antes de ejecutar ejercicios.", error=True)
            return
        numero = int(self.combo.get())
        resultado = self.liga.ejecutar_ejercicio(numero)
        bloque = "Ejercicio {0}\n{1}\n\n".format(numero, resultado)
        self.txt_resultados.insert(tk.END, bloque)
        self.txt_resultados.see(tk.END)
        self._notificar("Ejercicio {0} ejecutado correctamente.".format(numero))

    def ejecutar_todos(self):
        if self.liga is None:
            self._notificar("Debe construir la liga antes de ejecutar ejercicios.", error=True)
            return
        resultado = self.liga.ejecutar_todos()
        self.txt_resultados.delete("1.0", tk.END)
        self.txt_resultados.insert(tk.END, resultado)
        diferencias = self.benchmark.comparar(resultado)
        self.txt_comparacion.delete("1.0", tk.END)
        if diferencias:
            self.txt_comparacion.insert(tk.END, "DIFERENCIAS DETECTADAS\n")
            for item in diferencias:
                self.txt_comparacion.insert(tk.END, "- {0}\n".format(item))
            self._notificar("Ejecución completa con diferencias respecto al benchmark.", error=True)
        else:
            self.txt_comparacion.insert(tk.END, "Salida idéntica al benchmark esperado.")
            self._notificar("Ejecución completa y benchmark coincidente.")

    def _cargar_codigo_fuente(self):
        raiz = os.path.abspath(os.path.dirname(__file__))
        archivos = []
        for nombre in sorted(os.listdir(raiz)):
            if nombre.endswith(".py"):
                archivos.append(os.path.join(raiz, nombre))
        contenido = []
        for ruta in archivos:
            contenido.append("===== {0} =====".format(ruta))
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido.append(f.read())
            except Exception as ex:
                contenido.append("Error al leer archivo: {0}".format(ex))
            contenido.append("")
        self.txt_codigo.insert(tk.END, "\n".join(contenido))
