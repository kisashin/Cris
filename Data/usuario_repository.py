from config import get_db_connection
from Entity.usuario import Usuario

class UsuarioRepository:
    def __init__(self):
        self.connection = get_db_connection()

    def get_by_username(self, username):
        cursor = self.connection.cursor()
        try:
            cursor.execute("{CALL spConsultarUsuario (?)}", username)
            row = cursor.fetchone()
            if row:
                return Usuario(username=row[1], hashed_password=row[2], role=row[3], empresa=row[4], id_usuario=row[0])
            print("Usuario encontrado", row)
        except Exception as e:
            print("Error al obtener usuario:", e)
        return None

    def register(self, usuario: Usuario):
        cursor = self.connection.cursor()
        try:
            cursor.execute("{CALL sp_register_usuario (?, ?, ?, ?)}", usuario.username, usuario.hashed_password, usuario.role, usuario.empresa)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error en registro:", e)
            self.connection.rollback()
            return False

    def update(self, usuario: Usuario):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "{CALL sp_update_usuario (?, ?, ?, ?, ?)}",
                usuario.id_usuario,
                usuario.username,
                usuario.hashed_password,
                usuario.role,
                usuario.empresa  # 👈 añadimos empresa
            )
            self.connection.commit()
            return True
        except Exception as e:
            print("Error al actualizar:", e)
            self.connection.rollback()
            return False

    def delete(self, id_usuario: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute("{CALL sp_delete_usuario (?)}", id_usuario)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error al eliminar usuario:", e)
            self.connection.rollback()
            return False

    def list_all(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("{CALL sp_list_usuarios}")
            rows = cursor.fetchall()
            return [
                Usuario(
                    id_usuario=row[0],
                    username=row[1],
                    hashed_password=row[2],
                    role=row[3],
                    empresa=row[4]  # 👈 añadimos empresa
                )
                for row in rows
            ]
        except Exception as e:
            print("Error al listar usuarios:", e)
            return []