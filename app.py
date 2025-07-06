from flask import Flask, render_template, request, redirect
import openai
import os

app = Flask(__name__)

# Configuración de la API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Datos simulados
pacientes = []
citas = []

def generar_resumen_clinico(nombre, motivo):
    try:
        prompt = f"Paciente: {nombre}\nMotivo de consulta: {motivo}\nGenera un breve resumen clínico profesional:"
        respuesta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return respuesta.choices[0].text.strip()
    except Exception as e:
        return f"Error al generar resumen: {e}"

@app.route("/")
def index():
    return render_template("index.html", pacientes=pacientes, citas=citas)

@app.route("/agregar_paciente", methods=["POST"])
def agregar_paciente():
    nombre = request.form["nombre"]
    motivo = request.form["motivo"]
    resumen = generar_resumen_clinico(nombre, motivo)
    pacientes.append({"nombre": nombre, "motivo": motivo, "resumen": resumen})
    return redirect("/")

@app.route("/agendar_cita", methods=["POST"])
def agendar_cita():
    nombre = request.form["nombre_cita"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    citas.append({"nombre": nombre, "fecha": fecha, "hora": hora})
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
