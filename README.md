# KanMind Backend

REST API backend for the **KanMind** Kanban board application, built with
**Django** and the **Django REST Framework**. It provides token-based
authentication and endpoints for managing boards, tasks and comments.

This repository contains the **backend only**. It is meant to be used together
with the separate KanMind frontend.

## Tech Stack

- Python 3.9+
- Django 4.2
- Django REST Framework (Token Authentication)
- django-cors-headers
- SQLite (default development database)

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MarcelHaessler/KanMind.git
   cd KanMind
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv env
   source env/bin/activate        # macOS/Linux
   # env\Scripts\activate         # Windows
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the environment file** (see "Environment Variables" below)
   ```bash
   cp .env.example .env
   # then open .env and set a real SECRET_KEY
   ```

5. **Apply the migrations**
   ```bash
   python3 manage.py migrate
   ```

6. **Create a superuser** (for the Django admin)
   ```bash
   python3 manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python3 manage.py runserver
   ```
   The API is now available at `http://127.0.0.1:8000/`.

## Environment Variables

The project reads its secret key from a `.env` file (loaded via
`python-dotenv`). A template is provided in `.env.example`:

```
SECRET_KEY=your-secret-key-here
```

Copy it to `.env` and set your own value. Without a valid `SECRET_KEY`
the server will not start.

## Frontend Connection (CORS)

The frontend must point its API base URL to `http://127.0.0.1:8000`.

CORS is preconfigured for the Live Server default port `5500` in
`core/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5500',
    'http://localhost:5500',
]
```

If your frontend runs on a different port, add it to this list.

## Authentication

All endpoints (except registration and login) require a token. After
registering or logging in you receive a token, which must be sent in the
`Authorization` header of every request:

```
Authorization: Token <your-token>
```

## API Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST | `/api/registration/` | Register a new user, returns a token |
| POST | `/api/login/` | Log in, returns a token |
| GET | `/api/email-check/?email=` | Check whether an email is registered |
| GET | `/api/boards/` | List the boards the user owns or is a member of |
| POST | `/api/boards/` | Create a new board |
| GET | `/api/boards/{id}/` | Board details including members and tasks |
| PATCH | `/api/boards/{id}/` | Update board title / members |
| DELETE | `/api/boards/{id}/` | Delete a board (owner only) |
| GET | `/api/tasks/assigned-to-me/` | Tasks assigned to the current user |
| GET | `/api/tasks/reviewing/` | Tasks the current user is reviewing |
| POST | `/api/tasks/` | Create a task in a board |
| PATCH | `/api/tasks/{id}/` | Update a task |
| DELETE | `/api/tasks/{id}/` | Delete a task (creator or board owner) |
| GET | `/api/tasks/{id}/comments/` | List comments of a task |
| POST | `/api/tasks/{id}/comments/` | Add a comment to a task |
| DELETE | `/api/tasks/{id}/comments/{comment_id}/` | Delete a comment (author only) |

## Project Structure

```
core/         # Project configuration (settings, root urls)
auth_app/     # Registration, login, email-check
  api/        # serializers, views, urls
kanban_app/   # Boards, tasks, comments
  models.py
  api/        # serializers, views, urls, permissions
```
