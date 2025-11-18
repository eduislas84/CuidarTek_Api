from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MedicoBase(BaseModel):
    especialidad: str
    cedula_profesional: Optional[str] = None
    telefono_consultorio: Optional[str] = None
    direccion_consultorio: Optional[str] = None
    horario_consultorio: Optional[str] = None
    anos_experiencia: Optional[int] = None
    universidad: Optional[str] = None

class MedicoCreate(MedicoBase):
    id_usuario: int

class MedicoUpdate(BaseModel):
    especialidad: Optional[str] = None
    cedula_profesional: Optional[str] = None
    telefono_consultorio: Optional[str] = None
    direccion_consultorio: Optional[str] = None
    horario_consultorio: Optional[str] = None
    anos_experiencia: Optional[int] = None
    universidad: Optional[str] = None
    estatus: Optional[str] = None

class Medico(MedicoBase):
    id_medico: int
    id_usuario: int
    estatus: str
    fecha_registro: datetime

    class Config:
        from_attributes = True

class MedicoConUsuario(Medico):
    nombre: str
    correo: str
    rol: str

class MedicoConPacientes(MedicoConUsuario):
    total_pacientes: int