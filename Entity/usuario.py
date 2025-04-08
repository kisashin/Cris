import reflex as rx
from typing import Optional

class Usuario(rx.Base):
    id_usuario: Optional[int] = None
    username: str
    hashed_password: str
    role: str = "usuario"
    empresa: str = ""