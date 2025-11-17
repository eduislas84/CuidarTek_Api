
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CitasMedicasBase(BaseModel):
    fecha_cita: datetime
    motivo: Optional[str] = None
    observaciones: Optional[str] = None
    estatus: str = "programada"

class CitasMedicasCreate(CitasMedicasBase):
    id_paciente: int
    id_medico: int

class CitasMedicasUpdate(BaseModel):
    fecha_cita: Optional[datetime] = None
    motivo: Optional[str] = None
    observaciones: Optional[str] = None
    estatus: Optional[str] = None

class CitasMedicas(CitasMedicasBase):
    id_cita: int
    id_paciente: int
    id_medico: int

    class Config:
        from_attributes = True