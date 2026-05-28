"""
api_client.py
=============
HTTP-клієнт для C# ASP.NET Web API (BookingApi).
Використовується замість db.py коли API запущено.

Щоб переключитися з db.py на api_client.py — просто змініть імпорт у main.py:
    import api_client as db
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv(".env")

API_BASE = os.getenv("API_BASE_URL", "http://localhost:5000")
TIMEOUT  = 10  # секунд


def _get(path: str, **params) -> requests.Response:
    return requests.get(f"{API_BASE}{path}", params=params, timeout=TIMEOUT)


def _post(path: str, payload: dict) -> requests.Response:
    return requests.post(f"{API_BASE}{path}", json=payload, timeout=TIMEOUT)


def _put(path: str, payload: dict) -> requests.Response:
    return requests.put(f"{API_BASE}{path}", json=payload, timeout=TIMEOUT)


def _patch(path: str, payload: dict) -> requests.Response:
    return requests.patch(f"{API_BASE}{path}", json=payload, timeout=TIMEOUT)


# ══════════════════════════════════════════════════════════════════════════════
# USERS
# ══════════════════════════════════════════════════════════════════════════════

def get_all_users() -> dict:
    """Повертає {student_id: user_dict} — той самий формат що й db.py."""
    resp = _get("/api/users")
    resp.raise_for_status()
    users = resp.json()  # List[UserDto]
    return {u["student_id"]: u for u in users}


def create_user(student_id, first_name, last_name, email,
                faculty, password_hash, joined) -> bool:
    resp = _post("/api/users", {
        "student_id":    student_id,
        "first_name":    first_name,
        "last_name":     last_name,
        "email":         email,
        "faculty":       faculty,
        "password_hash": password_hash,
        "joined":        joined,
    })
    return resp.status_code == 201


def update_user(student_id, first_name, last_name, email, faculty) -> None:
    resp = _put(f"/api/users/{student_id}", {
        "first_name": first_name,
        "last_name":  last_name,
        "email":      email,
        "faculty":    faculty,
    })
    resp.raise_for_status()


def update_password(student_id, new_password_hash) -> None:
    resp = _patch(f"/api/users/{student_id}/password", {
        "password_hash": new_password_hash,
    })
    resp.raise_for_status()


# ══════════════════════════════════════════════════════════════════════════════
# BOOKINGS
# ══════════════════════════════════════════════════════════════════════════════

def get_all_bookings() -> list:
    """Повертає список booking_dict — той самий формат що й db.py."""
    resp = _get("/api/bookings")
    resp.raise_for_status()
    return resp.json()  # List[BookingDto]


def add_booking(booking: dict) -> bool:
    resp = _post("/api/bookings", booking)
    return resp.status_code == 201


def cancel_booking(booking_id: str) -> None:
    resp = requests.delete(f"{API_BASE}/api/bookings/{booking_id}", timeout=TIMEOUT)
    resp.raise_for_status()
