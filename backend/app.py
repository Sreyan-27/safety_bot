from flask import Flask, request, jsonify
from routes.audio_routes import audio_bp
from routes.test_routes import test_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(audio_bp, url_prefix="/audio")
app.register_blueprint(test_bp, url_prefix="/test")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Safety Bot Backend Running"}), 200

if __name__ == "__main__":
    app.run(debug=True)
