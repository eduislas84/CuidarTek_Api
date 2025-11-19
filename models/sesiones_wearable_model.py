
from database import db
import pymysql
from pymysql import Error
import json

class SesionesWearableModel:
    @staticmethod
    def create(sesion_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Convertir datos_recibidos a JSON si existe
            datos_recibidos = sesion_data.get('datos_recibidos')
            if datos_recibidos:
                datos_recibidos = json.dumps(datos_recibidos)
            
            cursor.execute(
                """INSERT INTO sesiones_wearable (id_paciente, dispositivo, datos_recibidos) 
                VALUES (%s, %s, %s)""",
                (sesion_data['id_paciente'], sesion_data.get('dispositivo'), datos_recibidos)
            )
            connection.commit()
            sesion_id = cursor.lastrowid
            cursor.execute("SELECT * FROM sesiones_wearable WHERE id_sesion = %s", (sesion_id,))
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
            cursor.execute("SELECT * FROM sesiones_wearable")
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(sesion_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sesiones_wearable WHERE id_sesion = %s", (sesion_id,))
            return cursor.fetchone()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_paciente_id(paciente_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sesiones_wearable WHERE id_paciente = %s ORDER BY fecha_sincronizacion DESC", (paciente_id,))
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_dispositivo(dispositivo: str):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sesiones_wearable WHERE dispositivo = %s ORDER BY fecha_sincronizacion DESC", (dispositivo,))
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def update(sesion_id: int, sesion_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Convertir datos_recibidos a JSON si existe
            if 'datos_recibidos' in sesion_data and sesion_data['datos_recibidos'] is not None:
                sesion_data['datos_recibidos'] = json.dumps(sesion_data['datos_recibidos'])
            
            update_fields = []
            values = []
            for field, value in sesion_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(sesion_id)
            query = f"UPDATE sesiones_wearable SET {', '.join(update_fields)} WHERE id_sesion = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM sesiones_wearable WHERE id_sesion = %s", (sesion_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def delete(sesion_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM sesiones_wearable WHERE id_sesion = %s", (sesion_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()