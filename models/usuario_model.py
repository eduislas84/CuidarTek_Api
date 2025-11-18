from database import db
import pymysql
from pymysql import Error

class UsuarioModel:
    @staticmethod
    def create(usuario_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO usuario (nombre, correo, password, rol, estatus) VALUES (%s, %s, %s, %s, %s)",
                (usuario_data['nombre'], usuario_data['correo'], usuario_data['password'], 
                 usuario_data['rol'], usuario_data.get('estatus', 'Activo'))
            )
            connection.commit()
            user_id = cursor.lastrowid
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (user_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_all():
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario")
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(usuario_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (usuario_id,))
            return cursor.fetchone()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_email(correo: str):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
            return cursor.fetchone()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def update(usuario_id: int, usuario_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Construir la consulta dinámicamente
            update_fields = []
            values = []
            for field, value in usuario_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(usuario_id)
            query = f"UPDATE usuario SET {', '.join(update_fields)} WHERE id_usuario = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (usuario_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def delete(usuario_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (usuario_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def authenticate(correo: str, password: str):
        """Autenticar usuario con correo y contraseña"""
        from auth import auth_handler  # Importar aquí para evitar dependencia circular
        usuario = UsuarioModel.get_by_email(correo)
        if not usuario:
            return None
        
        if not auth_handler.verify_password(password, usuario["password"]):
            return None
        
        return usuario

    @staticmethod
    def change_password(usuario_id: int, new_password: str):
        """Cambiar contraseña de usuario"""
        from auth import auth_handler  # Importar aquí para evitar dependencia circular
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            hashed_password = auth_handler.get_password_hash(new_password)
            cursor.execute(
                "UPDATE usuario SET password = %s WHERE id_usuario = %s",
                (hashed_password, usuario_id)
            )
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()