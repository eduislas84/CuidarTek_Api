
from database import db
import pymysql
from pymysql import Error

class RetosModel:
    @staticmethod
    def create(reto_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO retos (id_paciente, titulo, descripcion, progreso, recompensa, fecha_inicio, fecha_fin) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (reto_data['id_paciente'], reto_data['titulo'], reto_data.get('descripcion'),
                 reto_data.get('progreso', 0), reto_data.get('recompensa'),
                 reto_data.get('fecha_inicio'), reto_data.get('fecha_fin'))
            )
            connection.commit()
            reto_id = cursor.lastrowid
            cursor.execute("SELECT * FROM retos WHERE id_reto = %s", (reto_id,))
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
            cursor.execute("SELECT * FROM retos")
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(reto_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM retos WHERE id_reto = %s", (reto_id,))
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
            cursor.execute("SELECT * FROM retos WHERE id_paciente = %s", (paciente_id,))
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_activos():
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM retos WHERE progreso < 100 AND (fecha_fin IS NULL OR fecha_fin >= CURDATE())")
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def update(reto_id: int, reto_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            update_fields = []
            values = []
            for field, value in reto_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(reto_id)
            query = f"UPDATE retos SET {', '.join(update_fields)} WHERE id_reto = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM retos WHERE id_reto = %s", (reto_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def delete(reto_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM retos WHERE id_reto = %s", (reto_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()