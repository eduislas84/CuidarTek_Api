from .auth_controller import router as auth_router
from .usuario_controller import router as usuario_router
from .paciente_controller import router as paciente_router
from .indicadores_salud_controller import router as indicadores_salud_router
from .alertas_controller import router as alertas_router
from .recomendaciones_controller import router as recomendaciones_router
from .retos_controller import router as retos_router
from .citas_medicas_controller import router as citas_medicas_router
from .reportes_medicos_controller import router as reportes_medicos_router
from .sesiones_wearable_controller import router as sesiones_wearable_router
from .log_accesos_controller import router as log_accesos_router

__all__ = [
    'auth_router',
    'usuario_router',
    'paciente_router',
    'indicadores_salud_router',
    'alertas_router',
    'recomendaciones_router',
    'retos_router',
    'citas_medicas_router',
    'reportes_medicos_router',
    'sesiones_wearable_router',
    'log_accesos_router'
]