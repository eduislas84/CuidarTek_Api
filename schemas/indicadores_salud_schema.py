
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IndicadoresSaludBase(BaseModel):
    presion_sistolica: Optional[int] = None
    presion_diastolica: Optional[int] = None
    glucosa: Optional[float] = None
    peso: Optional[float] = None
    frecuencia_cardiaca: Optional[int] = None
    estado_animo: Optional[str] = None
    actividad_fisica: Optional[str] = None
    fuente_dato: str = "manual"

class IndicadoresSaludCreate(IndicadoresSaludBase):
    id_paciente: int

class IndicadoresSaludUpdate(BaseModel):
    presion_sistolica: Optional[int] = None
    presion_diastolica: Optional[int] = None
    glucosa: Optional[float] = None
    peso: Optional[float] = None
    frecuencia_cardiaca: Optional[int] = None
    estado_animo: Optional[str] = None
    actividad_fisica: Optional[str] = None
    fuente_dato: Optional[str] = None

class IndicadoresSalud(IndicadoresSaludBase):
    id_indicador: int
    id_paciente: int
    fecha_registro: datetime

    class Config:
        from_attributes = True