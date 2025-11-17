
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class SesionesWearableBase(BaseModel):
    dispositivo: Optional[str] = None
    datos_recibidos: Optional[Dict[str, Any]] = None

class SesionesWearableCreate(SesionesWearableBase):
    id_paciente: int

class SesionesWearableUpdate(BaseModel):
    dispositivo: Optional[str] = None
    datos_recibidos: Optional[Dict[str, Any]] = None

class SesionesWearable(SesionesWearableBase):
    id_sesion: int
    id_paciente: int
    fecha_sincronizacion: datetime

    class Config:
        from_attributes = True