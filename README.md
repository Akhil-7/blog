# BlogManagement

A Django-based backend application for managing tasks and users. This project is structured into multiple apps for better modularity.

## 📁 Project Structure

```
BLOG/
├── API/                      # Aggregator app for routing
│   ├── urls.py              # API-level routing
│
├── blog_management/              # App for managing blogs and comment
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # BlogPost and Comment model definition
│   ├── serializers.py       # Serializers for task models
│   ├── tests.py
│   ├── urls.py              # App-specific routes
│   ├── views.py             # Blog and Comment -related views
│
├── blog/          # Project settings
│   ├── settings.py
│   ├── urls.py              # Root URL configuration
│   ├── asgi.py
│   ├── wsgi.py
│
├── user_management/              # App for managing users
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # User model definition
│   ├── serializers.py       # Serializers for user models
│   ├── tests.py
│   ├── urls.py              # App-specific routes
│   ├── views.py             # User-related views
│
├── db.sqlite3               # SQLite database
├── manage.py                # Django CLI utility
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Django 3.2+
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Akhil-7/blogmanagement.git
   cd blog
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**  
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**  
   ```bash
   python manage.py runserver
   ```

6. **Access the API**  
   Navigate to `http://127.0.0.1:8000/` in your browser or use tools like Postman.



## 📦 API Overview

The APIs are split into two major parts:

- **Blog Management**: Create, delete, and retrieve blogs. Add and view comments.
- **User Management**: Register, authenticate, and manage users.

## 🔧 Configuration

All project-level settings can be found in:

```
blog/settings.py
```


## 📌 API Endpoints

### 🔐 User Management
| Method | Endpoint                 | Description              |
|--------|--------------------------|--------------------------|
| POST   | `api/user/register/`     | Register a new user      |
| POST   | `api/user/login/`        | Authenticate a user      |

### ✅ Blog Management
| Method | Endpoint                                             | Description                                                  |
|--------|------------------------------------------------------|--------------------------------------------------------------|
| GET    | `api/blog/blogs/`                                    | Retrieve all blogs                                           |
| GET    | `api/blog/blogs/?serach=search`                      | Retrieve all blogs contains search tearm                     |
| GET    | `api/blog/blogs/?page_num=_any_num_`                 | Retrieve all blogs in the current pagination                 |
| POST   | `api/blog/blogs/`                                    | Create a new blog                                            |
| GET    | `api/blog/blogs/<int:pk>/?comment_page_num=_any_num_`| Retrieve a specific blog with comments in current pagination |
| DELETE | `api/blog/blogs/<int:pk>/`                           | Delete a specific task                                       |
| POST   | `api/blog/blogs/<int:pk>/add_comment/`               | View dashboard summary or stats                              |