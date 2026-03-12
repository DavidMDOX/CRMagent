import os
from typing import Optional
from itsdangerous import URLSafeSerializer
from .data_store import USERS, User

def get_serializer() -> URLSafeSerializer:
    return URLSafeSerializer(secret_key=os.getenv("SECRET_KEY", "local-dev-secret"), salt="coppertrade-auth")

def authenticate(username: str, password: str) -> Optional[User]:
    dynamic_admin_password = os.getenv("ADMIN_PASSWORD")
    if username == "admin" and dynamic_admin_password:
        admin = USERS["admin"]
        if password == dynamic_admin_password:
            return User(admin.username, password, admin.role, admin.display_name)
    user = USERS.get(username)
    if user and user.password == password:
        return user
    return None

def issue_session(user: User) -> str:
    return get_serializer().dumps({"username":user.username,"role":user.role,"display_name":user.display_name})

def read_session(token: str | None):
    if not token:
        return None
    try:
        return get_serializer().loads(token)
    except Exception:
        return None
