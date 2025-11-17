
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportesMedicosBase(BaseModel):
    descripcion_general: Optional[str] = None
    diagnostico: Optional[str] = None
    recomendaciones_medicas: Optional[str] = None

class ReportesMedicosCreate(ReportesMedicosBase):
    id_paciente: int
    id_medico: int

class ReportesMedicosUpdate(BaseModel):
    descripcion_general: Optional[str] = None
    diagnostico: Optional[str] = None
    recomendaciones_medicas: Optional[str] = None

class ReportesMedicos(ReportesMedicosBase):
    id_reporte: int
    id_paciente: int
    id_medico: int
    fecha_reporte: datetime

    class Config:
        from_attributes = True