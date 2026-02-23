from flask import Flask, jsonify, request
from flask_cors import CORS
from lstm_model import predict
import os
import pandas as pd
import traceback

app = Flask(__name__)
CORS(app)

# -----------------------
# Data directory setup
# -----------------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------
# Routes
# -----------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend running"})


@app.route("/files", methods=["GET"])
def files():
    return jsonify(os.listdir(DATA_DIR))


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    save_path = os.path.join(DATA_DIR, file.filename)
    file.save(save_path)

    return jsonify({"message": "File uploaded successfully"})


@app.route("/predict", methods=["GET"])
def run_prediction():
    try:
        file = request.args.get("file")
        horizon = request.args.get("horizon", "6m")

        if not file:
            return jsonify({"error": "File not selected"}), 400

        file_path = os.path.join(DATA_DIR, file)
        if not os.path.exists(file_path):
            return jsonify({"error": f"File not found: {file_path}"}), 400

        # 🔴 SAFE limits for Render Free tier
        days_map = {
            "6m": 30,
            "1y": 60
        }

        days = days_map.get(horizon, 30)

        print("📄 File:", file_path)
        print("📅 Horizon days:", days)

        # 🔴 Reduce CSV size to avoid MemoryError
        df = pd.read_csv(file_path)
        df = df.tail(500)          # LIMIT rows (CRITICAL FIX)
        temp_path = os.path.join(DATA_DIR, "temp.csv")
        df.to_csv(temp_path, index=False)

        print("🚀 Starting LSTM prediction...")
        result = predict(temp_path, days)
        print("✅ Prediction completed")

        return jsonify(result)

    except Exception as e:
        print("❌ Prediction crashed")
        traceback.print_exc()
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500


# -----------------------
# App entry point (Render)
# -----------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )