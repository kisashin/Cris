import reflex as rx
from ..states.auth_state import AuthState
from Dashboard import styles  # ✅ Importa los estilos

def sidebar_item_icon(icon: str) -> rx.Component:
    return rx.icon(icon, size=18)

def sidebar_item(text: str, url: str) -> rx.Component:
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & text == "Dashboard"
    )

    return rx.link(
        rx.hstack(
            rx.match(
                text,
                ("Dashboard", sidebar_item_icon("layout-dashboard")),
                ("Perfil", sidebar_item_icon("user")),
                ("Configuración", sidebar_item_icon("settings")),
                sidebar_item_icon("chevron-right"),
            ),
            rx.text(text, size="3", weight="regular"),
            color=rx.cond(active, styles.accent_text_color, styles.text_color),
            style={
                "_hover": {
                    "background_color": rx.cond(
                        active,
                        styles.accent_bg_color,
                        styles.gray_bg_color,
                    ),
                    "color": rx.cond(
                        active,
                        styles.accent_text_color,
                        styles.text_color,
                    ),
                    "opacity": "1",
                },
                "opacity": rx.cond(active, "1", "0.95"),
            },
            align="center",
            border_radius=styles.border_radius,
            width="100%",
            spacing="2",
            padding="0.5em",
        ),
        underline="none",
        href=url,
        width="100%",
    )

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Mi App", size="4"),
            rx.divider(),
            sidebar_item("Dashboard", "/dashboard"),
            sidebar_item("Perfil", "/profile"),
            sidebar_item("Configuración", "/settings"),
            rx.spacer(),
            rx.cond(
                AuthState.role == "admin",
                rx.button("Administrador", color_scheme="purple", on_click=rx.redirect("/admin")),
                rx.fragment()
            ),
            rx.cond(
                AuthState.is_authenticated,
                rx.fragment(),
            ),
            spacing="4",
            padding="1em",
            align="start",
            width=styles.sidebar_content_width,
        ),
        width=styles.sidebar_width,
        height="100dvh",
        position="fixed",
        top="0",
        left="0",
        bg=rx.color("gray", 2),
        z_index="5",
    )
