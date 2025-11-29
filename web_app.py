"""Aplicación Flask para interactuar con el sistema experto desde la web."""
from datetime import datetime
import io
import sys
from typing import Dict, Optional

from flask import Flask, render_template, request

from engine_utils import imprimir_trazabilidad, preparar_engine
from hechos import Perfil
from reglas import SistemaEducativo
from resumen import imprimir_todo_unificado

app = Flask(__name__)


# ==== Lógica de generación del resumen ====
def _obtener_saludo() -> str:
    """Devuelve un saludo dinámico según la hora actual."""

    hora = datetime.now().hour
    if 6 <= hora < 12:
        return "¡Buen día! ☀️"
    if 12 <= hora < 18:
        return "¡Buenas tardes! 🌤️"
    if 18 <= hora < 24:
        return "¡Buenas noches! 🌙"
    return "Wow, estás conectado/a a la madrugada 😴 — ¡sos un crack!"


def generar_resumen(nombre: str, respuestas: Dict[str, Optional[bool]]) -> str:
    """Ejecuta el motor de inferencia y devuelve el resultado como texto plano."""

    nombre_normalizado = (nombre or "").strip() or "Estudiante"

    buffer = io.StringIO()
    stdout_original = sys.stdout
    sys.stdout = buffer
    try:
        print(_obtener_saludo())
        print("Soy tu asistente de la Facultad de Ingeniería (UNJu).")
        print(
            "Voy a usar tus respuestas para armar tu perfil y darte recomendaciones de estudio que realmente te sirvan. 🤝\n"
        )

        print(">>> Ejecutando inferencia...\n")
        engine, hechos_usuario = preparar_engine(respuestas, SistemaEducativo, Perfil)

        imprimir_todo_unificado(engine, hechos_usuario, "reglas.py")
        imprimir_trazabilidad()

        print(f"\n¡Gracias por contarme tu situación, {nombre_normalizado}!")
        print("Recordá que cada paso que das te acerca a tu objetivo académico. 💪")
        print("Seguí adelante con confianza: ¡tenés todo para lograrlo! 🚀")
    finally:
        sys.stdout = stdout_original

    return buffer.getvalue()


# ==== Rutas ====
@app.route("/", methods=["GET", "POST"])
def index():
    formulario = {
        "nombre": "",
        "trabaja": "no",
        "turno": "AC",
        "cursa_todo": "si",
        "retoma": "no",
        "dos_carreras": "no",
    }
    resultado = None

    if request.method == "POST":
        formulario["nombre"] = request.form.get("nombre", "").strip()
        formulario["trabaja"] = request.form.get("trabaja", "no")
        formulario["turno"] = request.form.get("turno", "AC")
        formulario["cursa_todo"] = request.form.get("cursa_todo", "si")
        formulario["retoma"] = request.form.get("retoma", "no")
        formulario["dos_carreras"] = request.form.get("dos_carreras", "no")

        respuestas = {
            "trabaja": formulario["trabaja"] == "si",
            "turno_trabajo": formulario["turno"] if formulario["trabaja"] == "si" else None,
            "cursa_todas": formulario["cursa_todo"] == "si",
            "retoma_estudios": formulario["retoma"] == "si",
            "doble_carrera": formulario["dos_carreras"] == "si",
        }

        resultado = generar_resumen(formulario["nombre"], respuestas)

    return render_template("index.html", formulario=formulario, resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)
