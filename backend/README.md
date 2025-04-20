## ATLAS API

# How to set up
  You need python (version 3.x), poetry and postgresql installed

```bash
sudo apt install python3
```

```bash
sudo apt install python3-poetry
```

```bash
sudo apt install postgresql postgresql-contrib
```

# Set up .env files
```bash
DB_NAME=atlasdb
DB_USER=<YOUR_USER_NAME OR POSTGRES>
DB_PASSWORD=<YOUR_PASSWORD>
DB_HOST=localhost
DB_PORt=5432
```

# Install packages using
```bash
poetry install
```

# How to run

```bash
poetry run python manage.py runserver
```

# Run tests with 
```bash
poetry run python manage.py test <module>.<tests>.<test_model>
```

# API Endpoints
```html
/signup and /login
```

# API endpoints example usage
Check status
```bash
curl http://localhost:8000/api/status
```

To signup
```bash
curl -X POST http://localhost:8000/api/signup/   -H "Content-Type: application/json"   -d '{"email": "test@example.com", "password": "strongpassword", "user_type": "GENERAL"}'
```

Then login using
```bash 
curl -X POST http://localhost:8000/api/login/-H "Content-Type: application/json"-d '{"email": "test@example.com", "password": "strongpassword"}'
```
