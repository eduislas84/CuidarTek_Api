
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogAccesosBase(BaseModel):
    accion: str
    ip_origen: Optional[str] = None

class LogAccesosCreate(LogAccesosBase):
    id_usuario: int

class LogAccesosUpdate(BaseModel):
    accion: Optional[str] = None
    ip_origen: Optional[str] = None

class LogAccesos(LogAccesosBase):
    id_log: int
    id_usuario: int
    fecha_hora: datetime

    class Config:
        from_attributes = True