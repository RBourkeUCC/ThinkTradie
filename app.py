import os
import sqlite3
from datetime import datetime, timezone
from flask import (
    Flask, render_template, request, redirect, 
    url_for, abort, flash, send_from_directory, session
)
from functools import wraps

###############################################################################
# SOURCE: Flask Documentation – File Uploads Pattern
# https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
# WHY: secure_filename is essential to sanitize user-provided filenames, 
# preventing path traversal attacks and ensuring filesystem compatibility.
###############################################################################
from werkzeug.utils import secure_filename

###############################################################################
# SOURCE: Werkzeug security helpers (Password Hashing)
# https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security
# WHY: PBKDF2 hashing is used to store irreversible representations of 
# passwords, protecting user credentials even if the database is compromised.
###############################################################################
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

###############################################################################
# SOURCE: Pixel Rocket – Global Bank Next.js Website Template (UI Inspiration)
# https://pixelrocket.store/free-templates/nextjs-templates/global-bank-nextjs-website-template
# WHY: This template provides the high-end, dark-mode aesthetic foundation for 
# the ThinkTradie Iteration 4 refurbishment.
###############################################################################

###############################################################################
# SOURCE: Flask configuration guidance (SECRET_KEY)
# https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY
# WHY: Cryptographically signs session cookies. Without this, users could 
# manipulate their session data to bypass authentication.
###############################################################################
app.secret_key = "dev"

DB_PATH = os.path.join(app.root_path, "app.db")
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------------------------------------------------------
# Custom Jinja Filters
# -----------------------------------------------------------------------------
###############################################################################
# SOURCE: Jinja2 API – Custom Filters
# https://jinja.palletsprojects.com/en/stable/api/#custom-filters
# WHY: To transform raw ISO timestamps into the dd/mm/yyyy format required 
# for professional trade reporting in Iteration 4.
###############################################################################
@app.template_filter("human_time")
def human_time(value: str) -> str:
    if not value: return ""
    clean = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(clean)
    return dt.strftime("%d/%m/%Y")

@app.template_filter("human_time_dmy")
def human_time_dmy(value: str) -> str:
    if not value: return ""
    clean = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(clean)
    return dt.strftime("%d/%m/%Y %H:%M")

@app.template_filter("date_dmy")
def date_dmy(value: str) -> str:
    if not value: return ""
    try:
        dt = datetime.fromisoformat(value)
    except ValueError: return value
    return dt.strftime("%d/%m/%Y")

# -----------------------------------------------------------------------------
# Database Helpers & Migrations
# -----------------------------------------------------------------------------
def get_db():
    ###########################################################################
    # SOURCE: Python sqlite3 documentation - sqlite3.Row
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.Row
    # WHY: Maps column names to dictionary keys, allowing row['column_name'] 
    # syntax which improves code readability and maintenance.
    ###########################################################################
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # SOURCE: Flask Tutorial – Initialize the Database
    # https://flask.palletsprojects.com/en/stable/tutorial/database/#initialize-the-database-file
    schema_path = os.path.join(app.root_path, "schema.sql")
    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = f.read()
        conn = get_db()
        conn.executescript(schema)
        conn.commit()

init_db()

def ensure_columns():
    ###########################################################################
    # SOURCE: SQLite PRAGMA table_info & ALTER TABLE
    # https://sqlite.org/pragma.html#pragma_table_info
    # WHY: Ensures existing databases are non-destructively updated to include 
    # Iteration 4 fields like first_name and display_name.
    ###########################################################################
    conn = get_db()
    if "due_date" not in {c[1] for c in conn.execute("PRAGMA table_info(tasks)")}:
        conn.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")
    cols = {c[1] for c in conn.execute("PRAGMA table_info(users)")}
    if "first_name" not in cols: conn.execute("ALTER TABLE users ADD COLUMN first_name TEXT")
    if "last_name" not in cols: conn.execute("ALTER TABLE users ADD COLUMN last_name TEXT")
    if "display_name" not in {c[1] for c in conn.execute("PRAGMA table_info(documents)")}:
        conn.execute("ALTER TABLE documents ADD COLUMN display_name TEXT")
    conn.commit()

ensure_columns()

# -----------------------------------------------------------------------------
# Access Control (The Gatekeeper)
# -----------------------------------------------------------------------------
def get_current_user():
    user_id = session.get("user_id")
    if not user_id: return None
    return get_db().execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()

###############################################################################
# SOURCE: Flask View Decorator Pattern
# https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/
# WHY: This is the security core. It intercepts requests; if 'user_id' is 
# absent from the session, it blocks the view and forces a redirect to signin.
###############################################################################
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("signin"))
        return view(*args, **kwargs)
    return wrapped

@app.context_processor
def inject_user():
    return {"current_user": get_current_user()}

# -----------------------------------------------------------------------------
# Authentication Routes (Public Access)
# -----------------------------------------------------------------------------
@app.route("/signin", methods=["GET", "POST"])
def signin():
    # SOURCE: Flask Sessions (Signed Cookies)
    # https://flask.palletsprojects.com/en/stable/quickstart/#sessions
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = get_db().execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("home"))
        flash("Invalid email or password.", "error")
    return render_template("signin.html", title="ThinkTradie | Sign In", mode="signin")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        fn, ln = (request.form.get("first_name") or "").strip(), (request.form.get("last_name") or "").strip()
        if not fn or len(password) < 8:
            flash("Invalid registration details.", "error")
            return redirect(url_for("signup"))
        pwd_hash = generate_password_hash(password, method="pbkdf2:sha256")
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        try:
            conn = get_db()
            conn.execute("INSERT INTO users(first_name, last_name, email, password_hash, created_at) VALUES(?,?,?,?,?)",
                         (fn, ln, email, pwd_hash, ts))
            conn.commit()
            return redirect(url_for("signin"))
        except sqlite3.IntegrityError: flash("Email already exists.", "error")
    return render_template("signin.html", title="ThinkTradie | Join Pro", mode="signup")

@app.post("/signout")
def signout():
    session.clear()
    return redirect(url_for("signin"))

# -----------------------------------------------------------------------------
# Protected Dashboard Routes (Authentication Required)
# -----------------------------------------------------------------------------
@app.get("/")
def root(): return redirect(url_for("home"))

@app.get("/home")
@login_required
def home():
    today_iso = datetime.now(timezone.utc).date().isoformat()
    today_tasks = get_db().execute("SELECT * FROM tasks WHERE is_done=0 AND due_date=?", (today_iso,)).fetchall()
    return render_template("home.html", title="ThinkTradie | Dashboard", today_tasks=today_tasks, today_iso=today_iso)

@app.get("/profile")
@login_required
def profile(): return render_template("profile.html", title="ThinkTradie | Profile")

@app.route("/inventory", methods=["GET", "POST"])
@login_required
def index():
    conn = get_db()
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        qty, thr = int(request.form.get("qty") or 0), int(request.form.get("threshold") or 0)
        conn.execute("INSERT INTO inventory(name, qty, threshold) VALUES(?,?,?)", (name, qty, thr))
        conn.commit()
        return redirect(url_for("index"))
    only_low = request.args.get("filter") == "low"
    q = "SELECT * FROM inventory ORDER BY name COLLATE NOCASE"
    if only_low: q = "SELECT * FROM inventory WHERE qty <= threshold ORDER BY name COLLATE NOCASE"
    return render_template("index.html", items=conn.execute(q).fetchall(), only_low=only_low, title="ThinkTradie | Inventory")

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit(item_id):
    conn = get_db()
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        qty, thr = int(request.form.get("qty") or 0), int(request.form.get("threshold") or 0)
        conn.execute("UPDATE inventory SET name=?, qty=?, threshold=? WHERE id=?", (name, qty, thr, item_id))
        conn.commit()
        return redirect(url_for("index"))
    item = conn.execute("SELECT * FROM inventory WHERE id=?", (item_id,)).fetchone()
    if not item: abort(404)
    return render_template("edit.html", item=item, title="ThinkTradie | Edit")

@app.post("/delete/<int:item_id>")
@login_required
def delete(item_id):
    conn = get_db(); conn.execute("DELETE FROM inventory WHERE id=?", (item_id,)); conn.commit()
    return redirect(url_for("index"))

@app.route("/documents", methods=["GET", "POST"])
@login_required
def documents():
    conn = get_db()
    if request.method == "POST":
        file = request.files.get("file")
        if file and ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            fn = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], fn))
            ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
            conn.execute("INSERT INTO documents (filename, display_name, stored_path, uploaded_at) VALUES (?,?,?,?)",
                         (fn, os.path.splitext(fn)[0], os.path.join("uploads", fn), ts))
            conn.commit()
        return redirect(url_for("documents"))
    return render_template("documents.html", documents=conn.execute("SELECT * FROM documents ORDER BY uploaded_at DESC").fetchall(), title="ThinkTradie | Capture")

@app.get("/vault")
@login_required
def vault():
    return render_template("vault.html", documents=get_db().execute("SELECT * FROM documents ORDER BY uploaded_at DESC").fetchall(), title="ThinkTradie | Vault")

@app.get("/vault/view/<int:doc_id>")
@login_required
def vault_view(doc_id):
    # SOURCE: Flask API – send_from_directory
    # https://flask.palletsprojects.com/en/stable/api/#flask.send_from_directory
    doc = get_db().execute("SELECT stored_path FROM documents WHERE id=?", (doc_id,)).fetchone()
    if not doc: abort(404)
    return send_from_directory(os.path.join(app.root_path, os.path.dirname(doc["stored_path"])), os.path.basename(doc["stored_path"]))

@app.post("/vault/delete/<int:doc_id>")
@login_required
def vault_delete(doc_id):
    conn = get_db(); doc = conn.execute("SELECT * FROM documents WHERE id=?", (doc_id,)).fetchone()
    if doc:
        conn.execute("DELETE FROM documents WHERE id=?", (doc_id,)); conn.commit()
        p = os.path.join(app.root_path, doc["stored_path"])
        if os.path.exists(p): os.remove(p)
    return redirect(url_for("vault"))

@app.post("/vault/rename/<int:doc_id>")
@login_required
def vault_rename(doc_id):
    # SOURCE: MDN – HTTP Methods (POST for updates)
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    n = (request.form.get("display_name") or "").strip()
    if n: conn = get_db(); conn.execute("UPDATE documents SET display_name=? WHERE id=?", (n, doc_id)); conn.commit()
    return redirect(url_for("vault"))

@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    conn = get_db()
    if request.method == "POST":
        t, n, d = (request.form.get("title") or "").strip(), request.form.get("notes"), request.form.get("due_date")
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        conn.execute("INSERT INTO tasks (title, notes, created_at, due_date) VALUES (?,?,?,?)", (t, n, ts, d))
        conn.commit(); return redirect(url_for("tasks"))
    o = conn.execute("SELECT * FROM tasks WHERE is_done=0 ORDER BY created_at DESC").fetchall()
    c = conn.execute("SELECT * FROM tasks WHERE is_done=1 ORDER BY completed_at DESC").fetchall()
    return render_template("tasks.html", open_tasks=o, completed_tasks=c, title="ThinkTradie | Tasks")

@app.post("/tasks/<int:task_id>/toggle")
@login_required
def toggle_task(task_id):
    # SOURCE: SQLite Datatypes (Handling Booleans as Integers 0/1)
    # https://sqlite.org/datatype3.html#boolean_datatype
    conn = get_db(); r = conn.execute("SELECT is_done FROM tasks WHERE id=?", (task_id,)).fetchone()
    if r:
        nv = 0 if r["is_done"] else 1
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds") if nv else None
        conn.execute("UPDATE tasks SET is_done=?, completed_at=? WHERE id=?", (nv, ts, task_id)); conn.commit()
    return redirect(url_for("tasks"))

@app.post("/tasks/<int:task_id>/delete")
@login_required
def delete_task(task_id):
    conn = get_db(); conn.execute("DELETE FROM tasks WHERE id=?", (task_id,)); conn.commit()
    return redirect(url_for("tasks"))

from flask import send_from_directory

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('static', 'sw.js')

if __name__ == "__main__":
    # Runs on port 5001 for Iteration 4 compatibility
    app.run(debug=True, host="0.0.0.0", port=5001)
