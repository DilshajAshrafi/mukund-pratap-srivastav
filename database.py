"""
Database Layer for Mukund's Portfolio
Handles SQLite database initialization, models, queries, and persistent storage.
"""

import os
import sqlite3
from datetime import datetime

# Database directory and file path
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DB_PATH = os.path.join(DB_DIR, 'portfolio.db')

def get_db_connection():
    """Returns a SQLite database connection with row factory configured."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes database tables and default seed records."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Contact Messages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_read INTEGER DEFAULT 0,
            ip_address TEXT
        )
    ''')

    # 2. Project Likes & Views Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_likes (
            project_id TEXT PRIMARY KEY,
            project_name TEXT NOT NULL,
            likes_count INTEGER DEFAULT 0,
            views_count INTEGER DEFAULT 0,
            last_liked_at TIMESTAMP
        )
    ''')

    # 3. Newsletter Subscribers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. Analytics & Activity Log Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Seed initial projects if not present
    default_projects = [
        ('cloud_platform', 'Cloud-Native Microservices Platform', 42, 280),
        ('smart_analytics', 'Smart Agro & IoT Analytics Engine', 38, 230),
        ('realtime_collab', 'Real-Time Collaborative Code Studio', 31, 175),
        ('dev_pulse', 'DevPulse Engineering Observability Suite', 27, 140)
    ]

    for proj_id, name, likes, views in default_projects:
        cursor.execute('''
            INSERT OR IGNORE INTO project_likes (project_id, project_name, likes_count, views_count)
            VALUES (?, ?, ?, ?)
        ''', (proj_id, name, likes, views))

    conn.commit()
    conn.close()

# --- Message Operations ---

def save_message(name, email, subject, message, ip=None):
    """Inserts a new contact submission into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (name, email, subject, message, ip_address)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, subject, message, ip))
    msg_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Log analytics
    log_event("contact_submission", f"From: {name} <{email}>")
    return msg_id

def get_all_messages(limit=50):
    """Retrieves all contact messages ordered by newest first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --- Project Likes Operations ---

def increment_project_like(project_id):
    """Increments the like counter for a project."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute('''
        UPDATE project_likes
        SET likes_count = likes_count + 1, last_liked_at = ?
        WHERE project_id = ?
    ''', (now, project_id))

    if cursor.rowcount == 0:
        cursor.execute('''
            INSERT INTO project_likes (project_id, project_name, likes_count, last_liked_at)
            VALUES (?, ?, 1, ?)
        ''', (project_id, project_id.replace('_', ' ').title(), now))

    cursor.execute('SELECT likes_count FROM project_likes WHERE project_id = ?', (project_id,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()

    log_event("project_liked", f"Project: {project_id}")
    return row['likes_count'] if row else 1

def get_all_project_stats():
    """Retrieves all project likes and views."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM project_likes')
    rows = cursor.fetchall()
    conn.close()
    return {row['project_id']: dict(row) for row in rows}

# --- Subscribers Operations ---

def add_subscriber(email):
    """Adds a new email subscriber."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO subscribers (email) VALUES (?)', (email,))
        conn.commit()
        conn.close()
        log_event("newsletter_signup", f"Email: {email}")
        return True, "Subscription successful!"
    except sqlite3.IntegrityError:
        return False, "This email is already subscribed."
    except Exception as e:
        return False, str(e)

# --- Analytics Operations ---

def log_event(event_type, metadata=None):
    """Logs an internal analytics event."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO analytics (event_type, metadata)
            VALUES (?, ?)
        ''', (event_type, metadata))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_dashboard_summary():
    """Returns aggregated metrics for portfolio stats."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) AS total FROM messages')
    total_messages = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) AS unread FROM messages WHERE is_read = 0')
    unread_messages = cursor.fetchone()['unread']

    cursor.execute('SELECT SUM(likes_count) AS total_likes FROM project_likes')
    row = cursor.fetchone()
    total_likes = row['total_likes'] or 0

    cursor.execute('SELECT COUNT(*) AS subscribers FROM subscribers')
    subscribers = cursor.fetchone()['subscribers']

    cursor.execute('SELECT COUNT(*) AS page_views FROM analytics WHERE event_type = "page_view"')
    page_views = cursor.fetchone()['page_views']

    conn.close()

    return {
        "total_messages": total_messages,
        "unread_messages": unread_messages,
        "total_project_likes": total_likes,
        "total_subscribers": subscribers,
        "total_page_views": page_views + 120 # Base traffic baseline
    }
