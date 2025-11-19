
from database import db
import pymysql
from pymysql import Error

class IndicadoresSaludModel:
    @staticmethod
    def create(indicador_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO indicadores_salud (id_paciente, presion_sistolica, presion_diastolica, 
                glucosa, peso, frecuencia_cardiaca, estado_animo, actividad_fisica, fuente_dato) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (indicador_data['id_paciente'], indicador_data.get('presion_sistolica'),
                 indicador_data.get('presion_diastolica'), indicador_data.get('glucosa'),
                 indicador_data.get('peso'), indicador_data.get('frecuencia_cardiaca'),
                 indicador_data.get('estado_animo'), indicador_data.get('actividad_fisica'),
                 indicador_data.get('fuente_dato', 'manual'))
            )
            connection.commit()
            indicador_id = cursor.lastrowid
            cursor.execute("SELECT * FROM indicadores_salud WHERE id_indicador = %s", (indicador_id,))
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
            cursor.execute("SELECT * FROM indicadores_salud")
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(indicador_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM indicadores_salud WHERE id_indicador = %s", (indicador_id,))
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
            cursor.execute("SELECT * FROM indicadores_salud WHERE id_paciente = %s ORDER BY fecha_registro DESC", (paciente_id,))
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def update(indicador_id: int, indicador_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            update_fields = []
            values = []
            for field, value in indicador_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(indicador_id)
            query = f"UPDATE indicadores_salud SET {', '.join(update_fields)} WHERE id_indicador = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM indicadores_salud WHERE id_indicador = %s", (indicador_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def delete(indicador_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM indicadores_salud WHERE id_indicador = %s", (indicador_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()