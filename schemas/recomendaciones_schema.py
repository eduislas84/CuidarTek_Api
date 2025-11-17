
from pydantic import BaseModel
from datetime import datetime

class RecomendacionesBase(BaseModel):
    contenido: str
    origen: str

class RecomendacionesCreate(RecomendacionesBase):
    id_paciente: int

class RecomendacionesUpdate(BaseModel):
    contenido: str = None
    origen: str = None

class Recomendaciones(RecomendacionesBase):
    id_recomendacion: int
    id_paciente: int
    fecha_generacion: datetime

    class Config:
        from_attributes = True