# main.py
# --- Parche para Python 3.11 ---
import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping

from experta import *
from reglas import SistemaEducativo
from hechos import Perfil
from significados import SIGNIFICADOS
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import re
import os
import json
from collections import defaultdict
from datetime import datetime

# ============================================================
#   horarios
# ============================================================
import json

def filtrar_materias_segun_hechos(hechos_finales, path="Horario_PrimerAño.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    materias_filtradas = []

    # -----------------------------------------------
    # Hechos existentes
    # -----------------------------------------------
    busca_virtual = "M" in hechos_finales       # M = virtual
    busca_presencial = "V" in hechos_finales    # V = presencial
    busca_manana = "L" in hechos_finales        # L = mañana
    busca_tarde = "N" in hechos_finales         # N = tarde

    for materia in data["materias"]:
        nombre = materia["nombre"]
        horarios_validos = []

        for h in materia["horarios"]:
            ok = True

            # -----------------------------------------------
            # FILTRO 1 — Modalidad
            # -----------------------------------------------
            if busca_virtual and not h["virtual"]:
                ok = False
            if busca_presencial and h["virtual"]:
                ok = False

            # -----------------------------------------------
            # FILTRO 2 — Horario por turno
            # -----------------------------------------------
            if busca_manana and h["inicio"] >= "12:00":
                ok = False

            if busca_tarde and h["inicio"] < "12:00":
                ok = False

            # Si pasa todos los filtros, lo agregamos
            if ok:
                horarios_validos.append(h)

        # Solo agregar materias que tengan comisiones válidas
        if horarios_validos:
            materias_filtradas.append({
                "materia": nombre,
                "horarios": horarios_validos
            })

    return materias_filtradas


# ============================================================
#   SALUDO
# ============================================================
def obtener_saludo():
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
    print(obtener_saludo())
    print("Soy tu asistente de la Facultad de Ingeniería (UNJu).")
    print("Voy a hacerte unas preguntas rápidas para armar tu perfil y poder darte recomendaciones de estudio que realmente te sirvan. 🤝\n")


def solicitar_nombre_usuario():
    nombre = input("Antes de empezar, ¿cómo te llamas? ").strip()
    return nombre or "Estudiante"


def imprimir_despedida(nombre):
    print("\n¡Gracias por contarme tu situación, {0}!".format(nombre))
    print("Recordá que cada paso que das te acerca a tu objetivo académico. 💪")
    print("Seguí adelante con confianza: ¡tenés todo para lograrlo! 🚀")


# ============================================================
#   MOSTRAR MATERIAS FILTRADAS
# ============================================================
def mostrar_materias_filtradas(materias):
    for m in materias:
        print(f"\nMateria: {m['materia']}")
        for h in m["horarios"]:
            tipo = "Virtual" if h["virtual"] else "Presencial"
            print(f"  - {h['dia']} {h['inicio']}–{h['fin']} ({tipo}, {h['tipo_clase']})")


# ============================================================
#   materias Troncales
# ============================================================




def cargar_materias_troncales(path="materias_troncales.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Agrupa materias destino por materia requisito
    correlativas_dict = defaultdict(list)

    for fila in data["materias_troncales"]:
        materia = fila["nombre"]
        correlativa = fila["correlativa"]
        anio = fila["año"].capitalize()
        cuatri = fila["cuatrimestre"]

        if correlativa.lower() == "no tiene":
            continue

        # Maneja correlativas múltiples "X y Y"
        requisitos = [c.strip() for c in correlativa.split("y")]

        for req in requisitos:
            correlativas_dict[req].append(
                f"{materia} ({anio}, {cuatri} cuatrimestre)"
            )

    # Construyo los mensajes sin repetir correlativas
    mensajes = []
    for req, destinos in correlativas_dict.items():
        destinos_str = ", ".join(destinos)
        mensajes.append(
            f"• Debes haber cursado **{req}** para avanzar a: {destinos_str}."
        )

    return mensajes



# ============================================================
#   DETECTAR ANTECEDENTES DE REGLAS
# ============================================================
def detectar_hechos_antecedentes(path_reglas):
    if not os.path.isfile(path_reglas):
        print(f"⚠️ No encontré {path_reglas}. Usando lista vacía.")
        return set()
    antecedentes = set()
    with open(path_reglas, 'r', encoding='utf-8') as f:
        contenido = f.read()
    for match in re.finditer(r'@Rule\s*\((.*?)\)\s*def', contenido, re.DOTALL):
        dentro = match.group(1)
        for name in re.findall(r'\b([A-Z][A-Za-z0-9_]*)\s*\(', dentro):
            antecedentes.add(name)
    return antecedentes

# ============================================================
#   CALCULAR FINALES
# ============================================================
def calcular_hechos_finales_auto(engine, path_reglas="reglas.py"):
    hechos_inferidos = []
    for fid, hecho in engine.facts.items():
        hechos_inferidos.append(hecho.__class__.__name__)
    hechos_inferidos = list(dict.fromkeys(hechos_inferidos))  

    antecedentes = detectar_hechos_antecedentes(path_reglas)

    return [h for h in hechos_inferidos if h not in antecedentes]

# ============================================================
#   IMPRIMIR SIGNIFICADOS
# ============================================================
def imprimir_significados(engine, path_reglas="reglas.py"):
    resumen = generar_resumen_significados(engine, path_reglas)

    print("\n=== HECHOS INFERIDOS ===")
    for linea in resumen["inferidos"]:
        print(linea)

    print("\n=== HECHOS FINALES ===")
    if resumen["finales"]:
        for linea in resumen["finales"]:
            print(linea)
    else:
        print("(No se detectaron hechos finales.)")

    if resumen["troncales"]:
        print("\n--- MATERIAS TRONCALES ---")
        for ruta in resumen["troncales"]:
            print(ruta)

    if resumen["materias_filtradas"]:
        print("\n--- MATERIAS DISPONIBLES SEGÚN TU PERFIL ---")
        mostrar_materias_filtradas(resumen["materias_filtradas"])

    return resumen["finales_ids"]


def generar_resumen_significados(engine, path_reglas="reglas.py"):
    inferidos = []
    finales = []
    troncales = []
    materias_filtradas = []

    finales_ids = set(calcular_hechos_finales_auto(engine, path_reglas))

    for _, hecho in engine.facts.items():
        nombre = hecho.__class__.__name__
        if nombre in SIGNIFICADOS:
            inferidos.append(f"{nombre}: {SIGNIFICADOS[nombre]}")

        if nombre in SIGNIFICADOS and nombre in finales_ids:
            finales.append(f"{nombre}: {SIGNIFICADOS[nombre]}")

            if nombre == "T":
                troncales = cargar_materias_troncales()

            if nombre in ["L", "N", "M", "V"]:
                hechos_finales = calcular_hechos_finales_auto(engine)
                materias_filtradas = filtrar_materias_segun_hechos(hechos_finales)

    return {
        "inferidos": inferidos,
        "finales": finales,
        "finales_ids": finales_ids,
        "troncales": troncales,
        "materias_filtradas": materias_filtradas,
    }


def generar_recomendaciones_conversacionales(finales, hechos_usuario):
    mensajes = []
    turnos_desc = {
        "AC": "mañana",
        "AD": "tarde",
        "AE": "noche",
    }

    turno_trabajo = next((t for t in turnos_desc if t in hechos_usuario), None)

    if turno_trabajo:
        mensajes.append(
            (
                "Veo que trabajás por la {0}. Aprovechá los huecos libres "
                "para repasar apuntes cortos y, si podés, reserva bloques fijos "
                "los días en que estés más descansado para avanzar con temas clave."
            ).format(turnos_desc[turno_trabajo])
        )
    else:
        mensajes.append(
            "Como hoy tu principal foco es el estudio, organizá una rutina estable "
            "con descansos breves entre materias para sostener el ritmo sin saturarte."
        )

    if "M" in finales or "N" in finales or "L" in finales:
        mensajes.append(
            "Elegí comisiones que se adapten a tu energía: si rendís mejor en la mañana, "
            "apostá por esos horarios; si necesitás flexibilidad, combiná clases virtuales "
            "con materiales asincrónicos para no perder continuidad."
        )

    if "T" in finales:
        mensajes.append(
            "Dale prioridad a las materias troncales. Tenerlas al día te abre la puerta "
            "a cuatrimestres más livianos y a promocionar sin retrasos innecesarios."
        )

    if "BB" in finales or "II" in finales:
        mensajes.append(
            "No descuides el descanso: agendá pausas y espacios recreativos cortos. "
            "Un cuerpo y mente descansados rinden más en parciales y proyectos." 
        )

    if "U" in finales or "FF" in finales:
        mensajes.append(
            "Cuando dispongas de minutos sueltos (viajes, colas, descansos), "
            "repasá tarjetas de memoria o resúmenes breves. Pequeños avances suman a largo plazo."
        )

    if not mensajes:
        mensajes.append(
            "Con la información que compartiste, mantené una planificación semanal con hitos "
            "claros (lecturas, ejercicios, consultas) y revisá tu progreso cada domingo."
        )

    return mensajes


def imprimir_recomendaciones_conversacionales(finales, hechos_usuario):
    print("\n=== RECOMENDACIONES PERSONALIZADAS ===")

    mensajes = generar_recomendaciones_conversacionales(finales, hechos_usuario)

    for mensaje in mensajes:
        print(f"• {mensaje}")


# ============================================================
#   INPUT SI/NO
# ============================================================
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

# ============================================================
#   PREGUNTAS
# ============================================================
PREGUNTAS_PERFILES = {
    "AB": "¿Solo estudias? (si/no): ",
    "AC": "¿Trabajás por la mañana? (si/no): ",
    "AD": "¿Trabajás por la tarde? (si/no): ",
    "AE": "¿Trabajás por la noche? (si/no): ",
    "AF": "¿Vas a cursar solo algunas materias? (si/no): ",
    "AG": "¿Vas a cursar todas las materias? (si/no): ",
    "AH": "¿Estás retomando los estudios después de un tiempo? (si/no): ",
    "AI": "¿Estás estudiando dos carreras a la vez? (si/no): ",
}

# ============================================================
#   MOTOR PRINCIPAL —
# ============================================================
def preparar_engine(respuestas):
    engine = SistemaEducativo()
    engine.reset()

    hechos_usuario = set()

    if respuestas.get("trabaja"):
        turno = respuestas.get("turno_trabajo") or "AC"
        engine.declare(Perfil(**{turno: True}))
        hechos_usuario.add(turno)
    else:
        engine.declare(Perfil(AB=True))
        hechos_usuario.add("AB")

    if respuestas.get("cursa_todas"):
        engine.declare(Perfil(AG=True))
        hechos_usuario.add("AG")
    else:
        engine.declare(Perfil(AF=True))
        hechos_usuario.add("AF")

    if respuestas.get("retoma_estudios"):
        engine.declare(Perfil(AH=True))
        hechos_usuario.add("AH")

    if respuestas.get("doble_carrera"):
        engine.declare(Perfil(AI=True))
        hechos_usuario.add("AI")

    engine.run()
    return engine, hechos_usuario


def ejecutar_inferencia(respuestas):
    engine, hechos_usuario = preparar_engine(respuestas)
    resumen = generar_resumen_significados(engine, "reglas.py")
    recomendaciones = generar_recomendaciones_conversacionales(resumen["finales_ids"], hechos_usuario)

    return resumen, recomendaciones


def run_engine():
    imprimir_info_inicial()
    nombre_usuario = solicitar_nombre_usuario()
    print("Respondé las siguientes preguntas con SI/NO:\n")
    respuestas = {}

    # 1) ¿Trabaja?
    trabaja = preguntar_si_no("¿Trabajás actualmente? (si/no): ")
    if trabaja:
        respuestas["trabaja"] = True
        respuestas["turno_trabajo"] = preguntar_turno_trabajo()
    else:
        respuestas["trabaja"] = False

    # 2) AG siempre; si responde que NO, inferimos automáticamente que cursa algunas (AF)
    respuestas["cursa_todas"] = preguntar_si_no(PREGUNTAS_PERFILES["AG"])

    # 4) AH y AI siempre
    respuestas["retoma_estudios"] = preguntar_si_no(PREGUNTAS_PERFILES["AH"])
    respuestas["doble_carrera"] = preguntar_si_no(PREGUNTAS_PERFILES["AI"])

    # EJECUTAR
    print("\n>>> Ejecutando inferencia...\n")
    engine, hechos_usuario = preparar_engine(respuestas)
    finales = imprimir_significados(engine, "reglas.py")
    imprimir_recomendaciones_conversacionales(finales, hechos_usuario)

    imprimir_despedida(nombre_usuario)


class AsistenteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente Académico UNJu")
        self.root.configure(bg="#0b1724")
        self.root.geometry("1000x720")
        self.root.minsize(920, 680)

        self._crear_estilos()

        self.nombre_var = tk.StringVar()
        self.trabaja_var = tk.StringVar(value="si")
        self.turno_var = tk.StringVar(value="AC")
        self.cursa_todas_var = tk.StringVar(value="si")
        self.retoma_var = tk.StringVar(value="no")
        self.doble_carrera_var = tk.StringVar(value="no")

        self._construir_layout()

    def _crear_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#0b1724")
        style.configure("Card.TFrame", background="#112336", relief="flat")
        style.configure("Title.TLabel", background="#0b1724", foreground="#e2ecf3", font=("Inter", 20, "bold"))
        style.configure("Section.TLabel", background="#112336", foreground="#e2ecf3", font=("Inter", 14, "bold"))
        style.configure("Body.TLabel", background="#112336", foreground="#c8d5e0", font=("Inter", 11))
        style.configure("Form.TLabel", background="#112336", foreground="#c8d5e0", font=("Inter", 11, "bold"))
        style.configure("Accent.TButton", background="#4fd1c5", foreground="#0b1724", font=("Inter", 12, "bold"))
        style.map("Accent.TButton", background=[("active", "#35b8ac")])
        style.configure("Radio.TRadiobutton", background="#112336", foreground="#c8d5e0", font=("Inter", 11))
        style.map("Radio.TRadiobutton", background=[("active", "#112336")])

    def _construir_layout(self):
        hero = ttk.Frame(self.root)
        hero.pack(fill=tk.X, padx=24, pady=(24, 12))

        saludo = obtener_saludo()
        ttk.Label(hero, text=f"{saludo} Soy tu asistente académico.", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            hero,
            text=(
                "Vamos a perfilar tu situación para recomendarte horarios y materias como lo haría "
                "un equipo experto de una gran empresa de software."
            ),
            style="Body.TLabel",
            wraplength=950,
            justify=tk.LEFT,
        ).pack(anchor="w", pady=(6, 0))

        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True, padx=24, pady=12)

        formulario = ttk.Frame(container, style="Card.TFrame")
        formulario.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))

        resultado = ttk.Frame(container, style="Card.TFrame")
        resultado.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12, 0))

        self._construir_formulario(formulario)
        self._construir_resultado(resultado)

    def _construir_formulario(self, parent):
        ttk.Label(parent, text="Tu perfil", style="Section.TLabel").pack(anchor="w", pady=(16, 8), padx=16)

        form = ttk.Frame(parent, style="Card.TFrame")
        form.pack(fill=tk.X, padx=16)

        self._crear_entry(form, "Nombre", self.nombre_var, placeholder="Ej: Ana")
        self._crear_radio(form, "¿Trabajás actualmente?", self.trabaja_var, callback=self._actualizar_turno_estado)

        turno_frame = ttk.Frame(form, style="Card.TFrame")
        ttk.Label(turno_frame, text="Turno laboral", style="Form.TLabel").pack(anchor="w")
        self.turno_combo = ttk.Combobox(
            turno_frame,
            textvariable=self.turno_var,
            state="readonly",
            values=[
                "AC - Mañana",
                "AD - Tarde",
                "AE - Noche",
            ],
            font=("Inter", 11),
        )
        self.turno_combo.pack(fill=tk.X, pady=4)
        self.turno_combo.current(0)
        turno_frame.pack(fill=tk.X, pady=6)

        self._crear_radio(form, "¿Vas a cursar todas las materias?", self.cursa_todas_var)
        self._crear_radio(form, "¿Estás retomando los estudios?", self.retoma_var)
        self._crear_radio(form, "¿Estudiás dos carreras a la vez?", self.doble_carrera_var)

        ttk.Button(
            form,
            text="Generar recomendaciones",
            style="Accent.TButton",
            command=self._procesar_formulario,
        ).pack(fill=tk.X, pady=(12, 16))

        self._actualizar_turno_estado()

    def _construir_resultado(self, parent):
        ttk.Label(parent, text="Diagnóstico y sugerencias", style="Section.TLabel").pack(anchor="w", pady=(16, 8), padx=16)

        self.resultado_text = tk.Text(
            parent,
            bg="#0f1e2f",
            fg="#e2ecf3",
            insertbackground="#e2ecf3",
            font=("Inter", 11),
            relief="flat",
            wrap=tk.WORD,
        )
        self.resultado_text.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
        self.resultado_text.configure(state=tk.DISABLED)

    def _crear_entry(self, parent, texto, var, placeholder=""):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill=tk.X, pady=6)
        ttk.Label(frame, text=texto, style="Form.TLabel").pack(anchor="w")
        entry = ttk.Entry(frame, textvariable=var, font=("Inter", 11))
        entry.insert(0, placeholder)
        entry.pack(fill=tk.X, pady=4)
        return entry

    def _crear_radio(self, parent, texto, var, callback=None):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill=tk.X, pady=6)
        ttk.Label(frame, text=texto, style="Form.TLabel").pack(anchor="w")
        opciones = ttk.Frame(frame, style="Card.TFrame")
        opciones.pack(anchor="w", pady=4)
        for valor, desc in [("si", "Sí"), ("no", "No")]:
            rb = ttk.Radiobutton(
                opciones,
                text=desc,
                value=valor,
                variable=var,
                style="Radio.TRadiobutton",
                command=callback,
            )
            rb.pack(side=tk.LEFT, padx=(0, 12))

    def _actualizar_turno_estado(self):
        if self.trabaja_var.get() == "si":
            self.turno_combo.state(["!disabled", "readonly"])
        else:
            self.turno_combo.state(["disabled"])

    def _procesar_formulario(self):
        nombre = (self.nombre_var.get() or "Estudiante").strip()
        trabaja = self.trabaja_var.get() == "si"
        turno_valor = self.turno_var.get().split(" ")[0]

        respuestas = {
            "trabaja": trabaja,
            "turno_trabajo": turno_valor if trabaja else None,
            "cursa_todas": self.cursa_todas_var.get() == "si",
            "retoma_estudios": self.retoma_var.get() == "si",
            "doble_carrera": self.doble_carrera_var.get() == "si",
        }

        try:
            engine, hechos_usuario = preparar_engine(respuestas)
            resumen = generar_resumen_significados(engine, "reglas.py")
            recomendaciones = generar_recomendaciones_conversacionales(resumen["finales_ids"], hechos_usuario)
            self._mostrar_resultados(nombre, resumen, recomendaciones)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror(
                "Ocurrió un problema",
                "No pudimos generar las recomendaciones en este momento. "
                f"Detalles técnicos: {exc}",
            )

    def _mostrar_resultados(self, nombre, resumen, recomendaciones):
        bloques = [
            f"¡Hola {nombre}! Este es tu diagnóstico personalizado:\n",
            "Perfil detectado:",
        ]

        bloques.extend([f"- {linea}" for linea in resumen["finales"]] or ["- Aún no detectamos un perfil definido."])

        if resumen["troncales"]:
            bloques.append("\nMaterias troncales prioritarias:")
            bloques.extend([f"- {ruta}" for ruta in resumen["troncales"]])

        if resumen["materias_filtradas"]:
            bloques.append("\nComisiones alineadas a tu disponibilidad:")
            for materia in resumen["materias_filtradas"]:
                bloques.append(f"• {materia['materia']}")
                for horario in materia["horarios"]:
                    tipo = "Virtual" if horario["virtual"] else "Presencial"
                    bloques.append(
                        f"   - {horario['dia']} {horario['inicio']}–{horario['fin']} ({tipo}, {horario['tipo_clase']})"
                    )

        bloques.append("\nRecomendaciones estilo experto:")
        bloques.extend([f"- {mensaje}" for mensaje in recomendaciones])

        bloques.append("\n" + "\n".join([
            "Gracias por contarme tu situación. Recordá que cada paso te acerca a tu objetivo académico. 💪",
            "Seguí adelante con confianza: ¡tenés todo para lograrlo! 🚀",
        ]))

        texto_final = "\n".join(bloques)

        self.resultado_text.configure(state=tk.NORMAL)
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert(tk.END, texto_final)
        self.resultado_text.configure(state=tk.DISABLED)


def lanzar_gui():
    root = tk.Tk()
    AsistenteGUI(root)
    root.mainloop()

# ============================================================
#   EJECUTAR
# ============================================================
if __name__ == "__main__":
    try:
        lanzar_gui()
    except tk.TclError:
        print("No se pudo iniciar la interfaz gráfica. Continuando en modo consola...")
        run_engine()


