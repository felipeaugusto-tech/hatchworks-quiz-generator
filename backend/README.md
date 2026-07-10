```bash
docker compose up --build
```

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

```powershell
.\.venv\Scripts\Activate.ps1
``` 
 
```
pip install -r requirements.txt
```

```
alembic -c alembic.ini upgrade head
```

```
uvicorn main:app --reload
```


## Useful URLs:
- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs