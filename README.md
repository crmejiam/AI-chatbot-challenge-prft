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

# Running Locally with Python Virtual Environment

To run this project on any PC after cloning the repository:

1. Clone the repository
    ```sh
    git clone https://github.com/crmejiam/AI-chatbot-challenge-prft.git
    cd AI-chatbot-challenge-prft
    ```

2. Create and activate a Python virtual environment
    ```sh
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. Install dependencies
    ```sh
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. Run the Flask app
    ```sh
    python -m flask --app app.routes run
    ```

5. Access the app
    Open your browser and go to: http://localhost:5000

### Main Endpoints
- `POST /chat/` — Ask questions about GitHub Actions and get actionable, accurate information from the chatbot.
- `POST /users/register` — Register a new account with email and password for personalized chat experience.
- `POST /users/login` — Log in securely to access chat features and history.
- `GET /admin/users` — Admin: View a list of all registered users for management and audit.
- `DELETE /admin/users/{userId}` — Admin: Remove (delete) users who should no longer have access.

---

## Team Members
- Felipe Acevedo Montoya
- Andres Zuluaga Mejia
- Cristian Mejia Martinez
