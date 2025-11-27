# ui.py
from datetime import datetime

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

# Entrada segura y preguntas
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
