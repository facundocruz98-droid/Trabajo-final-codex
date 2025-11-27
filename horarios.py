# horarios.py
import json

def filtrar_materias_segun_hechos(hechos_finales, path="Horario_PrimerAño.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    materias_filtradas = []

    busca_todo = "E" in hechos_finales
    busca_virtual = "M" in hechos_finales
    busca_presencial = "V" in hechos_finales
    busca_manana = "L" in hechos_finales
    busca_tarde = "N" in hechos_finales

    for materia in data["materias"]:
        nombre = materia["nombre"]
        horarios_validos = []

        for h in materia["horarios"]:
            ok = True

            # --- SI E está presente, no filtrar por modalidad ---
            if not busca_todo:
                if busca_virtual and not h["virtual"]:
                    ok = False
                if busca_presencial and h["virtual"]:
                    ok = False

            # --- Filtrado de horarios ---
            if busca_manana and h["inicio"] >= "12:00":
                ok = False
            if busca_tarde and h["inicio"] < "12:00":
                ok = False

            if ok:
                horarios_validos.append(h)

        if horarios_validos:
            materias_filtradas.append({
                "materia": nombre,
                "horarios": horarios_validos
            })

    return materias_filtradas

def mostrar_materias_filtradas(materias):
    for m in materias:
        print(f"\nMateria: {m['materia']}")
        for h in m["horarios"]:
            tipo = "Virtual" if h["virtual"] else "Presencial"
            print(f"  - {h['dia']} {h['inicio']}–{h['fin']} ({tipo}, {h['tipo_clase']})")
