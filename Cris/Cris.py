import reflex as rx
from Dashboard.pages.login import login_page
from Dashboard.pages.register import register_page
from Dashboard.pages.dashboard import dashboard_page
from Dashboard.pages.admin import admin_page

# Página raíz con redirección
def index():
    return rx.script("window.location.href = '/login';")

app = rx.App()
app.add_page(index, route="/", title="Inicio")
app.add_page(login_page, route="/login", title="Login")
app.add_page(register_page, route="/register", title="Registro")
app.add_page(dashboard_page, route="/dashboard", title="Dashboard")
app.add_page(admin_page, route="/admin", title="Panel de Administración") 
