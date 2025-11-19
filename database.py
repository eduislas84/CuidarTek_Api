def create_database_and_tables(self):
    """Crea las tablas en la base de datos defaultdb de Aiven"""
    connection = None
    try:
        print("🏗️  Iniciando creación de tablas en defaultdb...")
        
        connection = self.get_connection()
        if not connection:
            print("❌ No se pudo conectar a la base de datos")
            return
        
        cursor = connection.cursor()
        
        # Verificar conexión
        cursor.execute("SELECT DATABASE() as current_db, NOW() as server_time")
        db_info = cursor.fetchone()
        print(f"📊 Conectado a: {db_info['current_db']}")
        print(f"⏰ Hora del servidor: {db_info['server_time']}")
        
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

        # ✅ CORREGIDO DEFINITIVAMENTE: Eliminar y recrear log_accesos
        cursor.execute("DROP TABLE IF EXISTS log_accesos")
        print("🗑️  Tabla 'log_accesos' eliminada (si existía)")
        
        cursor.execute("""
            CREATE TABLE log_accesos (
                id_log INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL,
                accion VARCHAR(50) NOT NULL,
                fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_origen VARCHAR(45),
                FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
            )
        """)
        print("✅ Tabla 'log_accesos' creada con VARCHAR")

        # Crear tabla Mensajes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id_mensaje INT AUTO_INCREMENT PRIMARY KEY,
                id_remitente INT NOT NULL,
                id_destinatario INT NOT NULL,
                asunto VARCHAR(255),
                contenido TEXT NOT NULL,
                fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                leido BOOLEAN DEFAULT FALSE,
                fecha_leido TIMESTAMP NULL,
                FOREIGN KEY (id_remitente) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
                FOREIGN KEY (id_destinatario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
            )
        """)
        print("✅ Tabla 'mensajes' creada/verificada")
        
        # Crear tabla Paciente_Medico (relaciones)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paciente_medico (
                id_relacion INT AUTO_INCREMENT PRIMARY KEY,
                id_paciente INT NOT NULL,
                id_medico INT NOT NULL,
                fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estatus ENUM('pendiente', 'activo', 'rechazado', 'finalizado') DEFAULT 'pendiente',
                notas TEXT,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_paciente_medico (id_paciente, id_medico),
                FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE,
                FOREIGN KEY (id_medico) REFERENCES usuario(id_usuario) ON DELETE CASCADE
            )
        """)
        print("✅ Tabla 'paciente_medico' creada/verificada")
        
        # Crear tabla Medico (perfil médico)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medico (
                id_medico INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL,
                especialidad VARCHAR(255),
                cedula_profesional VARCHAR(50) UNIQUE,
                telefono_consultorio VARCHAR(20),
                direccion_consultorio TEXT,
                horario_consultorio TEXT,
                anos_experiencia INT,
                universidad VARCHAR(255),
                estatus ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
            )
        """)
        print("✅ Tabla 'medico' creada/verificada")
        
        print("🎉 ¡Todas las tablas creadas exitosamente en Aiven!")
        
    except Error as e:
        print(f"❌ Error creando tablas: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        if connection and connection.open:
            cursor.close()
            connection.close()
            print("🔒 Conexión cerrada")