
from database import db
import pymysql
from pymysql import Error

class AlertasModel:
    @staticmethod
    def create(alerta_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO alertas (id_paciente, tipo_alerta, descripcion, fecha_programada, estatus) 
                VALUES (%s, %s, %s, %s, %s)""",
                (alerta_data['id_paciente'], alerta_data['tipo_alerta'], 
                 alerta_data['descripcion'], alerta_data['fecha_programada'],
                 alerta_data.get('estatus', 'pendiente'))
            )
            connection.commit()
            alerta_id = cursor.lastrowid
            cursor.execute("SELECT * FROM alertas WHERE id_alerta = %s", (alerta_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_all():
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alertas")
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(alerta_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alertas WHERE id_alerta = %s", (alerta_id,))
            return cursor.fetchone()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_paciente_id(paciente_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alertas WHERE id_paciente = %s ORDER BY fecha_programada", (paciente_id,))
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_pendientes():
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alertas WHERE estatus = 'pendiente' ORDER BY fecha_programada")
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def update(alerta_id: int, alerta_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            update_fields = []
            values = []
            for field, value in alerta_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(alerta_id)
            query = f"UPDATE alertas SET {', '.join(update_fields)} WHERE id_alerta = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM alertas WHERE id_alerta = %s", (alerta_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete(alerta_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM alertas WHERE id_alerta = %s", (alerta_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()