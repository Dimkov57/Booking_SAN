# Booking_SAN 🏛️

University room booking system built with **Streamlit + PostgreSQL**.  
Optionally backed by a **C# ASP.NET Web API** for a proper service layer.

---

## Project structure

```
Booking_SAN/
├── main.py              # Streamlit UI (no JSON, pure DB)
├── db.py                # Direct PostgreSQL access (Psycopg2 + Dapper)
├── api_client.py        # Drop-in replacement for db.py using HTTP → C# API
├── .env                 # DB credentials (never commit this!)
├── .gitignore
├── requirements.txt
└── BookingApi/          # C# ASP.NET Web API (optional)
    ├── BookingApi.csproj
    ├── Program.cs
    ├── Models/
    │   └── Models.cs
    ├── Services/
    │   ├── NpgsqlConnectionFactory.cs
    │   ├── UserService.cs
    │   └── BookingService.cs
    └── Controllers/
        ├── UsersController.cs
        └── BookingsController.cs
```

---

## Quick start

### 1. Database

```bash
psql -U postgres -c "CREATE DATABASE booking_san;"
psql -U postgres -d booking_san -f Boo.sql
```

### 2. Environment

Rename `env` → `.env` (or create it):

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=booking_san
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Python dependencies

```bash
pip install -r requirements.txt
```

### 4a. Run with direct DB access (simple)

```bash
streamlit run main.py
```

`main.py` imports `db` — direct PostgreSQL.

### 4b. Run with C# API (optional)

```bash
# Terminal 1 — start the API
cd BookingApi
dotnet run
# Swagger UI: http://localhost:5000/swagger

# Terminal 2 — start Streamlit, pointing at the API
API_BASE_URL=http://localhost:5000 streamlit run main.py
```

Switch the import in `main.py` from `import db` to `import api_client as db` — that's it.

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/users` | All users |
| `POST` | `/api/users` | Register new user |
| `PUT` | `/api/users/{id}` | Update profile |
| `PATCH` | `/api/users/{id}/password` | Change password |
| `GET` | `/api/bookings` | All active bookings |
| `POST` | `/api/bookings` | Create booking |
| `DELETE` | `/api/bookings/{id}` | Cancel booking |

---

## .gitignore

```
.env
__pycache__/
*.pyc
BookingApi/bin/
BookingApi/obj/
users.json
bookings.json
```
