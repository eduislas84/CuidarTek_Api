
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlertasBase(BaseModel):
    tipo_alerta: str
    descripcion: str
    fecha_programada: datetime
    estatus: str = "pendiente"

class AlertasCreate(AlertasBase):
    id_paciente: int

class AlertasUpdate(BaseModel):
    tipo_alerta: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_programada: Optional[datetime] = None
    estatus: Optional[str] = None

class Alertas(AlertasBase):
    id_alerta: int
    id_paciente: int

    class Config:
        from_attributes = True