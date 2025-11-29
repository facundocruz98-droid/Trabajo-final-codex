# ui.py
"""Funciones de interacción por consola y una interfaz gráfica moderna con Tkinter."""

import io
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText


def obtener_saludo():
    """Devuelve un saludo dinámico según la hora actual."""
    h = datetime.now().hour
    if 6 <= h < 12:
        return "¡Buen día! ☀️"
    elif 12 <= h < 18:
        return "¡Buenas tardes! 🌤️"
    elif 18 <= h < 24:
        return "¡Buenas noches! 🌙"
    else:
        return "Wow, estás conectado a la madrugada 😴 — ¡sos un/a crack!"


def imprimir_info_inicial():
    """Muestra el saludo y el mensaje de presentación en consola."""
    print(obtener_saludo())
    print("Soy tu asistente de la Facultad de Ingeniería (UNJu).")
    print(
        "Voy a hacerte unas preguntas rápidas para armar tu perfil y poder darte recomendaciones de estudio que realmente te sirvan. 🤝\n"
    )


def solicitar_nombre_usuario():
    nombre = input("Antes de empezar, ¿cómo te llamas? ").strip()
    return nombre or "Estudiante"


def imprimir_despedida(nombre):
    print("\n¡Gracias por contarme tu situación, {0}!".format(nombre))
    print("Recordá que cada paso que das te acerca a tu objetivo académico. 💪")
    print("Seguí adelante con confianza: ¡tenés todo para lograrlo! 🚀")


# Entrada segura y preguntas (para la modalidad consola)
def _leer_entrada_segura(texto, default=""):
    try:
        return input(texto)
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada interrumpida. Usaré respuesta por defecto.")
        return default


def preguntar_si_no(texto):
    while True:
        r = _leer_entrada_segura(texto, default="no").strip().lower()
        if r in ["si", "sí", "s"]:
            return True
        if r in ["no", "n"]:
            return False
        print("⚠️ Responde solo 'si' o 'no'.")


def preguntar_turno_trabajo():
    opciones = {
        "1": ("AC", "mañana"),
        "2": ("AD", "tarde"),
        "3": ("AE", "noche"),
    }
    prompt = (
        "¿En qué turno trabajás? \n"
        "  [1] Mañana\n"
        "  [2] Tarde\n"
        "  [3] Noche\n"
        "Seleccioná una opción (1/2/3): "
    )
    while True:
        eleccion = _leer_entrada_segura(prompt).strip()
        if eleccion in opciones:
            return opciones[eleccion][0]
        print("⚠️ Debes elegir 1, 2 o 3 para continuar.")


def ejecutar_sistema_desde_ui(nombre, trabaja, cursa_todo, retoma, dos_carreras, turno_trabajo=None):
    """
    Ejecuta el sistema experto con datos provistos por la interfaz gráfica y
    devuelve el resultado completo en un solo string (igual a lo que se vería
    en consola), incluyendo:

    - saludo y mensaje inicial
    - resumen completo (hechos inferidos/finales)
    - recomendaciones
    - materias troncales y disponibles
    - explicación del razonamiento
    - mensaje final motivador personalizado
    """

    # Importaciones locales para evitar errores en entornos donde no estén
    # instaladas las dependencias hasta el momento en que realmente se necesitan.
    from engine_utils import imprimir_trazabilidad, preparar_engine
    from hechos import Perfil
    from reglas import SistemaEducativo
    from resumen import imprimir_todo_unificado

    nombre_usuario = (nombre or "").strip() or "Estudiante"

    buffer = io.StringIO()
    sys_stdout_original = sys.stdout
    sys.stdout = buffer
    try:
        imprimir_info_inicial()

        respuestas = {
            "trabaja": bool(trabaja),
            "cursa_todas": bool(cursa_todo),
            "retoma_estudios": bool(retoma),
            "doble_carrera": bool(dos_carreras),
            "turno_trabajo": turno_trabajo,
        }

        print("\n>>> Ejecutando inferencia...\n")
        engine, hechos_usuario = preparar_engine(respuestas, SistemaEducativo, Perfil)

        imprimir_todo_unificado(engine, hechos_usuario, "reglas.py")
        imprimir_trazabilidad()
        imprimir_despedida(nombre_usuario)
    finally:
        sys.stdout = sys_stdout_original

    return buffer.getvalue()


# === Sección gráfica (Tkinter) ===
def _configurar_estilos(style):
    """Configura un tema oscuro y moderno para los widgets ttk."""

    style.theme_use("clam")

    colores = {
        "fondo": "#0f172a",
        "panel": "#111827",
        "texto": "#e5e7eb",
        "primario": "#3b82f6",
        "primario_hover": "#60a5fa",
    }

    style.configure("TFrame", background=colores["fondo"])
    style.configure("Dark.TLabelframe", background=colores["panel"], foreground=colores["texto"], padding=10)
    style.configure("Dark.TLabelframe.Label", background=colores["panel"], foreground=colores["texto"], font=("Segoe UI", 11, "bold"))
    style.configure("TLabel", background=colores["panel"], foreground=colores["texto"], font=("Segoe UI", 10))
    style.configure("Header.TLabel", background=colores["fondo"], foreground=colores["texto"], font=("Segoe UI", 20, "bold"))
    style.configure("Subheader.TLabel", background=colores["fondo"], foreground=colores["texto"], font=("Segoe UI", 12))
    style.configure("TButton", background=colores["primario"], foreground="white", font=("Segoe UI", 10, "bold"), padding=10, borderwidth=0)
    style.map(
        "TButton",
        background=[("active", colores["primario_hover"])],
        foreground=[("active", "white")],
    )

    return colores


def crear_y_ejecutar_ui():
    """Arma la interfaz gráfica completa y conecta los datos del usuario con el motor de inferencia."""

    try:
        root = tk.Tk()
    except tk.TclError as exc:  # noqa: PERF203
        # Mensaje claro cuando no hay entorno gráfico disponible (por ejemplo, ejecución remota sin $DISPLAY).
        print(
            "No se pudo iniciar la interfaz gráfica. Verifica que tu sistema tenga un entorno gráfico disponible",
            "(DISPLAY configurado) e intenta nuevamente.\nDetalle:",
            exc,
        )
        return
    root.title("Asistente de Recomendaciones – Ingeniería UNJu")
    root.geometry("1000x700")

    style = ttk.Style(root)
    colores = _configurar_estilos(style)

    root.configure(bg=colores["fondo"])

    # Zona superior: saludo y presentación
    frame_top = ttk.Frame(root)
    frame_top.pack(fill="x", padx=15, pady=15)

    lbl_saludo = ttk.Label(frame_top, text=obtener_saludo(), style="Header.TLabel")
    lbl_saludo.pack(anchor="w")

    lbl_presentacion = ttk.Label(
        frame_top,
        text=(
            "Soy tu asistente de la Facultad de Ingeniería (UNJu).\n"
            "Voy a hacerte unas preguntas rápidas para armar tu perfil y poder darte recomendaciones de estudio que realmente te sirvan. 🤝"
        ),
        style="Subheader.TLabel",
        justify="left",
    )
    lbl_presentacion.pack(anchor="w", pady=(5, 0))

    # Zona inferior dividida en dos columnas
    frame_bottom = ttk.Frame(root)
    frame_bottom.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    frame_bottom.columnconfigure(0, weight=1)
    frame_bottom.columnconfigure(1, weight=2)

    # Panel izquierdo: entrada de datos
    panel_izq = ttk.Labelframe(frame_bottom, text="Datos del estudiante", style="Dark.TLabelframe")
    panel_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
    panel_izq.columnconfigure(0, weight=1)

    ttk.Label(panel_izq, text="Nombre", style="TLabel").grid(row=0, column=0, sticky="w", pady=(0, 5))
    entry_nombre = ttk.Entry(panel_izq, font=("Segoe UI", 10))
    entry_nombre.grid(row=1, column=0, sticky="ew", pady=(0, 10))

    def _crear_grupo_si_no(parent, texto, row):
        ttk.Label(parent, text=texto, style="TLabel").grid(row=row, column=0, sticky="w", pady=(0, 5))
        var = tk.StringVar(value="no")
        frame = ttk.Frame(parent, style="TFrame")
        frame.grid(row=row + 1, column=0, sticky="w", pady=(0, 10))
        ttk.Radiobutton(frame, text="Sí", value="si", variable=var).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(frame, text="No", value="no", variable=var).pack(side="left")
        return var

    var_trabaja = _crear_grupo_si_no(panel_izq, "¿Trabajás actualmente?", 2)
    ttk.Label(panel_izq, text="¿En qué turno trabajás?", style="TLabel").grid(row=4, column=0, sticky="w", pady=(0, 5))

    frame_turno = ttk.Frame(panel_izq, style="TFrame")
    frame_turno.grid(row=5, column=0, sticky="ew", pady=(0, 10))
    var_turno = tk.StringVar(value="AC")
    opciones_turno = {
        "AC": "Mañana",
        "AD": "Tarde",
        "AE": "Noche",
    }
    combo_turno = ttk.Combobox(
        frame_turno,
        textvariable=var_turno,
        state="readonly",
        values=[f"{codigo} - {texto}" for codigo, texto in opciones_turno.items()],
    )
    combo_turno.current(0)
    combo_turno.pack(fill="x")

    def _actualizar_estado_turno(*_args):
        habilitar = var_trabaja.get() == "si"
        combo_turno.state(["!disabled"] if habilitar else ["disabled"])

    var_trabaja.trace_add("write", _actualizar_estado_turno)
    _actualizar_estado_turno()

    var_cursa = _crear_grupo_si_no(panel_izq, "¿Vas a cursar todas las materias?", 6)
    var_retoma = _crear_grupo_si_no(panel_izq, "¿Estás retomando los estudios después de un tiempo?", 8)
    var_dos_carreras = _crear_grupo_si_no(panel_izq, "¿Estás estudiando dos carreras a la vez?", 10)

    # Panel derecho: resultados
    panel_der = ttk.Labelframe(frame_bottom, text="Resumen y Recomendaciones", style="Dark.TLabelframe")
    panel_der.grid(row=0, column=1, sticky="nsew", pady=5)
    panel_der.columnconfigure(0, weight=1)
    panel_der.rowconfigure(0, weight=1)

    texto_resultado = ScrolledText(
        panel_der,
        font=("Consolas", 10),
        background=colores["panel"],
        foreground=colores["texto"],
        insertbackground=colores["texto"],
        wrap="word",
    )
    texto_resultado.grid(row=0, column=0, sticky="nsew")

    def _mostrar_resultado():
        """Conecta las respuestas del usuario con el motor de inferencia y refresca el panel de texto."""

        nombre = entry_nombre.get().strip()
        trabaja = var_trabaja.get() == "si"
        cursa_todo = var_cursa.get() == "si"
        retoma = var_retoma.get() == "si"
        dos_carreras = var_dos_carreras.get() == "si"
        turno_trabajo = None
        if trabaja:
            seleccion = var_turno.get()
            turno_trabajo = seleccion.split(" - ", 1)[0] if " - " in seleccion else seleccion or None

        try:
            texto = ejecutar_sistema_desde_ui(
                nombre,
                trabaja,
                cursa_todo,
                retoma,
                dos_carreras,
                turno_trabajo=turno_trabajo,
            )
        except Exception as exc:  # noqa: BLE001
            # Muestra un mensaje claro si falta alguna dependencia o falla el motor.
            messagebox.showerror(
                "Error al ejecutar",
                "No se pudo generar el resumen. Verifica que las dependencias estén instaladas (por ejemplo, 'experta').\n\n"
                f"Detalle: {exc}",
            )
            return

        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, texto)

    btn_generar = ttk.Button(panel_izq, text="Generar recomendaciones", command=_mostrar_resultado)
    btn_generar.grid(row=12, column=0, sticky="ew", pady=(10, 0))

    root.mainloop()


if __name__ == "__main__":
    crear_y_ejecutar_ui()
