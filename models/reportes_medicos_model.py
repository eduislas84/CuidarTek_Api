
from database import db
from mysql.connector import Error

class ReportesMedicosModel:
    @staticmethod
    def create(reporte_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO reportes_medicos (id_paciente, id_medico, descripcion_general, diagnostico, recomendaciones_medicas) 
                VALUES (%s, %s, %s, %s, %s)""",
                (reporte_data['id_paciente'], reporte_data['id_medico'],
                 reporte_data.get('descripcion_general'), reporte_data.get('diagnostico'),
                 reporte_data.get('recomendaciones_medicas'))
            )
            connection.commit()
            reporte_id = cursor.lastrowid
            cursor.execute("SELECT * FROM reportes_medicos WHERE id_reporte = %s", (reporte_id,))
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
            cursor.execute("SELECT * FROM reportes_medicos")
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(reporte_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM reportes_medicos WHERE id_reporte = %s", (reporte_id,))
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
            cursor.execute("SELECT * FROM reportes_medicos WHERE id_paciente = %s ORDER BY fecha_reporte DESC", (paciente_id,))
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_medico_id(medico_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM reportes_medicos WHERE id_medico = %s ORDER BY fecha_reporte DESC", (medico_id,))
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def update(reporte_id: int, reporte_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            update_fields = []
            values = []
            for field, value in reporte_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(reporte_id)
            query = f"UPDATE reportes_medicos SET {', '.join(update_fields)} WHERE id_reporte = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM reportes_medicos WHERE id_reporte = %s", (reporte_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete(reporte_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM reportes_medicos WHERE id_reporte = %s", (reporte_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()