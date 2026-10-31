# Agent Project

This project is a Django-based web application with an AI chat/agent feature.

## Project Structure

```text
agent/
├── backend/
│   ├── src/
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── requirements.txt
│   ├── .env
│   ├── static/
│   ├── templates/
│   ├── agent/
│   └── chat/
├── README.md
└── .gitignore
```

## Tech Stack

### Backend / Web App
- Python
- Django
- SQLite
- Django templates
- Python environment with project dependencies

### AI / API Layer
- FastAPI-style service logic may be used in the backend modules
- SQLAlchemy models may be part of the project structure

## Project Setup

### 1. Go to the frontend directory

```bash
cd frontend
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Start the Django development server

```bash
python manage.py runserver
```

The app will usually run at:

```text
http://127.0.0.1:8000/
```

## App Overview

This Django project contains app modules such as:
- `agent`
- `chat`

These may include:
- chat views
- agent logic
- templates and static files
- database models for conversation storage

## Environment Configuration

Create a `.env` file inside the `frontend` directory if needed and configure values such as:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

## Database

The project currently uses SQLite by default:

```text
frontend/db.sqlite3
```

You can change the database settings in the Django settings file if needed.

## Useful Commands

Create a new app:

```bash
python manage.py startapp appname
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Run a Django shell:

```bash
python manage.py shell
```

## Notes

- This is a Django project, not a React app.
- The frontend is server-rendered and/or template-based.
- If you later add an API layer, it can coexist with Django views.

## License

This project is for local development or internal use unless otherwise specified.
