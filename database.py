import pymysql
from pymysql import Error
import os
from dotenv import load_dotenv
import ssl

load_dotenv()

class Database:
    def __init__(self):
        # No usar valores por defecto locales - forzar uso de variables de entorno
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.port = int(os.getenv("DB_PORT", "3306"))
        
        # Verificar que todas las variables críticas estén presentes
        self._check_environment_variables()

    def _check_environment_variables(self):
        """Verifica que todas las variables de entorno necesarias estén configuradas"""
        required_vars = {
            "DB_HOST": self.host,
            "DB_USER": self.user, 
            "DB_PASSWORD": self.password,
            "DB_NAME": self.database
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            print(f"⚠️  Variables de entorno faltantes: {', '.join(missing_vars)}")
            print("   Configúralas en Railway -> Variables")
        else:
            print("✅ Todas las variables de entorno están configuradas")

    def get_connection(self):
        try:
            # Verificar que tengamos todas las variables necesarias
            if not all([self.host, self.user, self.password, self.database]):
                print("❌ No se puede conectar: variables de BD incompletas")
                return None
            
            # Configuración SSL para Aiven
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            print(f"🔗 Intentando conectar a: {self.host}:{self.port}")
            
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor,
                ssl=ssl_context,  # SSL para Aiven
                connect_timeout=10,  # Timeout para conexiones cloud
                autocommit=True  # Asegurar autocommit para operaciones
            )
            
            print("✅ Conectado a Aiven MySQL exitosamente")
            return connection
            
        except Error as e:
            print(f"❌ Error conectando a Aiven MySQL: {e}")
            print(f"   Host: {self.host}")
            print(f"   Puerto: {self.port}")
            print(f"   Usuario: {self.user}")
            print(f"   Base de datos: {self.database}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return None

    def create_database_and_tables(self):
        """Crea la base de datos y las tablas si no existen"""
        connection = None
        try:
            print("🏗️  Iniciando creación de base de datos y tablas...")
            
            # Primero intentamos conectar directamente a la base de datos
            connection = self.get_connection()
            if not connection:
                print("❌ No se pudo conectar para crear tablas")
                return
            
            cursor = connection.cursor()
            
            # Verificar si la base de datos existe, si no, crearla
            cursor.execute("SELECT DATABASE() as current_db")
            current_db = cursor.fetchone()
            print(f"📊 Usando base de datos: {current_db['current_db']}")
            
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
            print("✅ Tabla 'usuario' creada/verificada")
            
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
            print("✅ Tabla 'paciente' creada/verificada")
            
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
            print("✅ Tabla 'indicadores_salud' creada/verificada")
            
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
            print("✅ Tabla 'alertas' creada/verificada")
            
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
            print("✅ Tabla 'recomendaciones' creada/verificada")
            
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
            print("✅ Tabla 'retos' creada/verificada")
            
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
            print("✅ Tabla 'citas_medicas' creada/verificada")
            
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
            print("✅ Tabla 'reportes_medicos' creada/verificada")
            
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
            print("✅ Tabla 'sesiones_wearable' creada/verificada")
            
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
            print("✅ Tabla 'log_accesos' creada/verificada")
            
            print("🎉 Base de datos y tablas creadas/verificadas exitosamente!")
            
        except Error as e:
            print(f"❌ Error creando base de datos y tablas: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()
                print("🔒 Conexión cerrada")

# Crear instancia global de la base de datos
db = Database()