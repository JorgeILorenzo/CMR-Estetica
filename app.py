from flask import Flask, render_template, request, redirect
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

pacientes = []
citas = []

def generar_resumen(nombre, motivo):
    prompt = f"Paciente: {nombre}. Motivo de consulta: {motivo}. Redactá un resumen clínico profesional y breve."
    try:
        respuesta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return respuesta.choices[0].text.strip()
    except Exception as e:
        return f"Error generando resumen: {e}"

@app.route("/")
def index():
    return render_template("index.html", pacientes=pacientes, citas=citas)

@app.route("/agregar_paciente", methods=["POST"])
def agregar_paciente():
    nombre = request.form["nombre"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    motivo = request.form["motivo"]
    resumen = generar_resumen(nombre, motivo)
    pacientes.append({"nombre": nombre, "email": email, "telefono": telefono, "motivo": motivo, "resumen": resumen})
    return redirect("/")

@app.route("/agendar_cita", methods=["POST"])
def agendar_cita():
    paciente = request.form["paciente"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    procedimiento = request.form["procedimiento"]
    citas.append({"paciente": paciente, "fecha": fecha, "hora": hora, "procedimiento": procedimiento})
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
