# Django Service Desk

A web-based help desk / ticketing system built with Django. Supports role-based access for Agents, Managers, and Customers, with real-time UI updates powered by HTMX and a Bootstrap 5 interface.

## Features

- **Role-based access control** — Agents, Managers, Customers with different permissions
- **Ticket management** — Create, assign, prioritize, and track tickets through a full status workflow
- **Internal records** — Agents can add internal notes invisible to customers
- **File attachments** — Upload images, documents, archives (max 30 MB per file)
- **Follower system** — Subscribe to tickets to track updates
- **Read/unread tracking** — See which tickets have new activity
- **Dynamic UI** — HTMX-powered pagination and modals, no page reloads
- **Filterable tables** — Filter and sort tickets by status, priority, company, date, assignee

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0 |
| Database | PostgreSQL or SQLite |
| Auth | django-allauth |
| Forms | django-crispy-forms + crispy-bootstrap5 |
| Tables | django-tables2 |
| Filters | django-filter |
| Frontend | Bootstrap 5, HTMX, Tom Select |
| Dev tools | django-debug-toolbar |

## Prerequisites

- Python 3.11+
- pip
- PostgreSQL 13+ *(optional — SQLite works out of the box)*

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/django-service-desk.git
cd django-service-desk
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirments.txt
```

### 4. Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=django_service_desk
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhost
DB_PORT=5432

# Settings module
DJANGO_SETTINGS_MODULE=_project.settings.local

# Custom admin URL (security through obscurity)
ADMIN_URL=your-custom-admin-path
```

To generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Set up the database

**Option A — SQLite** (no extra setup required, good for development):

Leave `DB_*` variables out of your `.env`. Django will use a local `db.sqlite3` file automatically.

**Option B — PostgreSQL** (recommended for production):

```sql
CREATE DATABASE django_service_desk;
CREATE USER db_user WITH PASSWORD 'db_password';
GRANT ALL PRIVILEGES ON DATABASE django_service_desk TO db_user;
```

Then fill in the `DB_*` variables in your `.env` as shown in step 4.

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create user groups

```bash
python manage.py setup_groups
```

This creates three groups: **Agents**, **Managers**, **Customers**.

### 8. Create a superuser

```bash
python manage.py createsuperuser
```

### 9. Collect static files (production only)

```bash
python manage.py collectstatic
```

### 10. Start the development server

```bash
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration

### Settings modules

| Module | Purpose |
|---|---|
| `_project.settings.base` | Shared base settings |
| `_project.settings.local` | Development (adds debug toolbar) |
| `_project.settings.production` | Production |

Set `DJANGO_SETTINGS_MODULE` in your `.env` accordingly.

### User management

Sign-up is **disabled by default** — users must be created via Django admin at `/<ADMIN_URL>/`. After creating a user, assign them to one of the three groups:

- **Agents** — full access, can manage all tickets and add internal records
- **Managers** — access limited to their company's tickets, read-only ticket fields
- **Customers** — access limited to their company's tickets, cannot see internal records

Users must also be associated with a **Company** via the admin panel.

## URL Overview

| URL | View |
|---|---|
| `/` | Redirect to dashboard or login |
| `/dashboard/` | Ticket dashboard with recent activity |
| `/tickets/` | Full ticket list with filters |
| `/tickets/create/` | Create a new ticket |
| `/tickets/<number>/` | Ticket detail, records, attachments |
| `/accounts/login/` | Login (allauth) |
| `/<ADMIN_URL>/` | Django admin |

## Project Structure

```
django-service-desk/
├── _project/               # Django project config
│   └── settings/
│       ├── base.py
│       ├── local.py
│       └── production.py
├── service_desk/           # Main application
│   ├── management/
│   │   └── commands/
│   │       └── setup_groups.py
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── filters.py
│   ├── tables.py
│   ├── signals.py
│   └── services.py
├── _media/                 # Uploaded files
├── _static/                # Collected static files
├── manage.py
├── requirments.txt
└── .env.example
```