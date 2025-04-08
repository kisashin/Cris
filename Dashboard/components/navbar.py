import reflex as rx
from Dashboard import styles 
from ..states.auth_state import AuthState

def navbar() -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        rx.el.nav(
            rx.hstack(
                rx.color_mode_cond(
                    rx.image(src="/reflex_black.svg", height="1em"),
                    rx.image(src="/reflex_white.svg", height="1em"),
                ),
                rx.spacer(),
                rx.button(
                    "Cerrar sesión",
                    on_click=AuthState.logout,
                    color_scheme="red",
                    style={
                        "border_radius": styles.border_radius,
                        "_hover": {
                            "opacity": "0.9"
                        },
                    },
                ),
                align="center",
                width="100%",
                padding_y="1.25em",
                padding_x=["1em", "1em", "2em"],
            ),
            position="sticky",
            top="0px",
            background_color=rx.color("gray", 1),
            border_bottom=styles.border,
            z_index="5",
        ),
        rx.fragment(),
    )
