# recomendaciones.py
# ============================================================
#  MÓDULO DE RECOMENDACIONES PERSONALIZADAS (Conversacionales)
# ============================================================

def generar_recomendaciones_conversacionales(finales, hechos_usuario):
    """
    Genera una lista de mensajes personalizados según:
    - Hechos finales inferidos por el sistema (finales) : iterable (set/list) de códigos de hechos
    - Hechos declarados explícitamente por el usuario (hechos_usuario) : set de hechos declarados
    """
    mensajes = []
    turnos_desc = {
        "AC": "mañana",
        "AD": "tarde",
        "AE": "noche",
    }

    # Detectar en qué turno trabaja el usuario (si corresponde)
    turno_trabajo = next((t for t in turnos_desc if t in hechos_usuario), None)

    # ------------------------------------------------------------
    # Recomendaciones según TURNOS
    # ------------------------------------------------------------
    if turno_trabajo:
        mensajes.append(
            (
                "Veo que trabajás por la {0}. Aprovechá los huecos libres "
                "para repasar apuntes cortos y, si podés, reservá bloques fijos "
                "los días en que estés más descansado para avanzar con temas clave."
            ).format(turnos_desc[turno_trabajo])
        )
    else:
        mensajes.append(
            "Como tu principal foco es el estudio, organizá una rutina estable "
            "con descansos breves entre materias para sostener el ritmo sin saturarte."
        )

    # ------------------------------------------------------------
    # Recomendaciones según HORARIOS Y MODALIDAD
    # ------------------------------------------------------------
    if "M" in finales or "N" in finales or "L" in finales:
        mensajes.append(
            "Elegí comisiones que se adapten a tu energía: si rendís mejor en la mañana, "
            "apostá por esos horarios; si necesitás flexibilidad, combiná clases virtuales "
            "con materiales asincrónicos para no perder continuidad."
        )

    # ------------------------------------------------------------
    # Recomendación por materias troncales
    # ------------------------------------------------------------
    if "T" in finales:
        mensajes.append(
            "Dale prioridad a las materias troncales. Tenerlas al día te abre la puerta "
            "a cuatrimestres más livianos y te permite promocionar sin retrasos innecesarios."
        )

    # ------------------------------------------------------------
    # Recomendación según nivel de agotamiento / intensidad
    # ------------------------------------------------------------
    if "BB" in finales or "II" in finales:
        mensajes.append(
            "No descuides el descanso: programá pausas y espacios recreativos cortos. "
            "Un cuerpo y una mente descansados rinden más en parciales y proyectos."
        )

    # ------------------------------------------------------------
    # Recomendación para usuarios con poco tiempo (U, FF)
    # ------------------------------------------------------------
    if "U" in finales or "FF" in finales:
        mensajes.append(
            "Aprovechá tiempos muertos (viajes, colas, pausas) para revisar resúmenes breves "
            "o tarjetas de memoria. Pequeños avances constantes generan grandes resultados."
        )

    # ------------------------------------------------------------
    # Recomendación genérica si nada coincidió
    # ------------------------------------------------------------
    if not mensajes:
        mensajes.append(
            "Con la información que compartiste, organizá una planificación semanal con hitos "
            "claros (lecturas, ejercicios, consultas) y revisá tu progreso cada domingo."
        )

    return mensajes


def imprimir_recomendaciones_conversacionales(finales, hechos_usuario, solo_devolver=False):
    """
    Imprime recomendaciones personalizadas basada en hechos inferidos
    y hechos declarados por el usuario.

    Parámetros:
    - finales: iterable con códigos de hechos finales (por ejemplo set o list)
    - hechos_usuario: set con hechos declarados por el usuario (ej. {'AC','AG'})
    - solo_devolver: si True, NO imprime y devuelve lista; si False (por defecto) imprime y devuelve lista.
    """
    mensajes = generar_recomendaciones_conversacionales(finales, hechos_usuario)

    if not solo_devolver:
        print("\n=== RECOMENDACIONES PERSONALIZADAS ===")
        for mensaje in mensajes:
            print(f"• {mensaje}")

    return mensajes

