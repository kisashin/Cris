from config import get_db_connection
from Entity.usuario import Usuario

class AdminRepository:
    def __init__(self):
        self.connection = get_db_connection()

    def listar_usuarios(self):
        cursor = self.connection.cursor()
        usuarios = []
        try:
            cursor.execute("{CALL sp_list_usuarios}")
            rows = cursor.fetchall()
            for row in rows:
                usuario = Usuario(
                    id_usuario=row[0],
                    username=row[1],
                    hashed_password=row[2],
                    role=row[3],
                    empresa=row[4]
                )
                usuarios.append(usuario)
        except Exception as e:
            print("Error al listar usuarios:", e)
        return usuarios

    def actualizar_usuario(self, usuario: Usuario):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "{CALL sp_update_usuario (?, ?, ?, ?, ?)}",
                usuario.id_usuario,
                usuario.username,
                usuario.hashed_password,
                usuario.role,
                usuario.empresa
            )
            self.connection.commit()
            return True
        except Exception as e:
            print("Error al actualizar usuario:", e)
            self.connection.rollback()
            return False
