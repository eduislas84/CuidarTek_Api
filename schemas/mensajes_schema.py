from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MensajeBase(BaseModel):
    id_remitente: int
    id_destinatario: int
    asunto: Optional[str] = None
    contenido: str

class MensajeCreate(MensajeBase):
    pass

class MensajeUpdate(BaseModel):
    asunto: Optional[str] = None
    contenido: Optional[str] = None

class Mensaje(MensajeBase):
    id_mensaje: int
    fecha_envio: datetime
    leido: bool
    fecha_leido: Optional[datetime] = None

    class Config:
        from_attributes = True

class MensajeConNombres(Mensaje):
    nombre_remitente: str
    nombre_destinatario: str

class ConversacionResponse(BaseModel):
    conversacion: list[MensajeConNombres]
    usuario1_id: int
    usuario2_id: int