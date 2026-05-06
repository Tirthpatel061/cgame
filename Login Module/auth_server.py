import json
import os
import re
import secrets
import hashlib
import subprocess
import sys
from datetime import datetime, timedelta
from email.message import EmailMessage

from flask import Flask, jsonify, request
from flask_cors import CORS
from mysql.connector import pooling, Error
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import smtplib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "c_game_db")

AUTH_PORT = int(os.getenv("AUTH_PORT", "5002"))
AUTH_DEBUG = os.getenv("AUTH_DEBUG", "true").lower() == "true"

OTP_EXPIRY_MINUTES = int(os.getenv("OTP_EXPIRY_MINUTES", "10"))
OTP_SALT = os.getenv("OTP_SALT", "dev-otp-salt")
ALLOW_DEV_OTP = os.getenv("ALLOW_DEV_OTP", "true").lower() == "true"

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
SMTP_STARTTLS = os.getenv("SMTP_STARTTLS", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SMTP_ENABLED = all([SMTP_HOST, SMTP_USER, SMTP_PASS, SMTP_FROM])

USER_STORE_PATH = os.path.join(BASE_DIR, "user_store.json")

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

pool = pooling.MySQLConnectionPool(
    pool_name="auth_pool",
    pool_size=5,
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    autocommit=True
)

app = Flask(__name__)
CORS(app)


def get_connection():
    return pool.get_connection()


def ensure_user_store():
    if not os.path.exists(USER_STORE_PATH):
        with open(USER_STORE_PATH, "w", encoding="utf-8") as file:
            json.dump([], file, indent=2)


def read_user_store():
    ensure_user_store()
    try:
        with open(USER_STORE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def write_user_store(data):
    with open(USER_STORE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def upsert_user_store(user_record):
    data = read_user_store()
    updated = False
    for index, record in enumerate(data):
        if record.get("email") == user_record.get("email"):
            data[index] = {**record, **user_record}
            updated = True
            break
    if not updated:
        data.append(user_record)
    write_user_store(data)


def sync_json_users_to_db():
    users = read_user_store()
    if not users:
        return
    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            for record in users:
                email = record.get("email")
                username = record.get("username")
                password_hash = record.get("password_hash")
                if not email or not username or not password_hash:
                    continue
                cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, password_hash)
                )
                user_id = cursor.lastrowid
                initialize_user_progress(conn, user_id, username)
            cursor.close()
    except Error:
        return


def initialize_user_progress(conn, user_id, username):
    default_progress = json.dumps({
        "unlockedLevels": [1],
        "completedLevels": [],
        "currentLevel": 1
    })
    default_player_data = json.dumps({
        "name": username,
        "xp": 0,
        "health": 100,
        "totalTasksCompleted": 0
    })
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_progress (user_id, level_progress, player_data) VALUES (%s, %s, %s)",
        (user_id, default_progress, default_player_data)
    )
    cursor.execute(
        "INSERT INTO player_stats (user_id, xp, health, current_level) VALUES (%s, %s, %s, %s)",
        (user_id, 0, 100, 1)
    )
    cursor.close()


def generate_otp():
    return f"{secrets.randbelow(1000000):06d}"


def hash_otp(otp):
    return hashlib.sha256(f"{otp}{OTP_SALT}".encode("utf-8")).hexdigest()


def send_otp_email(to_email, otp, for_reset=False):
    if not SMTP_ENABLED:
        return False, "SMTP is not configured"

    msg = EmailMessage()
    if for_reset:
        msg["Subject"] = "Password Reset - OTP Code"
        msg["From"] = f"Game Warrior <{SMTP_FROM}>"
        msg["To"] = to_email
        msg.set_content(
            f"Your password reset code is {otp}. It expires in {OTP_EXPIRY_MINUTES} minutes. "
            "If you did not request this, please ignore this email."
        )
    else:
        msg["Subject"] = "Your OTP Verification Code"
        msg["From"] = f"Game Warrior <{SMTP_FROM}>"
        msg["To"] = to_email
        msg.set_content(
            f"Your verification code is {otp}. It expires in {OTP_EXPIRY_MINUTES} minutes."
        )

    try:
        if SMTP_USE_SSL or SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.ehlo()
                if SMTP_STARTTLS:
                    server.starttls()
                    server.ehlo()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        return True, ""
    except Exception as exc:
        return False, str(exc)


@app.route("/auth/health", methods=["GET"])
def health_check():
    return jsonify({"ok": True})


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    identifier = (data.get("identifier") or "").strip()
    password = data.get("password") or ""

    if not identifier or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    "SELECT id, username, email, password FROM users WHERE email = %s OR username = %s",
                    (identifier, identifier)
                )
                user = cursor.fetchone()
                if not user or not check_password_hash(user["password"], password):
                    return jsonify({"success": False, "message": "Invalid credentials"}), 401

                cursor.execute(
                    "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s",
                    (user["id"],)
                )

                return jsonify({
                    "success": True,
                    "message": "Login successful",
                    "user": {
                        "id": user["id"],
                        "username": user["username"],
                        "email": user["email"]
                    }
                })
            finally:
                cursor.close()
    except Error as exc:
        return jsonify({"success": False, "message": f"Database error: {exc}"}), 500


@app.route("/auth/request-otp", methods=["POST"])
def request_otp():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"success": False, "message": "Invalid email format"}), 400

    if len(password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400

    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    "SELECT id FROM users WHERE email = %s OR username = %s",
                    (email, username)
                )
                if cursor.fetchone():
                    return jsonify({"success": False, "message": "User already exists"}), 409

                password_hash = generate_password_hash(password)
                cursor.execute(
                    """
                    INSERT INTO pending_users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE username = VALUES(username), password_hash = VALUES(password_hash)
                    """,
                    (username, email, password_hash)
                )

                otp_code = generate_otp()
                expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
                otp_hash = hash_otp(otp_code)
                cursor.execute(
                    """
                    INSERT INTO email_otps (email, otp_hash, expires_at, used, purpose)
                    VALUES (%s, %s, %s, %s, 'signup')
                    """,
                    (email, otp_hash, expires_at, False)
                )
            finally:
                cursor.close()

            email_sent, smtp_error = send_otp_email(email, otp_code)
            if not email_sent and not ALLOW_DEV_OTP:
                return jsonify({"success": False, "message": f"Failed to send OTP: {smtp_error}"}), 500

            response = {"success": True, "message": "OTP sent"}
            if not email_sent:
                response["smtp_error"] = smtp_error or "Email not sent"
                if ALLOW_DEV_OTP:
                    response["dev_otp"] = otp_code
            return jsonify(response)
    except Error as exc:
        return jsonify({"success": False, "message": f"Database error: {exc}"}), 500


@app.route("/auth/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    otp = (data.get("otp") or "").strip()

    if not email or not otp:
        return jsonify({"success": False, "message": "Email and OTP are required"}), 400

    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    """
                    SELECT id, otp_hash, expires_at, used, purpose
                    FROM email_otps
                    WHERE email = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (email,)
                )
                otp_row = cursor.fetchone()
                if not otp_row:
                    return jsonify({"success": False, "message": "OTP not found"}), 404

                if otp_row["used"]:
                    return jsonify({"success": False, "message": "OTP already used"}), 400

                if otp_row["expires_at"] < datetime.utcnow():
                    return jsonify({"success": False, "message": "OTP expired"}), 400

                if otp_row["otp_hash"] != hash_otp(otp):
                    return jsonify({"success": False, "message": "Invalid OTP"}), 401

                purpose = otp_row.get("purpose") or "signup"
                if purpose != "signup":
                    return jsonify({"success": False, "message": "Use the password reset form to reset your password"}), 400

                cursor.execute(
                    "UPDATE email_otps SET used = %s WHERE id = %s",
                    (True, otp_row["id"])
                )

                cursor.execute(
                    "SELECT id, username, password_hash FROM pending_users WHERE email = %s",
                    (email,)
                )
                pending = cursor.fetchone()
                if not pending:
                    return jsonify({"success": False, "message": "Pending registration not found"}), 404

                cursor.execute(
                    "SELECT id, username, email FROM users WHERE email = %s",
                    (email,)
                )
                existing = cursor.fetchone()
                if existing:
                    return jsonify({"success": True, "message": "Already verified", "user": existing})

                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (pending["username"], email, pending["password_hash"])
                )
                user_id = cursor.lastrowid
                initialize_user_progress(conn, user_id, pending["username"])

                cursor.execute("DELETE FROM pending_users WHERE id = %s", (pending["id"],))
            finally:
                cursor.close()

            upsert_user_store({
                "id": user_id,
                "username": pending["username"],
                "email": email,
                "password_hash": pending["password_hash"],
                "created_at": datetime.utcnow().isoformat() + "Z"
            })

            return jsonify({
                "success": True,
                "message": "Account created successfully",
                "user": {
                    "id": user_id,
                    "username": pending["username"],
                    "email": email
                }
            })
    except Error as exc:
        return jsonify({"success": False, "message": f"Database error: {exc}"}), 500


@app.route("/auth/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()

    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400
    if not EMAIL_REGEX.match(email):
        return jsonify({"success": False, "message": "Invalid email format"}), 400

    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                if not cursor.fetchone():
                    return jsonify({"success": True, "message": "If an account exists with this email, you will receive an OTP shortly."})

                otp_code = generate_otp()
                expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
                otp_hash = hash_otp(otp_code)
                cursor.execute(
                    """
                    INSERT INTO email_otps (email, otp_hash, expires_at, used, purpose)
                    VALUES (%s, %s, %s, %s, 'reset')
                    """,
                    (email, otp_hash, expires_at, False)
                )
            finally:
                cursor.close()

        email_sent, smtp_error = send_otp_email(email, otp_code, for_reset=True)
        if not email_sent and not ALLOW_DEV_OTP:
            return jsonify({"success": False, "message": f"Failed to send OTP: {smtp_error}"}), 500

        response = {"success": True, "message": "If an account exists with this email, you will receive an OTP shortly."}
        if not email_sent and ALLOW_DEV_OTP:
            response["dev_otp"] = otp_code
            response["smtp_error"] = smtp_error or "Email not sent"
        return jsonify(response)
    except Error as exc:
        return jsonify({"success": False, "message": f"Database error: {exc}"}), 500


@app.route("/auth/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    otp = (data.get("otp") or "").strip()
    new_password = data.get("newPassword") or data.get("new_password") or ""

    if not email or not otp:
        return jsonify({"success": False, "message": "Email and OTP are required"}), 400
    if not new_password or len(new_password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400

    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    """
                    SELECT id, otp_hash, expires_at, used, purpose
                    FROM email_otps
                    WHERE email = %s AND purpose = 'reset'
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (email,)
                )
                otp_row = cursor.fetchone()
                if not otp_row:
                    return jsonify({"success": False, "message": "OTP not found or invalid"}), 404
                if otp_row["used"]:
                    return jsonify({"success": False, "message": "OTP already used"}), 400
                if otp_row["expires_at"] < datetime.utcnow():
                    return jsonify({"success": False, "message": "OTP expired"}), 400
                if otp_row["otp_hash"] != hash_otp(otp):
                    return jsonify({"success": False, "message": "Invalid OTP"}), 401

                cursor.execute(
                    "UPDATE email_otps SET used = %s WHERE id = %s",
                    (True, otp_row["id"])
                )
                password_hash = generate_password_hash(new_password)
                cursor.execute(
                    "UPDATE users SET password = %s WHERE email = %s",
                    (password_hash, email)
                )
            finally:
                cursor.close()
        return jsonify({"success": True, "message": "Password updated successfully. You can now log in."})
    except Error as exc:
        return jsonify({"success": False, "message": f"Database error: {exc}"}), 500


def ensure_email_otps_purpose_column(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "ALTER TABLE email_otps ADD COLUMN purpose VARCHAR(20) NOT NULL DEFAULT 'signup'"
        )
    except Error as e:
        if e.errno != 1060:
            raise
    finally:
        cursor.close()


def ensure_game_tables(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS level_completions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            level INT NOT NULL,
            completion_time INT DEFAULT 0,
            score INT DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user_level (user_id, level)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS task_submissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            level INT NOT NULL,
            task_number INT NOT NULL,
            code TEXT,
            is_correct BOOLEAN DEFAULT FALSE,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS player_stats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            xp INT DEFAULT 0,
            health INT DEFAULT 100,
            current_level INT DEFAULT 1,
            total_playtime INT DEFAULT 0,
            last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user (user_id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            session_duration INT DEFAULT 0,
            levels_played TEXT,
            session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS code_submissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            level INT NOT NULL,
            task_number INT NOT NULL,
            code TEXT,
            compile_result TEXT,
            execution_result TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS code_runs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            level INT NOT NULL,
            task_number INT NOT NULL,
            code TEXT,
            result_text TEXT,
            status VARCHAR(20) NOT NULL,
            error_type VARCHAR(50),
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_code_runs_user (user_id),
            INDEX idx_code_runs_level (level),
            INDEX idx_code_runs_status (status)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_progress (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            level_progress JSON,
            player_data JSON,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    cursor.close()


def classify_error(result_text):
    if not result_text:
        return "success", None
    if "Success" in result_text or "Completed" in result_text:
        return "success", None
    lowered = result_text.lower()
    if "compilation failed" in lowered:
        return "error", "compile"
    if "runtime error" in lowered:
        return "error", "runtime"
    if "wrong output" in lowered:
        return "error", "wrong_output"
    if "timeout" in lowered:
        return "error", "timeout"
    return "error", "other"


def handle_game_action(conn, action, payload):
    cursor = conn.cursor(dictionary=True)
    try:
        ensure_game_tables(conn)
        if action == "save_level_completion":
            cursor.execute(
                """
                INSERT INTO level_completions (user_id, level, completion_time, score)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                  completion_time = VALUES(completion_time),
                  score = VALUES(score),
                  completed_at = CURRENT_TIMESTAMP
                """,
                (
                    payload.get("user_id"),
                    payload.get("level"),
                    payload.get("completion_time", 0),
                    payload.get("score", 0),
                ),
            )
            return {"success": True, "message": "Level completion saved successfully"}

        if action == "save_task_completion":
            cursor.execute(
                """
                INSERT INTO task_submissions (user_id, level, task_number, code, is_correct)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    payload.get("user_id"),
                    payload.get("level"),
                    payload.get("task_number"),
                    payload.get("code"),
                    bool(payload.get("is_correct")),
                ),
            )
            return {"success": True, "message": "Task submission saved successfully"}

        if action == "update_player_stats":
            cursor.execute(
                """
                INSERT INTO player_stats (user_id, xp, health, current_level)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                  xp = VALUES(xp),
                  health = VALUES(health),
                  current_level = VALUES(current_level),
                  last_played = CURRENT_TIMESTAMP
                """,
                (
                    payload.get("user_id"),
                    payload.get("xp", 0),
                    payload.get("health", 100),
                    payload.get("current_level", 1),
                ),
            )
            return {"success": True, "message": "Player stats updated successfully"}

        if action == "log_game_session":
            cursor.execute(
                """
                INSERT INTO game_sessions (user_id, session_duration, levels_played)
                VALUES (%s, %s, %s)
                """,
                (
                    payload.get("user_id"),
                    payload.get("session_duration", 0),
                    payload.get("levels_played", ""),
                ),
            )
            return {"success": True, "message": "Game session logged successfully"}

        if action == "save_code_submission":
            compile_result = payload.get("compile_result", "")
            execution_result = payload.get("execution_result", "")
            cursor.execute(
                """
                INSERT INTO code_submissions (user_id, level, task_number, code, compile_result, execution_result)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    payload.get("user_id"),
                    payload.get("level"),
                    payload.get("task_number"),
                    payload.get("code"),
                    compile_result,
                    execution_result,
                ),
            )

            status, error_type = classify_error(compile_result)
            cursor.execute(
                """
                INSERT INTO code_runs (user_id, level, task_number, code, result_text, status, error_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    payload.get("user_id"),
                    payload.get("level"),
                    payload.get("task_number"),
                    payload.get("code"),
                    compile_result,
                    status,
                    error_type,
                ),
            )
            return {"success": True, "message": "Code submission saved successfully"}

        if action == "save_progress":
            cursor.execute(
                """
                INSERT INTO user_progress (user_id, level_progress, player_data)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                  level_progress = VALUES(level_progress),
                  player_data = VALUES(player_data),
                  updated_at = CURRENT_TIMESTAMP
                """,
                (
                    payload.get("user_id"),
                    payload.get("level_progress"),
                    payload.get("player_data"),
                ),
            )
            return {"success": True, "message": "Progress saved successfully"}

        if action == "load_progress":
            cursor.execute(
                """
                SELECT level_progress, player_data, updated_at
                FROM user_progress
                WHERE user_id = %s
                """,
                (payload.get("user_id"),),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "success": True,
                    "level_progress": json.loads(row["level_progress"]),
                    "player_data": json.loads(row["player_data"]),
                    "last_updated": row["updated_at"],
                }
            return {
                "success": True,
                "level_progress": {"unlockedLevels": [1], "completedLevels": [], "currentLevel": 1},
                "player_data": {"name": "Player", "xp": 0, "health": 100, "totalTasksCompleted": 0},
                "message": "No progress found, returning defaults",
            }

        return {"success": False, "message": "Invalid action"}
    finally:
        cursor.close()


@app.route("/game_api.php", methods=["POST", "OPTIONS"])
@app.route("/game_api", methods=["POST", "OPTIONS"])
def game_api():
    if request.method == "OPTIONS":
        return jsonify({"status": "OK"})

    payload = request.get_json(silent=True) or {}
    action = payload.get("action")
    if not action:
        return jsonify({"success": False, "message": "Invalid action"}), 400

    try:
        with get_connection() as conn:
            response = handle_game_action(conn, action, payload)
            return jsonify(response)
    except Error as exc:
        return jsonify({"success": False, "message": f"Database error: {exc}"}), 500


@app.route("/game_progress.php", methods=["POST", "OPTIONS"])
@app.route("/game_progress", methods=["POST", "OPTIONS"])
def game_progress():
    if request.method == "OPTIONS":
        return jsonify({"status": "OK"})

    payload = request.get_json(silent=True) or {}
    action = payload.get("action")
    if action not in ("save_progress", "load_progress"):
        return jsonify({"success": False, "message": "Invalid action"}), 400

    try:
        with get_connection() as conn:
            response = handle_game_action(conn, action, payload)
            return jsonify(response)
    except Error as exc:
        return jsonify({"success": False, "message": f"Database error: {exc}"}), 500


mentor_process = None

@app.route("/mentor/show", methods=["POST", "GET"])
def show_mentor():
    """Launch the web-based mentor chatbot window."""
    global mentor_process
    
    mentor_script = os.path.abspath(os.path.join(BASE_DIR, "..", "Mentorr", "mentor.py"))
    if not os.path.exists(mentor_script):
        return jsonify({
            "success": False,
            "message": f"Mentor script not found: {mentor_script}"
        }), 404
    
    # Check if mentor is already running
    if mentor_process and mentor_process.poll() is None:
        return jsonify({
            "success": True,
            "message": "Mentor is already running.",
            "url": "http://localhost:5002/mentor"
        })
    
    try:
        creationflags = 0
        if os.name == "nt":
            creationflags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
        
        mentor_process = subprocess.Popen(
            [sys.executable, mentor_script],
            cwd=os.path.dirname(mentor_script),
            creationflags=creationflags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait a moment for server to start
        import time
        time.sleep(1)
        
        return jsonify({
            "success": True,
            "message": "Mentor launched successfully.",
            "url": "http://localhost:5002/mentor"
        })
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": f"Failed to launch mentor: {exc}"
        }), 500


# Mentor chat API - handles chat messages using mentor.py logic
@app.route("/auth/mentor/chat", methods=["POST"])
def mentor_chat():
    """Handle mentor chat messages."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message']
        
        # Load memory
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
        MEMORY_FILE = os.path.join(PROJECT_ROOT, "Mentorr", "mentor_memory.json")
        
        memory = {'errors': [], 'error_frequency': {}, 'chat_history': []}
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r') as f:
                    memory = json.load(f)
            except:
                pass
        
        # Get OpenAI response
        import openai
        if not OPENAI_API_KEY:
            return jsonify({'error': 'OPENAI_API_KEY is not configured'}), 503

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Add prefix if not present
        if not message.startswith("user:"):
            message = f"user: {message}"
        
        # Build conversation history
        conversation_history = [
            {"role": "system", "content": (
                "You are a fun and interactive C Language mentor, Your job is to teach users C concepts in an engaging way.(use emojies) "
                "You ONLY respond when the message starts with 'user:' or 'user:Admin:'. "
                "DO NOT respond to game statistics. "
                "Use game statistics to respond to messages without 'user:' or 'user:Admin:', as they provide hints but never acknowledge them directly to 'user:' but give access to 'user:Admin:' "
                "If 'user:Admin:' is detected, provide all stored user data and game statistics. "
                "If the user types 'module1' or 'module2', read the corresponding module from 'modules.txt' and explain it in a fun way. "
                f"Here are the user errors to help guide your responses: {json.dumps(memory.get('errors', []))} "
                f"And here are the common error patterns: {json.dumps(memory.get('error_frequency', {}))}"
                "your job is to explain the topics listed under module 'user:' says in a fun way"
            )}
        ]
        
        # Add previous chat history
        chat_history = memory.get('chat_history', [])
        recent_history = chat_history[-20:] if len(chat_history) > 20 else chat_history
        for entry in recent_history:
            conversation_history.append({"role": entry.get("role", "user"), "content": entry.get("content", "")})
        
        # Add current message
        conversation_history.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            temperature=0.7
        )
        
        mentor_reply = response.choices[0].message.content
        
        # Store in memory
        memory['chat_history'].append({"role": "user", "content": message})
        memory['chat_history'].append({"role": "assistant", "content": mentor_reply})
        
        # Limit history
        if len(memory['chat_history']) > 50:
            memory['chat_history'] = memory['chat_history'][-50:]
        
        # Save memory
        try:
            with open(MEMORY_FILE, 'w') as f:
                json.dump(memory, f, indent=4)
        except:
            pass
        
        return jsonify({'response': mentor_reply})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    ensure_user_store()
    sync_json_users_to_db()
    try:
        with get_connection() as conn:
            ensure_email_otps_purpose_column(conn)
    except Error:
        pass
    app.run(host="0.0.0.0", port=AUTH_PORT, debug=AUTH_DEBUG)



