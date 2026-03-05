# ThinkTradie

**Version:** Final (Iteration 6) · **Date:** 05 March 2026

ThinkTradie is a mobile-first productivity app built for sole traders and small crews who need a simple way to manage their inventory, tasks, and paperwork without the overhead of expensive software. It runs as a Progressive Web App (PWA), meaning it can be installed directly onto a phone's home screen and used like a native app — no app store required.

The app is live at **https://thinktradie.onrender.com** and works on Android, iPhone, and desktop.

---

## What It Does

ThinkTradie is built around four core modules:

* **Inventory Manager:** Add, edit, and delete stock items. Each item tracks a quantity and a low-stock threshold so you know when something needs reordering.
* **Task Manager:** Create tasks with optional due dates. Tasks due today are pulled onto the home dashboard automatically so you can see what needs doing at a glance.
* **Document Capture:** Take a photo or upload a file directly from your phone. Designed for quickly capturing receipts, delivery dockets, or site photos while on the job.
* **Document Vault:** A central place to store and retrieve important documents like insurance certs, safety statements, or contracts. Documents can be renamed for easy identification and viewed in-app without leaving the PWA.

All data is tied to a personal account with sign-in authentication, so each user only sees their own stuff.

---

## How It Was Built

ThinkTradie was developed across six iterations over the course of the academic year as part of the IS4470 Final Year Project at University College Cork.

### Iteration 1–3: Core Functionality

The first three iterations focused on getting the basics working. I built the four modules one by one — Inventory first, then Tasks and Document Capture, then the Document Vault and the Daily Task Manager. The goal was to have a working prototype with full CRUD (create, read, update, delete) operations for each module. All development was done locally using VS Code on my laptop.

### Iteration 4: Authentication & UI Overhaul

Iteration 4 introduced user accounts with sign-in/sign-out functionality and a complete visual redesign. The app went from a plain Bootstrap layout to a custom dark-themed UI with neon-green accents, rounded cards, and a consistent design language across all pages. Document renaming was also added to the Vault in this iteration. VS Code remained the primary development environment at this stage.

### Iteration 5: Cloud Deployment & PWA

This was the biggest architectural shift. I migrated the development environment from VS Code on my laptop to Termux on my Android phone — a Linux terminal emulator that lets you run a full command-line environment on a mobile device. The purpose of Termux was specifically to bridge the gap from desktop to mobile development and prove that the entire workflow could operate from a phone.

As part of this migration, I set up a Git repository and pushed the codebase to GitHub for the first time. GitHub was needed as the bridge between my development environment and Render, the cloud hosting platform. Once connected, every push to GitHub automatically rebuilds and deploys the app on Render — no manual server management required.

I also configured the PWA infrastructure — a web app manifest with high-resolution icons and a Service Worker — so the app can be installed on both Android and iPhone home screens and launches in standalone mode without browser chrome.

### Iteration 6: Final Polish

The final iteration was about consistency. I audited every page on both mobile and desktop and fixed the issues: dashboard cards that didn't match each other, page headings that said the wrong thing, emoji icons that looked different on every device, a date input that overflowed on mobile, and a dead-end in the document viewer when using the app in PWA mode. All emoji icons were replaced with professional inline SVGs from the Heroicons library, and a new in-app document viewer was built so users aren't stranded when viewing files in standalone mode.

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Language | Python | Straightforward, widely taught, and well-suited for rapid web prototyping. |
| Framework | Flask | Lightweight and flexible. Gives full control without the overhead of a larger framework like Django. |
| Database | SQLite | Zero-configuration, file-based database. Perfect for a single-user prototype with no external dependencies. |
| Server | Gunicorn | Production-grade WSGI server that replaced Flask's built-in dev server for stability and HTTPS support. |
| Hosting | Render (Free Tier) | Cloud platform with GitHub integration for automatic push-to-deploy. Free tier is sufficient for demonstration. |
| Frontend | HTML, Tailwind CSS, Jinja2 | Tailwind provides utility-first styling without writing custom CSS files. Jinja2 handles server-side templating. |
| Icons | Heroicons (Inline SVG) | Open-source, stroke-based SVG icons that render identically on every device and operating system. |
| Dev Environment | VS Code → Termux | VS Code on desktop for Iterations 1–4. Termux on Android from Iteration 5 onward to migrate development to mobile. |
| Version Control | Git + GitHub | Introduced in Iteration 5 to connect the codebase to Render for automated cloud deployment. |

---

## Known Limitations

These are documented honestly rather than hidden:

* **Ephemeral Database:** Render's free tier wipes the filesystem on every deploy or server spin-down, which means the SQLite database resets. User accounts, inventory, tasks, and uploaded documents do not persist permanently. A production version would need PostgreSQL.
* **Ephemeral File Storage:** Uploaded documents are stored on disk and lost when Render's filesystem resets. A production version would need cloud object storage like Cloudinary or AWS S3.
* **No Offline Access:** The Service Worker handles the install prompt but does not cache pages for offline use. The app needs an internet connection to function.
* **Cold Start Delay:** Render's free tier spins down after inactivity. The first request after spin-down takes 30–60 seconds. UptimeRobot is configured to ping the URL periodically to reduce this.

---

## Quick Start

```bash
# Production URL
https://thinktradie.onrender.com

# Local Development (via Termux or PC)
git pull origin main
pip install -r requirements.txt
python app.py

# Production (via Render + Gunicorn)
# Handled automatically by Procfile on git push to main
```

---

## Technical References

All references listed below are explicitly cited in `SOURCE:` comments within the ThinkTradie codebase. They are grouped by category and each entry notes which file(s) reference it.

### Flask & Werkzeug

* Flask Documentation – File Uploads Pattern — https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
  Used in: `app.py`, `schema.sql`, `documents.html`

* Flask Documentation – Rendering Templates — https://flask.palletsprojects.com/en/stable/quickstart/#rendering-templates
  Used in: `app.py`

* Flask Documentation – Configuration (SECRET_KEY) — https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY
  Used in: `app.py`

* Flask Documentation – Sessions (Signed Cookies) — https://flask.palletsprojects.com/en/stable/quickstart/#sessions
  Used in: `app.py`, `profile.html`

* Flask Documentation – View Decorator Pattern — https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/
  Used in: `app.py`

* Flask Tutorial – Initialize the Database — https://flask.palletsprojects.com/en/stable/tutorial/database/
  Used in: `app.py`, `schema.sql`

* Flask Tutorial – Update View — https://flask.palletsprojects.com/en/stable/tutorial/views/#update
  Used in: `edit.html`

* Flask Tutorial – Authentication Blueprints & Views — https://flask.palletsprojects.com/en/stable/tutorial/views/#authentication
  Used in: `signin.html`

* Flask Documentation – Post/Redirect/Get Pattern — https://flask.palletsprojects.com/en/stable/patterns/postredirectget/
  Used in: `signin.html`

* Flask API – send_from_directory — https://flask.palletsprojects.com/en/stable/api/#flask.send_from_directory
  Used in: `app.py`

* Flask Documentation – Deployment Options — https://flask.palletsprojects.com/en/stable/deploying/
  Used in: `Procfile`

* Werkzeug Security Helpers (Password Hashing) — https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security
  Used in: `app.py`

### SQLite & Database

* Python sqlite3 Documentation – sqlite3.Row — https://docs.python.org/3/library/sqlite3.html#sqlite3.Row
  Used in: `app.py`

* SQLite PRAGMA table_info & ALTER TABLE — https://sqlite.org/pragma.html#pragma_table_info
  Used in: `app.py`

* SQLite Datatypes (Boolean Handling) — https://sqlite.org/datatype3.html
  Used in: `app.py`, `schema.sql`

* SQLite Date and Time Functions — https://sqlite.org/lang_datefunc.html
  Used in: `schema.sql`

* SQLite CREATE TABLE Syntax (UNIQUE Constraint) — https://sqlite.org/lang_createtable.html
  Used in: `schema.sql`

### Jinja2 & Templating

* Jinja2 API – Custom Filters — https://jinja.palletsprojects.com/en/stable/api/#custom-filters
  Used in: `app.py`

* Jinja2 – Conditional Rendering — https://jinja.palletsprojects.com/en/stable/templates/#conditionals
  Used in: `vault.html`

### HTML & MDN Web Standards

* MDN: HTTP Methods — https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
  Used in: `app.py`, `profile.html`, `index.html`, `tasks.html`

* MDN: input type="file" (accept attribute) — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#accept
  Used in: `documents.html`

* MDN: HTMLInputElement capture — https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/capture
  Used in: `documents.html`

* MDN: input type="date" — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date
  Used in: `tasks.html`

* MDN: HTML object Element — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/object
  Used in: `vault_viewer.html`

* MDN: HTML Anchor download Attribute — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#download
  Used in: `vault_viewer.html`

* MDN: Window.history API — https://developer.mozilla.org/en-US/docs/Web/API/Window/history
  Used in: `vault.html`

* MDN: Window.history.back() — https://developer.mozilla.org/en-US/docs/Web/API/History/back
  Used in: `vault_viewer.html`

### CSS & Responsive Design

* MDN: CSS Selectors — https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors
  Used in: `styles.css`

* MDN: color-scheme CSS Property — https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme
  Used in: `styles.css`

* MDN: appearance CSS Property — https://developer.mozilla.org/en-US/docs/Web/CSS/appearance
  Used in: `styles.css`

* MDN: object-fit CSS Property — https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit
  Used in: `vault_viewer.html`

* MDN: Responsive Design — https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design
  Used in: `tasks.html`

* MDN: ::-webkit-calendar-picker-indicator — https://developer.mozilla.org/en-US/docs/Web/CSS/::-webkit-calendar-picker-indicator
  Used in: `styles.css`

* CSS-Tricks: Radial Gradients — https://css-tricks.com/almanac/properties/g/gradient/
  Used in: `styles.css`

* CSS-Tricks: Flexbox Truncated Text — https://css-tricks.com/flexbox-truncated-text/
  Used in: `styles.css`, `tasks.html`

* CSS-Tricks: Number Input Spinners — https://css-tricks.com/snippets/css/turn-off-number-input-spinners/
  Used in: `styles.css`

* Tailwind CSS: Animation (Pulse) — https://tailwindcss.com/docs/animation#pulse
  Used in: `index.html`

### SVG & Icons

* MDN: SVG – Scalable Vector Graphics — https://developer.mozilla.org/en-US/docs/Web/SVG
  Used in: `home.html`

* Tailwind Labs: Heroicons — https://heroicons.com/
  Used in: `home.html`, `vault.html`, `vault_viewer.html`

### PWA & Service Worker

* MDN: display-mode CSS Media Feature — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/display-mode
  Used in: `app.py`, `vault_viewer.html`

* MDN: Service Worker API — https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
  Used in: `sw.js`, `base.html`

* MDN: Web App Manifests — https://developer.mozilla.org/en-US/docs/Web/Manifest
  Used in: `manifest.json`, `base.html`

* MDN: Making PWAs Installable — https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable
  Used in: `manifest.json`

* W3C: Web Application Manifest Specification — https://www.w3.org/TR/appmanifest/
  Used in: `manifest.json`

* Google web.dev: Service Worker Lifecycle — https://web.dev/articles/service-worker-lifecycle
  Used in: `sw.js`

### Deployment & Infrastructure

* Gunicorn – Python WSGI HTTP Server — https://gunicorn.org/
  Used in: `Procfile`, `requirements.txt`

* Render: Deploy a Flask App — https://render.com/docs/deploy-flask
  Used in: deployment configuration

* Termux Wiki — https://wiki.termux.com/wiki/Main_Page
  Used in: development environment migration

### UI Design Inspiration

* Pixel Rocket – Global Bank Next.js Template — https://pixelrocket.store/free-templates/nextjs-templates/global-bank-nextjs-website-template
  Used in: `app.py`, `styles.css`

* Google Material Design: Cards Overview — https://m3.material.io/components/cards/overview
  Used in: `home.html`
