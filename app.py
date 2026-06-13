import asyncio
import logging
import traceback
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Import the agent (this triggers index loading on startup)
logger.info("Initializing DocSense AI agent...")
from main import run_agent

logger.info("Agent ready.")


@app.route("/")
def index():
    """Serve the chat frontend."""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "agent": "DocSense AI"})


@app.route("/api/chat", methods=["POST"])
def chat():
    """Process a chat message through the agent."""
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field in request body."}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        logger.info(f"Processing query: {user_message[:80]}...")
        response = asyncio.run(run_agent(user_message))
        logger.info("Query processed successfully.")
        return jsonify({"response": response})

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Agent error: {error_msg}")
        logger.error(traceback.format_exc())

        # Detect rate limit errors and return a friendly message
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return jsonify({
                "error": "The AI service is currently rate-limited. Please wait a moment and try again.",
                "error_type": "rate_limit"
            }), 429

        return jsonify({
            "error": "An unexpected error occurred while processing your request. Please try again.",
            "error_type": "server_error"
        }), 500


if __name__ == "__main__":
    print("\n>>> DocSense AI is running at http://localhost:5000\n")
    app.run(debug=False, host="0.0.0.0", port=5000)
