"""
Full-Stack Flask Backend Application for Mukund Pratap Srivastav's Portfolio
Serves RESTful API endpoints, SQLite persistence, and static frontend assets.
"""

import os
import re
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
import database
import mailer

# Initialize Flask App
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

# Initialize SQLite database on startup
database.init_db()

# --- CORS & Security Headers Middleware ---
@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# --- Static File Serving ---
@app.route('/')
def serve_index():
    """Serves Mukund Pratap Srivastav's portfolio frontend."""
    database.log_event("page_view", f"IP: {request.remote_addr}")
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static_file(filename):
    """Serves CSS, JS, Assets, and other static assets."""
    target_path = os.path.join(BASE_DIR, filename)
    if os.path.isfile(target_path):
        return send_from_directory(BASE_DIR, filename)
    return jsonify({"error": "File not found"}), 404

# --- Public REST API Endpoints ---

@app.route('/api/health', methods=['GET'])
def health_check():
    """System health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Mukund Pratap Srivastav Portfolio Engine",
        "backend": "Flask 3.1.3",
        "database": "SQLite 3",
        "server_time": datetime.now().isoformat(),
        "endpoints": [
            "/api/health",
            "/api/stats",
            "/api/contact",
            "/api/projects/likes",
            "/api/projects/like",
            "/api/subscribe",
            "/api/terminal"
        ]
    }), 200

@app.route('/api/stats', methods=['GET'])
def get_public_stats():
    """Returns live aggregated statistics."""
    summary = database.get_dashboard_summary()
    return jsonify({
        "success": True,
        "data": summary
    }), 200

@app.route('/api/contact', methods=['POST'])
def submit_contact_form():
    """
    Handles contact form submissions from the frontend.
    Validates input, writes to SQLite, and sends email notification.
    """
    data = request.get_json(silent=True) or request.form.to_dict()
    
    if not data:
        return jsonify({"success": False, "error": "Invalid request payload."}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    subject = data.get('subject', 'General Inquiry').strip()
    message = data.get('message', '').strip()

    # Validation
    if not name or len(name) < 2:
        return jsonify({"success": False, "error": "Please provide your name (at least 2 characters)."}), 400

    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"success": False, "error": "Please provide a valid email address."}), 400

    if not message or len(message) < 5:
        return jsonify({"success": False, "error": "Message must be at least 5 characters."}), 400

    # Save to SQLite
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    msg_id = database.save_message(name, email, subject, message, ip)

    # Dispatch email notification
    email_sent, email_status, gmail_compose_url = mailer.send_contact_email(name, email, subject, message)

    return jsonify({
        "success": True,
        "message": f"Thank you, {name}! Your message has been sent to Mukund Pratap Srivastav.",
        "message_id": msg_id,
        "email_sent": email_sent,
        "email_status": email_status,
        "gmail_compose_url": gmail_compose_url,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 201

@app.route('/api/projects/likes', methods=['GET'])
def get_project_likes():
    """Retrieves all project likes and views counts."""
    stats = database.get_all_project_stats()
    return jsonify({
        "success": True,
        "projects": stats
    }), 200

@app.route('/api/projects/like', methods=['POST'])
def like_project():
    """Increments like count for a project."""
    data = request.get_json(silent=True) or {}
    project_id = data.get('projectId', '').strip()

    if not project_id:
        return jsonify({"success": False, "error": "Project ID is required."}), 400

    new_count = database.increment_project_like(project_id)
    return jsonify({
        "success": True,
        "project_id": project_id,
        "likes": new_count
    }), 200

@app.route('/api/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Subscribes an email to technical updates."""
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()

    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"success": False, "error": "Valid email address required."}), 400

    success, msg = database.add_subscriber(email)
    status_code = 201 if success else 400
    return jsonify({
        "success": success,
        "message": msg
    }), status_code

@app.route('/api/terminal', methods=['POST'])
def process_terminal_command():
    """Processes interactive CLI terminal queries via the backend."""
    data = request.get_json(silent=True) or {}
    command = data.get('command', '').strip().lower()

    if not command:
        return jsonify({"output": ""}), 200

    database.log_event("terminal_cmd", command)

    # Dynamic Backend Commands
    if command == 'stats':
        summary = database.get_dashboard_summary()
        output = f"""[Live Backend Metrics (SQLite Database)]
• Total Page Views:     {summary['total_page_views']}
• Project Likes:        {summary['total_project_likes']}
• Contact Messages:     {summary['total_messages']}
• Subscribers:          {summary['total_subscribers']}
• Backend Status:       Flask 3.1.3 Active & Healthy (Port {os.environ.get('PORT', 5001)})"""
        return jsonify({"output": output, "status": "info"}), 200

    elif command in ('db', 'database'):
        output = f"""[SQLite Database Status]
• Database Location: {database.DB_PATH}
• Active Tables:    messages, project_likes, subscribers, analytics
• ACID Compliance:  Full SQLite WAL transaction support"""
        return jsonify({"output": output, "status": "accent"}), 200

    return jsonify({"fallback": True}), 200

# --- Main Entry Point ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print("\n========================================================")
    print(">> Mukund Pratap Srivastav Full-Stack Portfolio Server Running!")
    print(f">> Local URL:  http://localhost:{port}")
    print(f">> Database:   {database.DB_PATH}")
    print("========================================================\n")
    app.run(host='0.0.0.0', port=port, debug=False)
