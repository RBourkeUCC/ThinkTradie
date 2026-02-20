# ThinkTradie · Iteration 5
**Version: 5 (Iteration 5)** **Date: 20 February 2026**

**ThinkTradie** has evolved from a local prototype into a **cloud-deployed Progressive Web App (PWA)**. Iteration 5 focused on the migration from a local development environment to **Termux** and production hosting on **Render**.

## Project Roadmap
* **Iteration 1-3:** Core module development (Inventory, Task Manager, Document Vault).
* **Iteration 4:** UI refurbishment, branding, and secure user authentication.
* **Iteration 5:** Mobile-native migration (Termux), GitHub integration, Render Cloud Deployment, and installable PWA experience.

---

## Features (Iteration 5 Advancements)

### Cloud Migration & Production
* **Mobile-Native Development:** Fully migrated to **Termux** to enable Linux-based operations on a mobile device.
* **Automated Deployment:** Connected GitHub to **Render** for a "Push-to-Deploy" workflow.
* **Gunicorn Integration:** Implemented the **Gunicorn WSGI server** to manage production-level concurrency and stability.

### PWA Implementation
* **Web App Manifest:** Configured `manifest.json` with high-resolution icons (192px and 512px), theme colour, and standalone display mode to enable "Add to Home Screen" on both Android and iPhone.
* **Service Worker:** Implemented a root-level `sw.js` with a fetch event handler, required by Chrome to recognise the site as an installable PWA rather than offering a simple bookmark.
* **Note:** The Service Worker currently handles fetch events for installability. Offline page caching is not yet implemented and is a future consideration.

---

## Technical References & Online Sources

### Web App Manifest (PWA)
* **W3C Web App Manifest Specification** Source: [https://www.w3.org/TR/appmanifest/](https://www.w3.org/TR/appmanifest/)
* **MDN: Making PWAs Installable** Source: [https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable)
* **MDN: Web App Manifests** Source: [https://developer.mozilla.org/en-US/docs/Web/Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)

### Service Worker
* **MDN Web Docs: Service Worker API** Source: [https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
* **Google web.dev: Service Worker Lifecycle** Source: [https://web.dev/articles/service-worker-lifecycle](https://web.dev/articles/service-worker-lifecycle)

### Gunicorn & Deployment
* **Gunicorn – Python WSGI HTTP Server for UNIX** Source: [https://gunicorn.org/](https://gunicorn.org/)
* **Render: Deploy a Flask App** Source: [https://render.com/docs/deploy-flask](https://render.com/docs/deploy-flask)
* **Termux Wiki** Source: [https://wiki.termux.com/wiki/Main_Page](https://wiki.termux.com/wiki/Main_Page)
* **Flask Documentation – Deployment Options** Source: [https://flask.palletsprojects.com/en/stable/deploying/](https://flask.palletsprojects.com/en/stable/deploying/)

---

## Technical Diagnosis (Iteration 5)

| Element | Status | Diagnosis |
| :--- | :--- | :--- |
| **PWA Scope** | Resolved | Moved `sw.js` to the root directory to allow global scope interception. |
| **Server Logic** | Active | Transitioned from Flask's built-in server to Gunicorn for production stability. |
| **Data Persistence** | Warning | Current SQLite storage is ephemeral on Render; migration to PostgreSQL is a future consideration. |
| **Offline Access** | Not Available | SW handles fetch events for installability; offline page caching is not yet implemented. |

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
