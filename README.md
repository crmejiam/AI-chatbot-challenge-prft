# AI Chatbot Challenge PRFT

This repository will host a custom chat application designed to interact with clients in a polite and professional manner. The chatbot will maintain a strong focus on delivering an excellent customer experience, ensuring that all interactions are courteous and helpful.

Key features:
- Polite and respectful communication
- Accurate and specific information about GitHub Actions
- Dedicated to providing clear, concise, and relevant answers
- Focused on client satisfaction and support


The goal of this project is to create a reliable and effective chatbot that enhances client engagement and delivers high-quality assistance regarding GitHub Actions.

---

## Web Service Information

This repository includes a Python/Flask web service that powers the chat application. The service exposes RESTful endpoints for chat interactions, user registration, login, and admin user management.

### Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the web service:
   ```bash
   python run.py
   ```

### Main Endpoints
- `POST /chat/` — Interact with the chatbot
- `POST /users/register` — Register a new user
- `POST /users/login` — Log in as a user
- `GET /admin/users` — List all users (admin)
- `DELETE /admin/users/{userId}` — Remove a user (admin)

---

## Team Members
- Felipe Acevedo Montoya
- Andres Zuluaga Mejia
- Cristian Mejia Martinez
