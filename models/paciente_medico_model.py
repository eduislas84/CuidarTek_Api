from database import db
import pymysql
from pymysql import Error

class PacienteMedicoModel:
    @staticmethod
    def create_solicitud(solicitud_data: dict):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO paciente_medico 
                (id_paciente, id_medico, estatus, notas) 
                VALUES (%s, %s, %s, %s)""",
                (solicitud_data['id_paciente'], solicitud_data['id_medico'], 
                 'pendiente', solicitud_data.get('notas'))
            )
            connection.commit()
            relacion_id = cursor.lastrowid
            cursor.execute("SELECT * FROM paciente_medico WHERE id_relacion = %s", (relacion_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()



    @staticmethod
    def get_medicos_del_paciente(paciente_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT pm.*, um.nombre as nombre_medico, um.correo as correo_medico
                FROM paciente_medico pm
                JOIN usuario um ON pm.id_medico = um.id_usuario
                WHERE pm.id_paciente = %s AND pm.estatus = 'activo'
                ORDER BY pm.fecha_asignacion DESC
            """, (paciente_id,))
            return cursor.fetchall()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()


    @staticmethod
    def actualizar_estatus(relacion_id: int, nuevo_estatus: str, notas: str = None):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            
            if notas:
                cursor.execute(
                    "UPDATE paciente_medico SET estatus = %s, notas = %s WHERE id_relacion = %s",
                    (nuevo_estatus, notas, relacion_id)
                )
            else:
                cursor.execute(
                    "UPDATE paciente_medico SET estatus = %s WHERE id_relacion = %s",
                    (nuevo_estatus, relacion_id)
                )
            
            connection.commit()
            cursor.execute("SELECT * FROM paciente_medico WHERE id_relacion = %s", (relacion_id,))
            return cursor.fetchone()
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def verificar_relacion(paciente_id: int, medico_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM paciente_medico 
                WHERE id_paciente = %s AND id_medico = %s
            """, (paciente_id, medico_id))
            return cursor.fetchone()
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def delete(relacion_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM paciente_medico WHERE id_relacion = %s", (relacion_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()
                

    @staticmethod
    def get_medicos_del_paciente(paciente_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT pm.*, 
                    u.id_usuario,
                    u.nombre as nombre_medico, 
                    u.correo as correo_medico,
                    m.especialidad,
                    m.cedula_profesional,
                    m.telefono_consultorio
                FROM paciente_medico pm
                JOIN usuario u ON pm.id_medico = u.id_usuario
                LEFT JOIN medico m ON u.id_usuario = m.id_usuario
                WHERE pm.id_paciente = %s 
                AND pm.estatus = 'activo'
                ORDER BY pm.fecha_asignacion DESC
            """, (paciente_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Error en get_medicos_del_paciente: {str(e)}")
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_solicitudes_pendientes_medico(medico_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT pm.*, 
                    p.id_paciente,
                    p.id_usuario as id_usuario_paciente, 
                    u.nombre as nombre_paciente,
                    u.correo as correo_paciente, 
                    p.edad, 
                    p.sexo
                FROM paciente_medico pm
                JOIN paciente p ON pm.id_paciente = p.id_paciente
                JOIN usuario u ON p.id_usuario = u.id_usuario
                WHERE pm.id_medico = %s 
                AND pm.estatus = 'pendiente'
                ORDER BY pm.fecha_asignacion DESC
            """, (medico_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Error en get_solicitudes_pendientes_medico: {str(e)}")
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_pacientes_del_medico(medico_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT pm.*, 
                    p.id_paciente,
                    p.id_usuario as id_usuario_paciente, 
                    u.nombre as nombre_paciente,
                    u.correo as correo_paciente, 
                    p.edad, 
                    p.sexo, 
                    p.peso_actual, 
                    p.altura
                FROM paciente_medico pm
                JOIN paciente p ON pm.id_paciente = p.id_paciente
                JOIN usuario u ON p.id_usuario = u.id_usuario
                WHERE pm.id_medico = %s 
                AND pm.estatus = 'activo'
                ORDER BY pm.fecha_asignacion DESC
            """, (medico_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Error en get_pacientes_del_medico: {str(e)}")
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(relacion_id: int):
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT pm.*, 
                    p.id_usuario as id_usuario_paciente, 
                    u_paciente.nombre as nombre_paciente,
                    u_medico.nombre as nombre_medico,
                    m.especialidad
                FROM paciente_medico pm
                JOIN paciente p ON pm.id_paciente = p.id_paciente
                JOIN usuario u_paciente ON p.id_usuario = u_paciente.id_usuario
                JOIN usuario u_medico ON pm.id_medico = u_medico.id_usuario
                LEFT JOIN medico m ON u_medico.id_usuario = m.id_usuario
                WHERE pm.id_relacion = %s
            """, (relacion_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"❌ Error en get_by_id: {str(e)}")
            raise e
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()