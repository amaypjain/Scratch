from flask import Flask, jsonify
from src.models import UserProfile, TelemetryData
from src.context_engine import ContextEngine
from src.jitai_engine import JITAI_Engine
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Health AI App Running 🚀"

@app.route("/simulate")
def simulate():
    context_engine = ContextEngine()
    jitai = JITAI_Engine()

    user = UserProfile("U-1", "routine_eater")

    telemetry = TelemetryData(
        timestamp=datetime.datetime.now(),
        hrv=20,
        sleep_score=40,
        blood_glucose=65,
        lat=34.0522,
        lon=-118.2437
    )

    context = context_engine.evaluate_context(telemetry)
    nudge = jitai.generate_intervention(user, context)

    return jsonify({
        "vulnerability_score": context.vulnerability_score,
        "nudge": nudge
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
