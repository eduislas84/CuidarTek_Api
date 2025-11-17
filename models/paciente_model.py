
from database import db
from mysql.connector import Error

class PacienteModel:
    @staticmethod
    def create(paciente_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """INSERT INTO paciente (id_usuario, edad, sexo, peso_actual, altura, 
                enfermedades_cronicas, medicamentos, doctor_asignado) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (paciente_data['id_usuario'], paciente_data.get('edad'), paciente_data.get('sexo'),
                 paciente_data.get('peso_actual'), paciente_data.get('altura'),
                 paciente_data.get('enfermedades_cronicas'), paciente_data.get('medicamentos'),
                 paciente_data.get('doctor_asignado'))
            )
            connection.commit()
            paciente_id = cursor.lastrowid
            cursor.execute("SELECT * FROM paciente WHERE id_paciente = %s", (paciente_id,))
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
            cursor.execute("SELECT * FROM paciente")
            return cursor.fetchall()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(paciente_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM paciente WHERE id_paciente = %s", (paciente_id,))
            return cursor.fetchone()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_usuario_id(usuario_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM paciente WHERE id_usuario = %s", (usuario_id,))
            return cursor.fetchone()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def update(paciente_id: int, paciente_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            
            update_fields = []
            values = []
            for field, value in paciente_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(paciente_id)
            query = f"UPDATE paciente SET {', '.join(update_fields)} WHERE id_paciente = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM paciente WHERE id_paciente = %s", (paciente_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete(paciente_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM paciente WHERE id_paciente = %s", (paciente_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()