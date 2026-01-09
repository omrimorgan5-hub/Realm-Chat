# Realm Chat 🗨️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-building-important)](https://github.com/omrimorgan5-hub/Realm-Chat)

A full-stack real-time chat application built as part of my college-application portfolio.  
The codebase starts in plain JavaScript and Flask, then progressively migrates to **TypeScript** and **Django** for a production-grade, scalable architecture.

Follow the journey from MVP to polished product—PRs, issues, and feedback are welcome!

---

## ✨ Features (so far)

* Secure e-mail based authentication (Flask-JWT)
* Real-time messaging via WebSockets
* Responsive, vanilla-JS frontend (TypeScript refactor in progress)
* JSON file store → PostgreSQL migration planned

---

## 🛠 Tech Roadmap

| Layer        | Phase 1 (MVP)               | Phase 2 (Scale)            |
|--------------|-----------------------------|----------------------------|
| **Frontend** | JavaScript, HTML, CSS       | TypeScript + Vite          |
| **Backend**  | Flask, Flask-SocketIO       | Django, Django-Channels    |
| **Database** | JSON Flat Files             | PostgreSQL                 |
| **Auth**     | e-mail verification         | JWT + refresh tokens       |
| **Deploy**   | localhost                   | Docker + Railway / Render  |

---

## 🚀 Quick Start (local dev)

```bash
# 1. Clone repo
git clone https://github.com/omrimorgan5-hub/Realm-Chat.git
cd Realm-Chat

# 2. Backend (Flask)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# 3. Frontend (live-server or any static server)
cd frontend
npm install -g live-server
live-server --port=5500

Realm-Chat/
├─ backend/          # Flask code (will move to django/ later)
├─ frontend/         # HTML, CSS, JS → TS
├─ docs/             # Screenshots, ER diagrams, API spec
├─ tests/            # Pytest + Jest suites (WIP)
└─ README.md

| Months | Milestone                                                 |
| ------ | --------------------------------------------------------- |
| 1-4    | ✅ Auth (signup/login), e-mail verification, basic WS chat |
| 5-8    | 🔄 TypeScript refactor, persistent DB, user profiles      |
| 9-12   | ⏳ Django migration, group rooms, reactions, CI/CD         |

🤝 Contributing

    Fork & clone
    Create feature branch (git checkout -b feature/amazing-feature)
    Commit (git commit -m 'Add amazing feature')
    Push (git push origin feature/amazing-feature)
    Open a Pull Request

📄 License
MIT © Omri Morgan
📫 Stay in Touch
Star ⭐ this repo to follow along as commits land and milestones get crushed. Questions? Open an issue or DM me on Twitter.
