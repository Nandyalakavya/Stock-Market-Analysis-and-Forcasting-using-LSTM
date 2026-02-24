from flask import Flask, jsonify, request
from flask_cors import CORS
from lstm_model import predict
import os
import traceback

app = Flask(__name__)
CORS(app)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


@app.route("/")
def home():
    return jsonify({"status": "Backend running"})


@app.route("/files")
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


@app.route("/predict")
def run_prediction():
    try:
        file = request.args.get("file")
        horizon = request.args.get("horizon", "6m")

        if not file:
            return jsonify({"error": "File not selected"}), 400

        file_path = os.path.join(DATA_DIR, file)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 400

        # 🔴 SAME logic, just safe fallback
        days_map = {
            "6m": 60,
            "1y": 80,
            "2y": 100,
        }

        days = days_map.get(horizon, 180)

        print("🔮 Running prediction:", file_path, "Days:", days)

        result = predict(file_path, days)

        print("✅ Prediction completed")
        return jsonify(result)

    except Exception as e:
        print("❌ Prediction error")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# 🔴 Render-safe entry point (ONLY required change)
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )