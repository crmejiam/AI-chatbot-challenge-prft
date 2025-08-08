# User Stories for AI Chatbot Challenge PRFT

---

## Story 1
**Persona:** Customer
**Story:** As a customer, I want to ask questions about GitHub Actions so I can understand how to automate my workflows.
**Statement:** "I want to know how to set up a CI/CD pipeline using GitHub Actions."
**Benefit:** Enables customers to get accurate, actionable information quickly.
**Acceptance Criteria:**
- The chatbot responds with clear steps for setting up a CI/CD pipeline.
- The information is specific to GitHub Actions.
**Mapped Endpoint:** POST /chat/

---


## Story 2
**Persona:** Customer
**Story:** As a customer, I want to register an account so I can securely access the chat application and save my chat history.
**Statement:** "I want to sign up and create my own account."
**Benefit:** Allows customers to have personalized experiences and access previous conversations.
**Acceptance Criteria:**
- Customers can register with a valid email and password.
- Registration confirmation is sent to the customer.
- Errors are shown for invalid or duplicate registrations.
**Mapped Endpoint:** POST /users/register

---


## Story 3
**Persona:** Admin
**Story:** As an admin, I want to view all registered users and remove users if necessary so I can manage access to the chat application.
**Statement:** "I need to see a list of all users and be able to delete users who should no longer have access."
**Benefit:** Ensures proper user management and security within the chat app.
**Acceptance Criteria:**
- Admins can retrieve a list of all registered users.
- Admins can remove (delete) users from the system.
- Actions are logged for audit purposes.
**Mapped Endpoints:**
- GET /admin/users
- DELETE /admin/users/{userId}

---


## Story 4
**Persona:** Customer
**Story:** As a customer, I want to log in to my account so I can access my chat history and interact with the chatbot securely.
**Statement:** "I want to log in with my credentials to use the chat app."
**Benefit:** Ensures secure access and personalized experience for each customer.
**Acceptance Criteria:**
- Customers can log in with a valid email and password.
- Login errors are handled gracefully (e.g., incorrect password, non-existent account).
- Successful login grants access to chat features and history.
**Mapped Endpoint:** POST /users/login

---

## Story 5
**Persona:** Developer
**Story:** As a developer, I want to test the chatbot endpoints so I can ensure reliability before deployment.
**Statement:** "I need to verify that all chat-related endpoints work as expected."
**Benefit:** Reduces bugs and improves system stability.
**Acceptance Criteria:**
- All endpoints are covered by automated tests.
- Tests pass for typical and edge cases.
**Mapped Endpoint:** GET /test/endpoints
