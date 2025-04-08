import reflex as rx
from Dashboard.states.auth_state import AuthState

def login_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                # Logo y título
                rx.center(
                    rx.image(
                        src="/logo.png",
                        width="2.5em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Inicia sesión en tu cuenta",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                # Input de usuario
                rx.vstack(
                    rx.text("Nombre de usuario", size="3", weight="medium", text_align="left", width="100%"),
                    rx.input(
                        rx.input.slot(rx.icon("user")),
                        placeholder="usuario",
                        type="text",
                        size="3",
                        width="100%",
                        on_change=AuthState.set_login_username
                    ),
                    spacing="2",
                    width="100%",
                ),
                # Input de contraseña
                rx.vstack(
                    rx.hstack(
                        rx.text("Contraseña", size="3", weight="medium"),
                        rx.link("¿Olvidaste tu contraseña?", href="#", size="3"),
                        justify="between",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="Contraseña",
                        type="password",
                        size="3",
                        width="100%",
                        on_change=AuthState.set_login_password
                    ),
                    spacing="2",
                    width="100%",
                ),
                # Botón de iniciar sesión
                rx.button("Entrar", size="3", width="100%", is_loading=AuthState.is_loading, on_click=AuthState.login,),
                # Enlace a registro
                rx.center(
                    rx.text("¿Nuevo aquí?", size="3"),
                    rx.link("Regístrate", href="/register", size="3"),
                    opacity="0.8",
                    spacing="2",
                    direction="row",
                    width="100%",
                ),
                rx.text(AuthState.message, color="red", text_align="center", width="100%"),
                spacing="6",
                width="100%",
            ),
            max_width="28em",
            size="4",
            width="100%",
        ),
        height="100vh",
        width="100vw",
        bg="black",
    )
