# TradieFlow · Iteration 5
**Version: 5 (Iteration 5)** **Date: 19 February 2026**

**TradieFlow** is a lightweight, mobile-first productivity tool designed for sole traders and small crews to manage materials, tasks, and documentation without unnecessary admin. Iteration 5 marks the evolution from a functional MVP into a **Live Progressive Web App (PWA)**, transitioning the "Premium UI" into a production-ready cloud environment on Render.

## Project Roadmap
* **Iteration 1-3:** Core Inventory, Document Capture, and Task Manager development.
* **Iteration 4:** High-level UI refurbishment, TradieFlow branding, and secure user authentication.
* **Iteration 5:** Cloud deployment (Render), PWA manifest implementation, and Service Worker architecture for offline resilience.

---

## Features (Iteration 5 Advancements)

### User Authentication & Cloud Access
* **Secure Cloud Hosting:** Application now live on Render with full HTTPS encryption, mandatory for secure PWA standards.
* **Mandatory Sign-In:** Application-wide privacy enforced via `@login_required` decorators; all core routes are locked by default.
* **Gunicorn Production Server:** Transitioned to Gunicorn to handle concurrent mobile traffic with high stability.

### Premium Dashboard & PWA Integration
* **Standalone Mobile Experience:** Custom `manifest.json` allows TradieFlow to be "Installed" on iOS home screens, providing a native app interface without browser bars.
* **Bento Grid Layout:** Maintained organized data visualization inspired by bank-grade SaaS for high-level oversight.
* **Service Worker (sw.js):** Implemented at the root level to intercept requests and provide "Cache-First" logic, ensuring the dashboard loads in low-signal environments.
* **Aesthetic:** Responsive dark-mode palette (#0e0f11) with neon-lime (#ccff00) accents.

### Document Vault (Extended)
* **Metadata Management:** Renaming functionality allows users to assign meaningful labels to stored files.
* **Offline Access:** Service Worker ensures the Vault interface is accessible even when the device is in Airplane Mode.

---

## Technical References & Research Sources

### PWA & Offline Standards
* **MDN Web Docs: Service Worker API** (Lifecycle & Fetch Interception)
* **W3C Web App Manifest** (Standalone Display & Icons)
* **Google web.dev: Offline-First Foundations**

### UI / UX & Security
* **Pixel Rocket Global Bank Template** (Design Foundation)
* **Werkzeug Security Helpers** (PBKDF2 Password Hashing)
* **Flask Session Management**

---

## Technical Diagnosis (Iteration 5)

| Element | Status | Diagnosis |
| :--- | :--- | :--- |
| **PWA Scope** | Resolved | SW moved to root directory to ensure full control over homepage and authentication routes. |
| **Deployment** | Active | Connected to Render via GitHub Private Repo for continuous deployment. |
| **Data Storage** | Ephemeral | SQLite is currently stored on temporary disk; migration to PostgreSQL recommended for permanent data. |

---

## Quick Start
```bash
# Live Production URL
[https://thinktradie.onrender.com](https://thinktradie.onrender.com)

# Local Setup
git clone [https://github.com/RBourkeUCC/ThinkTradie.git](https://github.com/RBourkeUCC/ThinkTradie.git)
pip install -r requirements.txt
python app.py
