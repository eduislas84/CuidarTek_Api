
from .usuario_schema import Usuario, UsuarioCreate, UsuarioUpdate
from .paciente_schema import Paciente, PacienteCreate, PacienteUpdate
from .indicadores_salud_schema import IndicadoresSalud, IndicadoresSaludCreate, IndicadoresSaludUpdate
from .alertas_schema import Alertas, AlertasCreate, AlertasUpdate
from .recomendaciones_schema import Recomendaciones, RecomendacionesCreate, RecomendacionesUpdate
from .retos_schema import Retos, RetosCreate, RetosUpdate
from .citas_medicas_schema import CitasMedicas, CitasMedicasCreate, CitasMedicasUpdate
from .reportes_medicos_schema import ReportesMedicos, ReportesMedicosCreate, ReportesMedicosUpdate
from .sesiones_wearable_schema import SesionesWearable, SesionesWearableCreate, SesionesWearableUpdate
from .log_accesos_schema import LogAccesos, LogAccesosCreate, LogAccesosUpdate
from .mensajes_schema import Mensaje, MensajeCreate, MensajeUpdate, MensajeConNombres, ConversacionResponse
from .paciente_medico_schema import (
    PacienteMedico, PacienteMedicoCreate, PacienteMedicoUpdate,
    PacienteMedicoConNombres, SolicitudPendiente, PacienteConInfo
)
from .medico_schema import Medico, MedicoCreate, MedicoUpdate, MedicoConUsuario, MedicoConPacientes

__all__ = [
    'Usuario', 'UsuarioCreate', 'UsuarioUpdate',
    'Paciente', 'PacienteCreate', 'PacienteUpdate',
    'IndicadoresSalud', 'IndicadoresSaludCreate', 'IndicadoresSaludUpdate',
    'Alertas', 'AlertasCreate', 'AlertasUpdate',
    'Recomendaciones', 'RecomendacionesCreate', 'RecomendacionesUpdate',
    'Retos', 'RetosCreate', 'RetosUpdate',
    'CitasMedicas', 'CitasMedicasCreate', 'CitasMedicasUpdate',
    'ReportesMedicos', 'ReportesMedicosCreate', 'ReportesMedicosUpdate',
    'SesionesWearable', 'SesionesWearableCreate', 'SesionesWearableUpdate',
    'LogAccesos', 'LogAccesosCreate', 'LogAccesosUpdate',
    'Mensaje', 'MensajeCreate', 'MensajeUpdate', 'MensajeConNombres', 'ConversacionResponse',
    
    'PacienteMedico', 'PacienteMedicoCreate', 'PacienteMedicoUpdate',
    'PacienteMedicoConNombres', 'SolicitudPendiente', 'PacienteConInfo',
    'Medico', 'MedicoCreate', 'MedicoUpdate', 'MedicoConUsuario', 'MedicoConPacientes'

]