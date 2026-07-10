# Backend

## Local Development

### Docker Compose

Run from the repository root:

```bash
docker compose up --build
```

### Manual Python Run

Create and activate the backend virtual environment:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
```

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Run migrations from the repository root:

```bash
alembic -c backend/alembic.ini upgrade head
```

Start the API from the repository root using the package path:

```bash
python -m uvicorn backend.main:app --reload
```

Do not use `uvicorn main:app --reload` from inside `backend/`; this monorepo expects package-qualified startup from the repository root.

## Useful URLs

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs