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
    print("\n=== HECHOS INFERIDOS ===")
    for fid, hecho in engine.facts.items():
        nombre = hecho.__class__.__name__
        if nombre in SIGNIFICADOS:
            print(f"{nombre}: {SIGNIFICADOS[nombre]}")

    finales = set(calcular_hechos_finales_auto(engine, path_reglas))

    print("\n=== HECHOS FINALES ===")
    any_final = False
    for fid, hecho in engine.facts.items():
        nombre = hecho.__class__.__name__
        if nombre in SIGNIFICADOS and nombre in finales:
            print(f"{nombre}: {SIGNIFICADOS[nombre]}")
            any_final = True
            # 🔥 SI EL HECHO FINAL ES "TRONCALES", MOSTRAR MATERIAS TRONCALES
            if nombre == "T":
                print("\n--- MATERIAS TRONCALES ---")
                rutas = cargar_materias_troncales()
                for r in rutas:
                 print(r)
            # 🔥 FILTRAR MATERIAS SEGÚN HORARIOS (L, N, M, V)
            if nombre in ["L", "N", "M", "V"]:
                hechos_finales = calcular_hechos_finales_auto(engine)
                materias_filtradas = filtrar_materias_segun_hechos(hechos_finales)

                if materias_filtradas:
                    print("\n--- MATERIAS DISPONIBLES SEGÚN TU PERFIL ---")
                    mostrar_materias_filtradas(materias_filtradas)

    if not any_final:
        print("(No se detectaron hechos finales.)")


# ============================================================
#   INPUT SI/NO
# ============================================================
def preguntar_si_no(texto):
    while True:
        r = input(texto).strip().lower()
        if r in ["si", "sí", "s"]:
            return True
        if r in ["no", "n"]:
            return False
        print("⚠️ Responde solo 'si' o 'no'.")

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
def run_engine():
    engine = SistemaEducativo()
    engine.reset()

    print(obtener_saludo())
    print("Respondé las siguientes preguntas con SI/NO:\n")

    hechos_usuario = set()

    # 1) AB
    if preguntar_si_no(PREGUNTAS_PERFILES["AB"]):
        engine.declare(Perfil(AB=True))
        hechos_usuario.add("AB")
        trabaja = False
    else:
        trabaja = None

    # 2) si NO AB → preguntar si trabaja
    if "AB" not in hechos_usuario:
        if preguntar_si_no("¿Trabajás? (si/no): "):
            trabaja = True
        else:
            trabaja = False

    # 3) Si trabaja → AC AD AE
    if trabaja:
        if preguntar_si_no(PREGUNTAS_PERFILES["AC"]):
            engine.declare(Perfil(AC=True))
            hechos_usuario.add("AC")
        if preguntar_si_no(PREGUNTAS_PERFILES["AD"]):
            engine.declare(Perfil(AD=True))
            hechos_usuario.add("AD")
        if preguntar_si_no(PREGUNTAS_PERFILES["AE"]):
            engine.declare(Perfil(AE=True))
            hechos_usuario.add("AE")

    # 4) AG siempre
    if preguntar_si_no(PREGUNTAS_PERFILES["AG"]):
        engine.declare(Perfil(AG=True))
        hechos_usuario.add("AG")
        cursa_todas = True
    else:
        cursa_todas = False

    # 5) AF solo si NO cursa todas
    if not cursa_todas:
        if preguntar_si_no(PREGUNTAS_PERFILES["AF"]):
            engine.declare(Perfil(AF=True))
            hechos_usuario.add("AF")

    # 6) AH y AI siempre
    if preguntar_si_no(PREGUNTAS_PERFILES["AH"]):
        engine.declare(Perfil(AH=True))
        hechos_usuario.add("AH")

    if preguntar_si_no(PREGUNTAS_PERFILES["AI"]):
        engine.declare(Perfil(AI=True))
        hechos_usuario.add("AI")

    # EJECUTAR
    print("\n>>> Ejecutando inferencia...\n")
    engine.run()
    imprimir_significados(engine, "reglas.py")
    hechos_finales = engine.facts
    hechos = [f for f in hechos_finales.values() if isinstance(f, str)]

# ============================================================
#   EJECUTAR
# ============================================================
if __name__ == "__main__":
    run_engine()


