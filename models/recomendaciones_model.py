
from database import db
import pymysql
from pymysql import Error

class RecomendacionesModel:
    @staticmethod
    def create(recomendacion_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO recomendaciones (id_paciente, contenido, origen) 
                VALUES (%s, %s, %s)""",
                (recomendacion_data['id_paciente'], recomendacion_data['contenido'], 
                 recomendacion_data['origen'])
            )
            connection.commit()
            recomendacion_id = cursor.lastrowid
            cursor.execute("SELECT * FROM recomendaciones WHERE id_recomendacion = %s", (recomendacion_id,))
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
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM recomendaciones")
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(recomendacion_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM recomendaciones WHERE id_recomendacion = %s", (recomendacion_id,))
            return cursor.fetchone()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_paciente_id(paciente_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM recomendaciones WHERE id_paciente = %s ORDER BY fecha_generacion DESC", (paciente_id,))
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def update(recomendacion_id: int, recomendacion_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            
            update_fields = []
            values = []
            for field, value in recomendacion_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(recomendacion_id)
            query = f"UPDATE recomendaciones SET {', '.join(update_fields)} WHERE id_recomendacion = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM recomendaciones WHERE id_recomendacion = %s", (recomendacion_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def delete(recomendacion_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM recomendaciones WHERE id_recomendacion = %s", (recomendacion_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()