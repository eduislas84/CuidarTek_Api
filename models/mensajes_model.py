from database import db
import pymysql
from pymysql import Error

class MensajesModel:
    @staticmethod
    def create(mensaje_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO mensajes 
                (id_remitente, id_destinatario, asunto, contenido) 
                VALUES (%s, %s, %s, %s)""",
                (mensaje_data['id_remitente'], mensaje_data['id_destinatario'], 
                 mensaje_data.get('asunto'), mensaje_data['contenido'])
            )
            connection.commit()
            mensaje_id = cursor.lastrowid
            cursor.execute("SELECT * FROM mensajes WHERE id_mensaje = %s", (mensaje_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(mensaje_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM mensajes WHERE id_mensaje = %s", (mensaje_id,))
            return cursor.fetchone()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_remitente(usuario_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT m.*, u1.nombre as nombre_remitente, u2.nombre as nombre_destinatario
                FROM mensajes m
                JOIN usuario u1 ON m.id_remitente = u1.id_usuario
                JOIN usuario u2 ON m.id_destinatario = u2.id_usuario
                WHERE m.id_remitente = %s
                ORDER BY m.fecha_envio DESC
            """, (usuario_id,))
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_destinatario(usuario_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT m.*, u1.nombre as nombre_remitente, u2.nombre as nombre_destinatario
                FROM mensajes m
                JOIN usuario u1 ON m.id_remitente = u1.id_usuario
                JOIN usuario u2 ON m.id_destinatario = u2.id_usuario
                WHERE m.id_destinatario = %s
                ORDER BY m.fecha_envio DESC
            """, (usuario_id,))
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_conversacion(usuario1_id: int, usuario2_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT m.*, u1.nombre as nombre_remitente, u2.nombre as nombre_destinatario
                FROM mensajes m
                JOIN usuario u1 ON m.id_remitente = u1.id_usuario
                JOIN usuario u2 ON m.id_destinatario = u2.id_usuario
                WHERE (m.id_remitente = %s AND m.id_destinatario = %s)
                   OR (m.id_remitente = %s AND m.id_destinatario = %s)
                ORDER BY m.fecha_envio ASC
            """, (usuario1_id, usuario2_id, usuario2_id, usuario1_id))
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def marcar_como_leido(mensaje_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "UPDATE mensajes SET leido = TRUE, fecha_leido = CURRENT_TIMESTAMP WHERE id_mensaje = %s",
                (mensaje_id,)
            )
            connection.commit()
            cursor.execute("SELECT * FROM mensajes WHERE id_mensaje = %s", (mensaje_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def update(mensaje_id: int, mensaje_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            update_fields = []
            values = []
            for field, value in mensaje_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(mensaje_id)
            query = f"UPDATE mensajes SET {', '.join(update_fields)} WHERE id_mensaje = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM mensajes WHERE id_mensaje = %s", (mensaje_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete(mensaje_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM mensajes WHERE id_mensaje = %s", (mensaje_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()