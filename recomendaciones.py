# recomendaciones.py
# ============================================================
#  MÓDULO DE RECOMENDACIONES PERSONALIZADAS (Conversacionales)
# ============================================================

recomendaciones_personales = {
    "A": (
        "Trata de dedicar al menos una hora diaria a cada materia importante. No hace falta que lo hagas todo junto: "
        "podés repartirlo entre mañana, tarde o noche según cuándo te sientas más despejado. "
        "Lo importante es mantener ese pequeño hábito todos los días. Esa hora constante te ayuda a no atrasarte, "
        "a entender mejor los temas y a llegar más tranquilo a los parciales."
    ),

    "B": (
        "Trata de avanzar al ritmo de la materia para que no se te acumule todo. "
        "Cada clase suma, y si vas repasando lo que ves semana a semana, llegas a los parciales mucho más tranquilo. "
        "Hacé un repaso corto después de cada clase: 10 o 15 minutos alcanzan para fijar lo más importante y evitar atrasarte."
    ),

    "C": (
        "Si podés, rendí los finales apenas termina la cursada. "
        "Tenés todos los temas fresquitos y necesitás mucho menos esfuerzo para estudiar. "
        "Además, te evitás acumular finales más adelante, cuando cuesta retomar y se hace todo más pesado."
    ),

    "D": (
        "Si una materia se puede promocionar, tratá de aprovecharlo. "
        "Estudiar un poco todas las semanas y cumplir con los parciales te puede ahorrar rendir un final entero más adelante. "
        "Además, cuando promocionás una materia, sentís que avanzás más rápido y te sacás un peso enorme de encima."
    ),

    "E": (
        "Ir a clase y tomar apuntes propios te da una ventaja enorme. "
        "Muchas veces los profes explican qué temas son clave, cuáles suelen tomar en parciales o finales, "
        "e incluso aclaran errores de sus propias diapositivas. "
        "Si faltás, te perdés esas aclaraciones importantes y estudiar solo desde las diapos te puede jugar en contra. "
        "Anotá todo lo que el profe recalca, explica o corrige: esos detalles después marcan la diferencia."
    ),

    "F": (
        "Establecer un tiempo fijo para cada materia te ordena muchísimo. "
        "Puede ser media hora, una hora o lo que tengas, pero lo importante es que sea constante. "
        "Cuando sabés que todos los días le dedicás ese ratito a cada materia, evitás atrasarte, "
        "estudiás más relajado y llegás a los parciales con todo más fresquito."
    ),

    "G": (
        "Si estás trabajando en doble turno, es clave organizar bien tus tiempos para no agotarte. "
        "Elegí horarios de cursada donde estés más despierto y repartí el estudio en bloques cortitos para no saturarte. "
        "No te exijas como alguien que tiene todo el día libre: ajustá tu ritmo a tu realidad. "
        "Con buena organización podés avanzar sin quemarte, incluso con un trabajo pesado."
    ),

    "I": (
        "A veces la carrera puede sentirse larga o pesada, pero no olvides por qué empezaste ni lo lejos que ya llegaste. "
        "Avanzá a tu propio ritmo y no te compares con los demás: cada persona aprende distinto. "
        "Buscá apoyo en compañeros avanzados, parciales viejos o material extra cuando algo se te haga difícil. "
        "Y sobre todo: seguí aunque sea de a poquito. Cada avance suma."
    ),

    "K": (
        "Hay técnicas de estudio que les funcionaron a muchos estudiantes avanzados y te pueden servir a vos también. "
        "Hacé resúmenes propios y mapas conceptuales para entender materias largas o teóricas. "
        "Si es una materia práctica, lo mejor es hacer ejercicios. "
        "Usá videotutoriales cuando algo no te quede claro. "
        "Probá el método Pomodoro para concentrarte sin agotarte. "
        "Usá Anki o repaso espaciado para memorizar. "
        "Practicá con parciales anteriores; muchos profes repiten estilo. "
        "Pedile a la IA preguntas tipo examen para practicar más. "
        "Probá todo de a poco y quedate con lo que mejor te funcione."
    ),

    "L": (
        "Aquí te muestro las materias que se dictan a la mañana para que puedas organizar mejor tu cursada."
    ),

    "M": (
        "Si tenés poco tiempo por el trabajo o te cuesta llegar a la facultad, aprovechar las clases virtuales te puede salvar. "
        "Te permiten organizarte mejor, avanzar a tu ritmo y no perder contenido. "
        "Además podés pausar o volver a ver explicaciones cuando algo no te quede claro."
    ),

    "N": (
        "Aquí te muestro las materias que se dictan a la tarde para que puedas organizar mejor tu cursada."
    ),

    "R": (
        "Hacer un curso nivelatorio antes de empezar el año te puede ayudar muchísimo si venís flojo en algún tema. "
        "Te sirve para recuperar bases, entender mejor las materias del primer año y arrancar el cuatrimestre con más seguridad. "
        "No es tiempo perdido: al contrario, te ahorra problemas después."
    )
}


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
                "Veo que trabajás por la {0}. Puedo ofrecerte las siguientes recomendaciones para facilitar tu cursada universitaria:"
            ).format(turnos_desc[turno_trabajo])
        )
    else:
        mensajes.append(
            "Como tu principal foco es el estudio, Puedo ofrecerte las siguientes recomendaciones para facilitar tu cursada universitaria:"
        )

    # ------------------------------------------------------------
    # Recomendaciones sedun los Hechos Finales o Inferidos
    # ------------------------------------------------------------
  
    for codigo in finales:
      if codigo in recomendaciones_personales:
         mensajes.append(recomendaciones_personales[codigo])

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

