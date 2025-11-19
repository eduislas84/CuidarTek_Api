import pymysql
from pymysql import Error
from database import db

class UsuarioModel:
    
    @staticmethod
    def get_by_email(email: str):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return None
                
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuario WHERE correo = %s", (email,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error buscando usuario por email: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()

    @staticmethod
    def create(usuario_data: dict):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return None
                
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO usuario (nombre, correo, password, rol, estatus)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                usuario_data['nombre'],
                usuario_data['correo'], 
                usuario_data['password'],
                usuario_data['rol'],
                usuario_data.get('estatus', 'Activo')
            ))
            connection.commit()
            usuario_id = cursor.lastrowid
            
            # Obtener el usuario recién creado
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (usuario_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error creando usuario: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()

    @staticmethod
    def get_by_id(usuario_id: int):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return None
                
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (usuario_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error obteniendo usuario por ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()

    @staticmethod
    def update(usuario_id: int, usuario_data: dict):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return None
                
            cursor = connection.cursor()
            
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
            print(f"Error actualizando usuario: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()

    @staticmethod
    def get_all():
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return []
                
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuario ORDER BY fecha_registro DESC")
            return cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo usuarios: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()