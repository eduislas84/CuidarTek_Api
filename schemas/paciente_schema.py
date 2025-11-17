from pydantic import BaseModel
from typing import Optional

class PacienteBase(BaseModel):
    edad: Optional[int] = None
    sexo: Optional[str] = None
    peso_actual: Optional[float] = None
    altura: Optional[float] = None
    enfermedades_cronicas: Optional[str] = None
    medicamentos: Optional[str] = None
    doctor_asignado: Optional[int] = None

class PacienteCreate(PacienteBase):
    id_usuario: int

class PacienteUpdate(BaseModel):
    edad: Optional[int] = None
    sexo: Optional[str] = None
    peso_actual: Optional[float] = None
    altura: Optional[float] = None
    enfermedades_cronicas: Optional[str] = None
    medicamentos: Optional[str] = None
    doctor_asignado: Optional[int] = None

class Paciente(PacienteBase):
    id_paciente: int
    id_usuario: int

    class Config:
        from_attributes = True
