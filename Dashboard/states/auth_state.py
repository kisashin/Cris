import logging
import reflex as rx
import asyncio
import bcrypt
from Entity.usuario import Usuario
from Data.usuario_repository import UsuarioRepository

logging.basicConfig(level=logging.ERROR)

class SessionState(rx.State):
    is_authenticated: bool = False
    username: str = ""
    role: str = ""
    empresa: str = ""
    message: str = ""

    @rx.event
    def logout(self):  # Añadimos la anotación de tipo
        self.is_authenticated = False
        self.username = ""
        self.role = ""
        self.empresa = ""
        self.message = ""
        yield rx.redirect("/")  # Esto sí hace la redirección real


class AuthState(SessionState):
    login_username: str = ""
    login_password: str = ""
    register_username: str = ""
    register_password: str = ""
    register_empresa: str = ""
    is_loading: bool = False

    @rx.event
    async def login(self):
        if not self.login_username or not self.login_password:
            yield rx.toast("Por favor ingresa usuario y contraseña.", duration=3000)
            return

        self.is_loading = True
        await asyncio.sleep(0.1)  # Para permitir mostrar el loading spinner

        repo = UsuarioRepository()
        usuario = repo.get_by_username(self.login_username)

        if usuario and bcrypt.checkpw(self.login_password.encode('utf-8'), usuario.hashed_password.encode('utf-8')):
            self.is_authenticated = True
            self.username = usuario.username
            self.role = usuario.role
            self.empresa = usuario.empresa
            self.is_loading = False

            yield rx.toast.success("Bienvenido!", duration=2000)
            yield rx.redirect("/dashboard")
        else:
            self.is_loading = False
            yield rx.toast.error("Credenciales incorrectas.", duration=3000)

    @rx.event
    async def register(self):

        logging.info("Entró al método register()")
        logging.info(f"Username recibido: {self.register_username}")
        logging.info(f"Password recibido: {self.register_password}")
        logging.info(f"Empresa recibida: {self.register_empresa}")

        if not self.register_username or not self.register_password:
            yield rx.toast.warning("Todos los campos son obligatorios.", duration=3000)
            return

        self.is_loading = True
        await asyncio.sleep(0.1)

        repo = UsuarioRepository()
        usuario_existente = repo.get_by_username(self.register_username)

        logging.info(f"🔎 Resultado de get_by_username: {usuario_existente}")

        if usuario_existente:
            self.is_loading = False
            yield rx.toast.warning(f"El usuario '{self.register_username}' ya existe.", duration=3000)
            return

        hashed = bcrypt.hashpw(self.register_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        nuevo_usuario = Usuario(
            username=self.register_username,
            hashed_password=hashed,
            role='usuario',
            empresa=self.register_empresa
        )
        success = repo.register(nuevo_usuario)

        self.is_loading = False
        if success:
            logging.info("Usuario registrado exitosamente")
            yield rx.toast.success("Registro exitoso. Inicia sesión.", duration=3000)
            yield rx.redirect("/login")
        else:
            logging.error("Error al registrar el usuario")
            yield rx.toast.error("Error en el registro.", duration=3000)


