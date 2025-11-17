
from pydantic import BaseModel
from datetime import date
from typing import Optional

class RetosBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    progreso: int = 0
    recompensa: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class RetosCreate(RetosBase):
    id_paciente: int

class RetosUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    progreso: Optional[int] = None
    recompensa: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class Retos(RetosBase):
    id_reto: int
    id_paciente: int

    class Config:
        from_attributes = True