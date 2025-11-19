from database import db
import pymysql
from pymysql import Error

class MedicoModel:
    @staticmethod
    def create(medico_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO medico 
                (id_usuario, especialidad, cedula_profesional, telefono_consultorio, 
                 direccion_consultorio, horario_consultorio, anos_experiencia, universidad, estatus) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (medico_data['id_usuario'], medico_data['especialidad'], 
                 medico_data.get('cedula_profesional'), medico_data.get('telefono_consultorio'),
                 medico_data.get('direccion_consultorio'), medico_data.get('horario_consultorio'),
                 medico_data.get('anos_experiencia'), medico_data.get('universidad'),
                 medico_data.get('estatus', 'Activo'))
            )
            connection.commit()
            medico_id = cursor.lastrowid
            cursor.execute("SELECT * FROM medico WHERE id_medico = %s", (medico_id,))
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
            cursor.execute("""
                SELECT m.*, u.nombre, u.correo, u.rol
                FROM medico m
                JOIN usuario u ON m.id_usuario = u.id_usuario
                WHERE u.estatus = 'Activo' AND m.estatus = 'Activo'
            """)
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(medico_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT m.*, u.nombre, u.correo, u.rol
                FROM medico m
                JOIN usuario u ON m.id_usuario = u.id_usuario
                WHERE m.id_medico = %s
            """, (medico_id,))
            return cursor.fetchone()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_user_id(usuario_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT m.*, u.nombre, u.correo, u.rol
                FROM medico m
                JOIN usuario u ON m.id_usuario = u.id_usuario
                WHERE m.id_usuario = %s
            """, (usuario_id,))
            return cursor.fetchone()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_medicos_activos():
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT m.*, u.nombre, u.correo, u.rol,
                       (SELECT COUNT(*) FROM paciente_medico pm 
                        WHERE pm.id_medico = m.id_usuario AND pm.estatus = 'activo') as total_pacientes
                FROM medico m
                JOIN usuario u ON m.id_usuario = u.id_usuario
                WHERE u.estatus = 'Activo' AND m.estatus = 'Activo'
            """)
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def update(medico_id: int, medico_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            
            update_fields = []
            values = []
            for field, value in medico_data.items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
            
            values.append(medico_id)
            query = f"UPDATE medico SET {', '.join(update_fields)} WHERE id_medico = %s"
            
            cursor.execute(query, values)
            connection.commit()
            
            cursor.execute("SELECT * FROM medico WHERE id_medico = %s", (medico_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def delete(medico_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM medico WHERE id_medico = %s", (medico_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()