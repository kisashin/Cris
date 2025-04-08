# Dashboard/pages/dashboard.py
import reflex as rx
from ..states.auth_state import AuthState
from Dashboard.components.navbar import navbar
from Dashboard.components.sidebar import sidebar

@rx.page(route="/dashboard", title="Dashboard")
def dashboard_page() -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        rx.hstack(
            sidebar(),
            rx.box(
                navbar(),
                rx.vstack(
                    rx.heading(f"Bienvenido {AuthState.username}", size="5"),
                    rx.text(f"Tu rol es: {AuthState.role}"),
                    spacing="4",
                    padding="2em",
                ),
                width="100%",
            ),
            width="100%",
            height="100dvh",
        ),
        # 👇 Esta parte redirige al login si no está autenticado
        rx.script("window.location.href = '/login'")
    )
