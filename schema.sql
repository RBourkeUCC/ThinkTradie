-- ############################################################################
-- # THINKTRADIE SCHEMA INITIALIZATION - ITERATION 4
-- # SOURCE: Flask Tutorial – Database Schema
-- # https://flask.palletsprojects.com/en/stable/tutorial/database/
-- # WHY: Keeping the schema in a separate SQL file allows for clean, 
-- # declarative table evolution across iterations.
-- ############################################################################

-- -----------------------------------------------------------------------------
-- Inventory Management (Iteration 1)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    qty INTEGER NOT NULL,
    threshold INTEGER NOT NULL
);

-- -----------------------------------------------------------------------------
-- Document Capture & Vault (Iteration 2 → Iteration 4)
-- ############################################################################
-- # SOURCE: Flask Documentation – Uploading Files
-- # https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
-- # TECHNIQUE: Metadata-only storage. Actual binary files are stored on disk 
-- # while SQLite maintains the relational pointers and display_name metadata.
-- ############################################################################
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    display_name TEXT,              -- Iteration 4: Support for user-defined names
    stored_path TEXT NOT NULL,
    uploaded_at TEXT NOT NULL       -- ISO 8601 UTC timestamp
);

-- -----------------------------------------------------------------------------
-- Task Manager & Daily Schedule (Iteration 2 → Iteration 3)
-- ############################################################################
-- # SOURCE: SQLite Boolean Handling & ISO 8601 Date Functions
-- # https://sqlite.org/datatype3.html
-- # https://sqlite.org/lang_datefunc.html
-- # WHY: SQLite lacks native BOOLEAN/DATE types; using INTEGER (0/1) and 
-- # TEXT (YYYY-MM-DD) enables robust filtering for the Daily Task view (US7).
-- ############################################################################
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    notes TEXT,
    is_done INTEGER NOT NULL DEFAULT 0,  -- 0 = open, 1 = completed
    created_at TEXT NOT NULL,            -- ISO 8601 UTC timestamp
    completed_at TEXT,                   -- NULL until toggled
    due_date TEXT                        -- ISO 8601 date (YYYY-MM-DD)
);

-- -----------------------------------------------------------------------------
-- Authentication & User Profiles (Iteration 4)
-- ############################################################################
-- # SOURCE: SQLite UNIQUE Constraint & CREATE TABLE Syntax
-- # https://sqlite.org/lang_createtable.html
-- # WHY: email must be UNIQUE to prevent duplicate account registration.
-- # NOTE: password_hash stores the PBKDF2 string, NEVER plaintext.
-- ############################################################################
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,       -- Iteration 4: Profile branding support
    last_name TEXT NOT NULL,        -- Iteration 4: Profile branding support
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL        -- Account creation timestamp
);