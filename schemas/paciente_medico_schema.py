from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PacienteMedicoBase(BaseModel):
    id_paciente: int
    id_medico: int
    notas: Optional[str] = None

class PacienteMedicoCreate(PacienteMedicoBase):
    pass

class PacienteMedicoUpdate(BaseModel):
    estatus: str
    notas: Optional[str] = None

class PacienteMedico(PacienteMedicoBase):
    id_relacion: int
    fecha_asignacion: datetime
    estatus: str
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True

class PacienteMedicoConNombres(PacienteMedico):
    nombre_medico: str
    correo_medico: Optional[str] = None
    especialidad: Optional[str] = None
    cedula_profesional: Optional[str] = None
    telefono_consultorio: Optional[str] = None

class SolicitudPendiente(BaseModel):
    id_relacion: int
    id_paciente: int
    id_usuario_paciente: int
    nombre_paciente: str
    correo_paciente: str
    edad: Optional[int] = None
    sexo: Optional[str] = None
    fecha_asignacion: datetime
    notas: Optional[str] = None

class PacienteConInfo(BaseModel):
    id_relacion: int
    id_paciente: int
    id_usuario_paciente: int
    nombre_paciente: str
    correo_paciente: str
    edad: Optional[int] = None
    sexo: Optional[str] = None
    peso_actual: Optional[float] = None
    altura: Optional[float] = None
    fecha_asignacion: datetime