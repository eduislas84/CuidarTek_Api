from database import db
import pymysql
from pymysql import Error

class LogAccesosModel:
    @staticmethod
    def create(log_data: dict):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                print("❌ No hay conexión para crear log")
                return None
                
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO log_accesos (id_usuario, accion, ip_origen) 
                VALUES (%s, %s, %s)""",
                (log_data['id_usuario'], log_data['accion'], log_data.get('ip_origen'))
            )
            connection.commit()
            log_id = cursor.lastrowid
            cursor.execute("SELECT * FROM log_accesos WHERE id_log = %s", (log_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error creando log: {e}")
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
            cursor.execute("SELECT * FROM log_accesos ORDER BY fecha_hora DESC")
            return cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo logs: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()

    @staticmethod
    def get_by_id(log_id: int):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return None
                
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM log_accesos WHERE id_log = %s", (log_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error obteniendo log por ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()

    @staticmethod
    def get_by_usuario_id(usuario_id: int):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return []
                
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM log_accesos WHERE id_usuario = %s ORDER BY fecha_hora DESC", (usuario_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo logs por usuario: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()

    @staticmethod
    def get_by_accion(accion: str):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return []
                
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM log_accesos WHERE accion = %s ORDER BY fecha_hora DESC", (accion,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error obteniendo logs por acción: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()

    @staticmethod
    def update(log_id: int, log_data: dict):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return None
                
            cursor = connection.cursor()
            
            update_fields = []
            values = []
            for field, value in log_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(log_id)
            query = f"UPDATE log_accesos SET {', '.join(update_fields)} WHERE id_log = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM log_accesos WHERE id_log = %s", (log_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error actualizando log: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()

    @staticmethod
    def delete(log_id: int):
        connection = db.get_connection()
        cursor = None
        try:
            if not connection or not connection.open:
                return False
                
            cursor = connection.cursor()
            cursor.execute("DELETE FROM log_accesos WHERE id_log = %s", (log_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error eliminando log: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection and connection.open:
                connection.close()