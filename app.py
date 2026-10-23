
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    """Display the application status."""
    return jsonify(
        application="Jenkins CI/CD Demo",
        status="running",
        message="Deployment successful!"
    ), 200


@app.get("/health")
def health():
    """Health-check endpoint for deployment verification."""
    return jsonify(
        status="healthy"
    ), 200


@app.errorhandler(404)
def not_found(error):
    """Return JSON for routes that do not exist."""
    return jsonify(
        status="error",
        message="Endpoint not found"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Return a generic JSON response for server errors."""
    return jsonify(
        status="error",
        message="Internal server error"
    ), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
