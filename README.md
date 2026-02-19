# TradieFlow · Iteration 5
**Version: 5 (Iteration 5)** **Date: 19 February 2026**

**TradieFlow** has evolved from a local prototype into a **cloud-deployed Progressive Web App (PWA)**. Iteration 5 focused on the migration from a local development environment to **Termux** and production hosting on **Render**.

## Project Roadmap
* **Iteration 1-3:** Core module development (Inventory, Task Manager, Document Vault).
* **Iteration 4:** UI refurbishment, branding, and secure user authentication.
* **Iteration 5:** Mobile-native migration (Termux), GitHub integration, and Render Cloud Deployment.

---

## Features (Iteration 5 Advancements)

### Cloud Migration & Production
* **Mobile-Native Development:** Fully migrated to **Termux** to enable Linux-based operations on a mobile device.
* **Automated Deployment:** Connected GitHub to **Render** for a "Push-to-Deploy" workflow.
* **Gunicorn Integration:** Implemented the **Gunicorn WSGI server** to manage production-level concurrency and stability.

### PWA Implementation
* **Web App Manifest:** Configured `manifest.json` to enable a standalone "Add to Home Screen" experience.
* **Service Worker Logic:** Implemented a root-level `sw.js` for request interception and offline caching.
* **Offline Resilience:** Leveraged a "Cache-First" strategy to ensure the application shell loads in Airplane Mode.

---

## Technical References & Online Sources

### Web App Manifest (PWA)
* **W3C Web App Manifest Specification** Source: [https://www.w3.org/TR/appmanifest/](https://www.w3.org/TR/appmanifest/)
* **MDN: Add to Home Screen** Source: [https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Installability](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Installability)

### Service Worker (Offline Capabilities)
* **MDN Web Docs: Service Worker API** Source: [https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
* **Google web.dev: Service Worker Lifecycle** Source: [https://web.dev/articles/service-worker-lifecycle](https://web.dev/articles/service-worker-lifecycle)

### Gunicorn (Production Server)
* **Gunicorn Official Documentation** Source: [https://docs.gunicorn.org/en/stable/](https://docs.gunicorn.org/en/stable/)
* **Render: Deploying Python Apps** Source: [https://render.com/docs/deploy-python-flask](https://render.com/docs/deploy-python-flask)

---

## Technical Diagnosis (Iteration 5)

| Element | Status | Diagnosis |
| :--- | :--- | :--- |
| **PWA Scope** | Resolved | Moved `sw.js` to the root directory to allow global scope caching. |
| **Server Logic** | Active | Transitioned from Flask's built-in server to Gunicorn for production security. |
| **Data Persistence**| Warning | Current SQLite storage is ephemeral; migration to PostgreSQL recommended. |

---

## Quick Start
```bash
# Production URL
[https://thinktradie.onrender.com](https://thinktradie.onrender.com)

# Git Sync
git pull origin main
pip install -r requirements.txt
python app.py
