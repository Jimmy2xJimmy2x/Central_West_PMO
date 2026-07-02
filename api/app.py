"""Flask application factory"""

import sys
from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.routes import tasks, timeblocks, recurring, notes


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(tasks.bp)
    app.register_blueprint(timeblocks.bp)
    app.register_blueprint(recurring.bp)
    app.register_blueprint(notes.bp)

    # Serve static files from web/dist/ (production)
    web_dist = Path(__file__).parent.parent / "web" / "dist"

    @app.route("/")
    def index():
        if web_dist.exists():
            return send_from_directory(web_dist, "index.html")
        return {"message": "PMO Management Assistant API", "version": "0.1.0"}

    @app.route("/<path:path>")
    def serve_static(path):
        if web_dist.exists() and (web_dist / path).exists():
            return send_from_directory(web_dist, path)
        # Return index.html for client-side routing
        if web_dist.exists():
            return send_from_directory(web_dist, "index.html")
        return {"error": "Not found"}, 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
