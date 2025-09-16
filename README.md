# UserHub - Task Management API

UserHub is a robust RESTful API built with Django and Django REST Framework. It provides a complete backend solution for a user and task management system, featuring JWT-based authentication, full CRUD operations for tasks, file attachments, and more.

## Features

- **User Authentication**: Secure user registration and login using JSON Web Tokens (JWT).
- **User Profiles**: Extended user model with profile information like full name, date of birth, etc.
- **Task Management**: Full CRUD (Create, Read, Update, Delete) functionality for user-specific tasks.
- **File Attachments**: Users can attach files to their tasks.
- **Pagination**: Task listings are paginated for efficient data retrieval.
- **Search & Ordering**: Tasks can be searched by title/description and ordered via API parameters.
- **Advanced Filtering**: Search, filter, and order tasks through the API.
- **Custom API Actions**:
  - `duplicate`: Create a copy of an existing task.
  - `recent`: Get tasks created in the last 7 days.
  - `delete_all`: Bulk delete all tasks for a user.
- **API Documentation**: Auto-generated API documentation available via Swagger UI and ReDoc.
- **Environment-based Configuration**: Securely manage settings using a `.env` file.

## Technologies Used

- **Backend**: Python, Django, Django REST Framework
- **Database**: SQLite3 (default, configurable)
- **Authentication**: djangorestframework-simplejwt
- **API Documentation**: drf-yasg
- **Dependencies**: django-filter, python-dotenv

---

## Setup and Installation

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd user_management_system
```

### 2. Create and Activate a Virtual Environment

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory by copying the provided example.

```bash
# For Windows
copy .env.example .env

# For macOS/Linux
cp .env.example .env
```

Open the `.env` file and set a new `SECRET_KEY`. You can generate one with the following command:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Run Database Migrations

Apply the database migrations to create the necessary tables.

```bash
python userhub/manage.py migrate
```

### 6. Create a Superuser

Create an admin user to access the Django admin panel.

```bash
python userhub/manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python userhub/manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:

- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`