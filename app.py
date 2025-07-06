import os
from flask import Flask, render_template, request, redirect, url_for, flash
import openai

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret")  # Needed for flash messages

# In-memory data storage
patients = []
appointments = []

# Configure OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
else:
    print("Warning: OPENAI_API_KEY not set. AI summaries will not work.")

def generate_clinical_summary(name, reason):
    prompt = f"Paciente: {name}, Motivo: {reason}. Redacta un resumen clínico profesional y breve."
    try:
        if not openai.api_key:
            raise ValueError("OpenAI API key not set")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=80,
            temperature=0.7,
        )
        summary = response.choices[0].message["content"].strip()
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "No se pudo generar el resumen clínico automáticamente."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Register patient
        if "register_patient" in request.form:
            name = request.form.get("name", "").strip()
            reason = request.form.get("reason", "").strip()
            if not name or not reason:
                flash("Nombre y motivo de consulta son obligatorios.", "error")
            else:
                summary = generate_clinical_summary(name, reason)
                patients.append({
                    "name": name,
                    "reason": reason,
                    "summary": summary,
                })
                flash("Paciente registrado correctamente.", "success")
            return redirect(url_for("index"))

        # Schedule appointment
        if "schedule_appointment" in request.form:
            patient_name = request.form.get("patient_name", "").strip()
            date = request.form.get("date", "")
            time = request.form.get("time", "")
            if not patient_name or not date or not time:
                flash("Todos los campos para agendar cita son obligatorios.", "error")
            else:
                appointments.append({
                    "patient_name": patient_name,
                    "date": date,
                    "time": time,
                })
                flash("Cita agendada correctamente.", "success")
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        patients=patients,
        appointments=appointments
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)