import reflex as rx
from Entity.usuario import Usuario
from Data.admin_repository import AdminRepository

class AdminState(rx.State):
    usuarios: list[Usuario] = []
    message: str = ""

    @rx.event
    def load_usuarios(self):
        """Carga la lista de usuarios desde la base de datos."""
        repo = AdminRepository()
        self.usuarios = repo.listar_usuarios()
        print("🧪 Usuarios cargados desde DB:", self.usuarios)
        self.message = f"{len(self.usuarios)} usuarios cargados."

    @rx.event
    def actualizar_usuario(self, index: int, campo: str, valor: str):
        """Actualiza el campo 'role' o 'empresa' de un usuario en la lista."""
        usuario = self.usuarios[index]
        setattr(usuario, campo, valor)
        self.usuarios[index] = usuario  # Esto dispara la actualización visual

    @rx.event
    def guardar_cambios(self):
        """Guarda todos los cambios hechos a los usuarios en la base de datos."""
        repo = AdminRepository()
        success = repo.actualizar_usuario(self.usuarios)
        self.message = "Cambios guardados correctamente." if success else "Error al guardar cambios."
