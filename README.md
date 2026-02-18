# TradieFlow · Iteration 4 
**Version: 5 (Iteration 4)** **Date: 04 February 2026**

**TradieFlow** is a lightweight, mobile-first productivity tool designed for sole traders and small crews to manage materials, tasks, and documentation without unnecessary admin. This iteration marks the strategic rebranding from the "Tradespeople App" to **TradieFlow**, reflecting a more streamlined and professional digital experience. The application has been transformed from a functional MVP into a premium professional tool with a focus on high-end UI/UX and mandatory secure authentication.

## Project Roadmap
* **Iteration 1:** Core Inventory module with low-stock logic.
* **Iteration 2:** Document Capture (upload/metadata) and Task Manager.
* **Iteration 3:** Document Vault, mobile camera capture, and Daily Task view.
* **Iteration 4:** High-level UI refurbishment, TradieFlow branding, secure user authentication, and Vault renaming.

---

## Features (Iteration 4 Refinements)

### User Authentication & Access Control
* **Mandatory Sign-In:** Application-wide privacy enforced via `@login_required` decorators; all core routes are locked by default.
* **Secure Sessions:** Signed session cookies ensure trade data remains private to the authenticated user.
* **Password Security:** Industry-standard PBKDF2 hashing handled via Werkzeug.
* **Personalised Experience:** Dashboard greets users by their registered `first_name` and features a unique builder avatar.
* **Refined Profile:** Displays "Member Since" in `dd/mm/yyyy` format with a simplified "Active" status.

### Premium Dashboard (Bento Grid)
* **High-Level Layout:** "Bento Grid" design for organised data visualisation inspired by bank-grade SaaS.
* **Visual Feedback:** Real-time "System Active" pulse indicators and personalised greetings.
* **Aesthetic:** Responsive dark-mode palette (#0e0f11) with neon-lime (#ccff00) accents.

### Document Vault (Extended)
* **Metadata Management:** New renaming functionality (US11) allows users to assign meaningful labels to stored files without altering the disk filename.
* **Professional Explorer:** High-level view for site media and PDFs with secure view/delete actions.

---

## Technical References & Research Sources

### UI / UX & High-Level Design
* **Pixel Rocket Global Bank Template** (Design Foundation)  
    [https://pixelrocket.store/free-templates/nextjs-templates/global-bank-nextjs-website-template](https://pixelrocket.store/free-templates/nextjs-templates/global-bank-nextjs-website-template)
* **Tailwind CSS Utility Patterns** (Bento Grid & Spacing)  
    [https://tailwindcss.com/docs/grid-template-columns](https://tailwindcss.com/docs/grid-template-columns)
* **Glassmorphism & Radial Gradients** [https://css-tricks.com/almanac/properties/g/gradient/](https://css-tricks.com/almanac/properties/g/gradient/)

### Backend & Security
* **Werkzeug Security Helpers** (PBKDF2 Hashing)  
    [https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security](https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security)
* **Flask Session Management** [https://flask.palletsprojects.com/en/stable/quickstart/#sessions](https://flask.palletsprojects.com/en/stable/quickstart/#sessions)
* **Flask View Decorators** (login_required logic)  
    [https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/](https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/)
* **Secure File Sanitisation** [https://flask.palletsprojects.com/en/stable/patterns/fileuploads/](https://flask.palletsprojects.com/en/stable/patterns/fileuploads/)

### Frontend Semantics
* **Custom Branding:** Custom TF emblem designed for high-contrast visibility.
* **Jinja2 Custom Filters:** Implementation of `dd/mm/yyyy` date formatting for UK/IE standards.



## Database Schema (SQLite)

* **Users Table:** Stores first/last names, email (unique), and secure password hashes.
* **Tasks Table:** Stores titles, notes, and ISO 8601 due_dates for Daily Task filtering.
* **Inventory Table:** Tracks quantities and low-stock thresholds.
* **Documents Table:** Metadata storage including `display_name`; physical files stored in `/uploads`.

## Quick Start
```bash
# Set up environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install and run
pip install -r requirements.txt
python app.py