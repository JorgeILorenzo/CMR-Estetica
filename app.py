from flask import Flask, render_template, request, redirect
import openai
import os
from datetime import datetime

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

patients = []
appointments = []

@app.route("/")
def home():
    return render_template("home.html", patients=patients, appointments=appointments)

@app.route("/nuevo", methods=["POST"])
def nuevo_paciente():
    nombre = request.form["nombre"]
    motivo = request.form["motivo"]
    resumen = generar_resumen_clinico(motivo)
    patients.append({"nombre": nombre, "motivo": motivo, "resumen": resumen})
    return redirect("/")

@app.route("/cita", methods=["POST"])
def agendar_cita():
    nombre = request.form["nombre"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    appointments.append({"nombre": nombre, "fecha": fecha, "hora": hora})
    return redirect("/")

def generar_resumen_clinico(motivo):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Resumen clínico para consulta estética basada en el motivo: {motivo}",
        max_tokens=60
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)