
from database import db
import pymysql
from pymysql import Error

class CitasMedicasModel:
    @staticmethod
    def create(cita_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO citas_medicas (id_paciente, id_medico, fecha_cita, motivo, observaciones, estatus) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (cita_data['id_paciente'], cita_data['id_medico'], cita_data['fecha_cita'],
                 cita_data.get('motivo'), cita_data.get('observaciones'),
                 cita_data.get('estatus', 'programada'))
            )
            connection.commit()
            cita_id = cursor.lastrowid
            cursor.execute("SELECT * FROM citas_medicas WHERE id_cita = %s", (cita_id,))
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
            cursor.execute("SELECT * FROM citas_medicas")
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(cita_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM citas_medicas WHERE id_cita = %s", (cita_id,))
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
            cursor.execute("SELECT * FROM citas_medicas WHERE id_paciente = %s ORDER BY fecha_cita", (paciente_id,))
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_medico_id(medico_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM citas_medicas WHERE id_medico = %s ORDER BY fecha_cita", (medico_id,))
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_programadas():
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM citas_medicas WHERE estatus = 'programada' ORDER BY fecha_cita")
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def update(cita_id: int, cita_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            update_fields = []
            values = []
            for field, value in cita_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(cita_id)
            query = f"UPDATE citas_medicas SET {', '.join(update_fields)} WHERE id_cita = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM citas_medicas WHERE id_cita = %s", (cita_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def delete(cita_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM citas_medicas WHERE id_cita = %s", (cita_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()