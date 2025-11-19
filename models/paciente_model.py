# paciente_models.py
from database import db
import pymysql
from pymysql import Error
import logging

logger = logging.getLogger(__name__)

class PacienteModel:
    @staticmethod
    def create(paciente_data: dict):
        """
        Inserta un paciente. Construye la query dinámicamente para evitar errores
        si faltan campos opcionales. Usa DictCursor para devolver diccionarios.
        """
        connection = db.get_connection()
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Filtrar campos permitidos y preparar query dinámica
            allowed_fields = [
                "id_usuario", "edad", "sexo", "peso_actual", "altura",
                "enfermedades_cronicas", "medicamentos", "doctor_asignado"
            ]
            columns = []
            placeholders = []
            values = []

            for field in allowed_fields:
                # solo incluir si viene en dict (incluso si es None) -> esto permitirá insertar NULL
                if field in paciente_data:
                    columns.append(field)
                    placeholders.append("%s")
                    values.append(paciente_data.get(field))

            if not columns:
                raise ValueError("No se proporcionaron campos para crear el paciente")

            query = f"INSERT INTO paciente ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            cursor.execute(query, tuple(values))
            connection.commit()
            paciente_id = cursor.lastrowid

            cursor.execute("SELECT * FROM paciente WHERE id_paciente = %s", (paciente_id,))
            result = cursor.fetchone()
            return result
        except Error as e:
            # Loguear y re-lanzar para que el controlador pueda devolver un HTTPException con detalle
            logger.exception("Error en PacienteModel.create")
            raise e
        finally:
            try:
                if connection and connection.open:
                    cursor.close()
                    connection.close()
            except Exception:
                pass

    @staticmethod
    def get_all():
        connection = db.get_connection()
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM paciente")
            return cursor.fetchall()
        finally:
            try:
                if connection and connection.open:
                    cursor.close()
                    connection.close()
            except Exception:
                pass

    @staticmethod
    def get_by_id(paciente_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM paciente WHERE id_paciente = %s", (paciente_id,))
            return cursor.fetchone()
        finally:
            try:
                if connection and connection.open:
                    cursor.close()
                    connection.close()
            except Exception:
                pass

    @staticmethod
    def get_by_usuario_id(usuario_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM paciente WHERE id_usuario = %s", (usuario_id,))
            return cursor.fetchone()
        finally:
            try:
                if connection and connection.open:
                    cursor.close()
                    connection.close()
            except Exception:
                pass

    @staticmethod
    def update(paciente_id: int, paciente_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            update_fields = []
            values = []
            for field, value in paciente_data.items():
                # Solo actualizar campos que explícitamente se envían (permitir falsy como 0)
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)

            if not update_fields:
                # Nada que actualizar, devolver el registro actual
                cursor.execute("SELECT * FROM paciente WHERE id_paciente = %s", (paciente_id,))
                return cursor.fetchone()

            values.append(paciente_id)
            query = f"UPDATE paciente SET {', '.join(update_fields)} WHERE id_paciente = %s"

            cursor.execute(query, tuple(values))
            connection.commit()

            cursor.execute("SELECT * FROM paciente WHERE id_paciente = %s", (paciente_id,))
            return cursor.fetchone()
        except Error as e:
            logger.exception("Error en PacienteModel.update")
            raise e
        finally:
            try:
                if connection and connection.open:
                    cursor.close()
                    connection.close()
            except Exception:
                pass

    @staticmethod
    def delete(paciente_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM paciente WHERE id_paciente = %s", (paciente_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.exception("Error en PacienteModel.delete")
            raise e
        finally:
            try:
                if connection and connection.open:
                    cursor.close()
                    connection.close()
            except Exception:
                pass
