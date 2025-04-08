import reflex as rx
from ..states.auth_state import AuthState
from Dashboard.components.navbar import navbar
from Dashboard.components.sidebar import sidebar
from ..states.admin_state import AdminState 

@rx.page(route="/admin", title="Panel de Administración", on_load=AdminState.load_usuarios)
def admin_page() -> rx.Component:
    return rx.cond(
        (AuthState.is_authenticated & (AuthState.role == "admin")),
        rx.hstack(
            sidebar(),
            rx.box(
                navbar(),
                rx.vstack(
                    rx.heading("Bienvenido al Panel de Administración", size="5"),
                    rx.text("Aquí puedes gestionar opciones exclusivas para administradores."),
                    rx.button("Cargar Usuarios", on_click=AdminState.load_usuarios),
                    rx.foreach(
                        AdminState.usuarios,
                        lambda usuario, index: rx.hstack(
                            rx.text(usuario.username, width="20%"),
                            rx.input(
                                value=usuario.role,
                                on_change=lambda value: AdminState.actualizar_usuario(index, "role", value),
                                placeholder="Rol",
                                width="20%",
                            ),
                            rx.input(
                                value=usuario.empresa,
                                on_change=lambda value: AdminState.actualizar_usuario(index, "empresa", value),
                                placeholder="Empresa",
                                width="30%",
                            ),
                            spacing="4",
                            width="100%",
                            padding_y="0.5em",
                        ),
                    ),
                    rx.button("Guardar Cambios", on_click=AdminState.guardar_cambios, color_scheme="green"),
                    rx.text(AdminState.message, color="green"),
                ),
                width="100%",
            ),
            width="100%",
            height="100dvh",
        ),
        rx.script("window.location.href = '/login'") 
    )