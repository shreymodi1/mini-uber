import logging
from flask import Flask, request, jsonify
from typing import Any, Dict
import demo_api  # TODO: Ensure demo_api.py is in the correct import path

logger = logging.getLogger(__name__)


def create_flask_app() -> Flask:
    """
    Initializes a Flask application and sets up routes that internally call demo_api functions.

    Returns:
        Flask: A configured Flask application instance.
    """
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def serve_frontend() -> Any:
        """
        Serves the main page for the React frontend.
        TODO: Update this to serve your React build or a static file if needed.

        Returns:
            A simple JSON response with a placeholder message.
        """
        return jsonify({"message": "React frontend placeholder"}), 200

    @app.route("/api/hello", methods=["GET"])
    def hello_world() -> Any:
        """
        Example endpoint that calls demo_api to return a greeting message.

        Returns:
            A JSON response containing a greeting message or an error.
        """
        try:
            greeting = demo_api.get_greeting()
            return jsonify({"message": greeting}), 200
        except Exception as exc:
            logger.exception("Error retrieving greeting")
            return jsonify({"error": str(exc)}), 500

    @app.route("/api/items", methods=["POST"])
    def create_item() -> Any:
        """
        Creates a new item by calling the demo_api create_item function.

        Returns:
            A JSON response containing the newly created item or an error.
        """
        try:
            payload: Dict[str, Any] = request.json
            new_item = demo_api.create_item(payload)
            return jsonify({"created_item": new_item}), 201
        except Exception as exc:
            logger.exception("Error creating item")
            return jsonify({"error": str(exc)}), 500

    # TODO: Add more endpoints to support your React frontend as needed

    return app


def run_demo_app() -> None:
    """
    Runs the Flask application on a specified host and port.
    Launch by executing `python demo_app.py`.
    """
    logging.basicConfig(level=logging.INFO)
    application = create_flask_app()
    # TODO: For production, consider using a production WSGI server like Gunicorn or uWSGI
    application.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    run_demo_app()