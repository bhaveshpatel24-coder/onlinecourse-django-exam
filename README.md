# OnlineCourse

A small Django course and mock-exam application with an admin interface.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/` to create courses, lessons, questions, and choices. Public course detail pages use `/courses/<course-id>/`; the exam is at `/courses/<course-id>/exam/` and requires a signed-in user.

The included settings and secret key are for local development only. Configure a secure secret key, database, and production settings before deployment.
