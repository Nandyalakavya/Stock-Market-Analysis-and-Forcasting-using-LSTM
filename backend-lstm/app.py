from flask import Flask, jsonify, request
from flask_cors import CORS
from lstm_model import predict
import os

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
            return jsonify({"error": "File not found"}), 400

        days_map = {
            "6m": 60,
            "1y": 120,
        }

        print("🔮 Running prediction for", file_path, "days:", days_map[horizon])
        result = predict(file_path, days_map[horizon])
        print("✅ Prediction completed")
        return jsonify(result)

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500


# -----------------------
# App entry point (Render)
# -----------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )