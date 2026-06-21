from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "trivy-demo-app"}), 200

@app.route("/")
def index():
    return jsonify({
        "app": "Trivy Container Security Demo",
        "version": "1.0.0",
        "description": "Sample application used to demonstrate Trivy container vulnerability scanning in CI/CD."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
