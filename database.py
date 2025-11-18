import pymysql
from pymysql import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "12345")
        self.database = os.getenv("DB_NAME", "cuidartek_db")
        self.port = int(os.getenv("DB_PORT", "3306"))  # Convertir a int aquí

    def get_connection(self):
        try:
            connection = pymysql.connect(  # ✅ Cambiado a pymysql.connect
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor  # ✅ Agregar esto para obtener diccionarios
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def create_database_and_tables(self):
        """Crea la base de datos y las tablas si no existen"""
        connection = None
        try:
            # Primero conectamos sin especificar base de datos para crearla
            connection = pymysql.connect(  # ✅ Cambiado a pymysql.connect
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cursor = connection.cursor()
            
            # Crear base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # Crear tabla Usuario
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    correo VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    rol ENUM('paciente', 'medico', 'admin') NOT NULL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    estatus ENUM('Activo', 'Inactivo') DEFAULT 'Activo'
                )
            """)
            
            # Crear tabla Paciente
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS paciente (
                    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
                    id_usuario INT NOT NULL,
                    edad INT,
                    sexo ENUM('Masculino', 'Femenino', 'Otro'),
                    peso_actual DECIMAL(5,2),
                    altura DECIMAL(4,2),
                    enfermedades_cronicas TEXT,
                    medicamentos TEXT,
                    doctor_asignado INT,
                    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
                    FOREIGN KEY (doctor_asignado) REFERENCES usuario(id_usuario) ON DELETE SET NULL
                )
            """)
            
            # Crear tabla Indicadores_Salud
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS indicadores_salud (
                    id_indicador INT AUTO_INCREMENT PRIMARY KEY,
                    id_paciente INT NOT NULL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    presion_sistolica INT,
                    presion_diastolica INT,
                    glucosa DECIMAL(5,2),
                    peso DECIMAL(5,2),
                    frecuencia_cardiaca INT,
                    estado_animo VARCHAR(100),
                    actividad_fisica VARCHAR(100),
                    fuente_dato ENUM('manual', 'wearable') DEFAULT 'manual',
                    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE
                )
            """)
            
            # Crear tabla Alertas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alertas (
                    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
                    id_paciente INT NOT NULL,
                    tipo_alerta ENUM('medicación', 'cita', 'actividad', 'agua') NOT NULL,
                    descripcion TEXT NOT NULL,
                    fecha_programada DATETIME NOT NULL,
                    estatus ENUM('pendiente', 'completada', 'omitida') DEFAULT 'pendiente',
                    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE
                )
            """)
            
            # Crear tabla Recomendaciones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recomendaciones (
                    id_recomendacion INT AUTO_INCREMENT PRIMARY KEY,
                    id_paciente INT NOT NULL,
                    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    contenido TEXT NOT NULL,
                    origen ENUM('IA', 'médico') NOT NULL,
                    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE
                )
            """)
            
            # Crear tabla Retos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS retos (
                    id_reto INT AUTO_INCREMENT PRIMARY KEY,
                    id_paciente INT NOT NULL,
                    titulo VARCHAR(255) NOT NULL,
                    descripcion TEXT,
                    progreso INT DEFAULT 0 CHECK (progreso >= 0 AND progreso <= 100),
                    recompensa VARCHAR(255),
                    fecha_inicio DATE,
                    fecha_fin DATE,
                    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE
                )
            """)
            
            # Crear tabla Citas_Medicas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS citas_medicas (
                    id_cita INT AUTO_INCREMENT PRIMARY KEY,
                    id_paciente INT NOT NULL,
                    id_medico INT NOT NULL,
                    fecha_cita DATETIME NOT NULL,
                    motivo TEXT,
                    observaciones TEXT,
                    estatus ENUM('programada', 'completada', 'cancelada') DEFAULT 'programada',
                    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE,
                    FOREIGN KEY (id_medico) REFERENCES usuario(id_usuario) ON DELETE CASCADE
                )
            """)
            
            # Crear tabla Reportes_Medicos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reportes_medicos (
                    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
                    id_paciente INT NOT NULL,
                    id_medico INT NOT NULL,
                    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    descripcion_general TEXT,
                    diagnostico TEXT,
                    recomendaciones_medicas TEXT,
                    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE,
                    FOREIGN KEY (id_medico) REFERENCES usuario(id_usuario) ON DELETE CASCADE
                )
            """)
            
            # Crear tabla Sesiones_Wearable
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sesiones_wearable (
                    id_sesion INT AUTO_INCREMENT PRIMARY KEY,
                    id_paciente INT NOT NULL,
                    dispositivo VARCHAR(255),
                    fecha_sincronizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    datos_recibidos JSON,
                    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE
                )
            """)
            
            # Crear tabla Log_Accesos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS log_accesos (
                    id_log INT AUTO_INCREMENT PRIMARY KEY,
                    id_usuario INT NOT NULL,
                    accion ENUM('inicio_sesion', 'actualización_datos', 'eliminación', 'exportación') NOT NULL,
                    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_origen VARCHAR(45),
                    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
                )
            """)
            
            connection.commit()
            print("Base de datos y tablas creadas exitosamente!")
            
        except Error as e:
            print(f"Error creating database and tables: {e}")
        finally:
            if connection and connection.open:  # ✅ Cambiado a connection.open
                cursor.close()
                connection.close()

# Crear instancia global de la base de datos
db = Database()