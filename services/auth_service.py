import os
import json
import hashlib
from typing import Optional, Dict, Any, List

try:
    import streamlit as st
except ImportError:
    st = None

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.json")

def hash_password(password: str) -> str:
    """Hashes a plain text password using SHA-256."""
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()

def _load_data() -> Dict[str, Any]:
    """Loads user & trip database from data/users.json."""
    if not os.path.exists(USERS_FILE):
        return {"users": [], "trips": []}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"users": [], "trips": []}

def _save_data(data: Dict[str, Any]) -> bool:
    """Saves user & trip database back to data/users.json."""
    try:
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False

def authenticate_user(email_or_username: str, password: str) -> Optional[Dict[str, Any]]:
    """Validates user credentials against database."""
    data = _load_data()
    clean_id = email_or_username.strip().lower()
    hashed = hash_password(password)

    for user in data.get("users", []):
        user_email = user.get("email", "").strip().lower()
        user_name = user.get("name", "").strip().lower()
        if (clean_id == user_email or clean_id == user_name) and user.get("password_hash") == hashed:
            user_safe = dict(user)
            user_safe.pop("password_hash", None)
            return user_safe
    return None

def register_user(
    name: str,
    email: str,
    password: str,
    travel_style: str = "Relaxed",
    home_city: str = "Hyderabad"
) -> (bool, str):
    """Registers a new user into the database."""
    if not name or not email or not password:
        return False, "All fields (Name, Email, Password) are required."

    if len(password) < 4:
        return False, "Password must be at least 4 characters long."

    data = _load_data()
    clean_email = email.strip().lower()

    for user in data.get("users", []):
        if user.get("email", "").strip().lower() == clean_email:
            return False, f"An account with email '{email}' already exists. Please log in."

    new_user = {
        "id": f"usr_{len(data.get('users', [])) + 1:03d}",
        "name": name.strip(),
        "email": clean_email,
        "password_hash": hash_password(password),
        "role": "Student Explorer",
        "phone": "+91 98000 00000",
        "home_city": home_city.strip() if home_city else "Hyderabad",
        "travel_style": travel_style,
        "joined_date": "2026-11-15",
        "avatar_emoji": "🎒"
    }

    data.setdefault("users", []).append(new_user)
    if _save_data(data):
        return True, "Registration successful! You can now log in."
    return False, "Failed to save user. Please try again."

def get_user_trips(user_email: str) -> List[Dict[str, Any]]:
    """Retrieves all saved trips for the given user email."""
    data = _load_data()
    clean_email = user_email.strip().lower()
    return [t for t in data.get("trips", []) if t.get("user_email", "").strip().lower() == clean_email]

def is_logged_in() -> bool:
    """Checks if a user is currently authenticated in session state."""
    if st and hasattr(st, "session_state"):
        return bool(st.session_state.get("is_authenticated", False))
    return False

def get_current_user() -> Optional[Dict[str, Any]]:
    """Returns the authenticated user object or None."""
    if st and hasattr(st, "session_state"):
        return st.session_state.get("user_info", None)
    return None

def login_user(user_dict: Dict[str, Any]):
    """Sets session state to logged in with the given user profile."""
    if st and hasattr(st, "session_state"):
        st.session_state["is_authenticated"] = True
        st.session_state["user_info"] = user_dict
        if "origin_input" in st.session_state:
            st.session_state["origin_input"] = user_dict.get("home_city", "Hyderabad")

def logout_user():
    """Logs out the user and clears authentication state."""
    if st and hasattr(st, "session_state"):
        st.session_state["is_authenticated"] = False
        st.session_state["user_info"] = None
