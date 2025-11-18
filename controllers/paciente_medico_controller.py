from fastapi import APIRouter, HTTPException, Depends
from models.paciente_medico_model import PacienteMedicoModel
from models.paciente_model import PacienteModel
from models.usuario_model import UsuarioModel
from models.medico_model import MedicoModel
from schemas.paciente_medico_schema import (
    PacienteMedico, PacienteMedicoCreate, PacienteMedicoUpdate,
    PacienteMedicoConNombres, SolicitudPendiente, PacienteConInfo
)
from auth import get_current_active_user, require_medico, require_paciente
from typing import List

router = APIRouter(prefix="/paciente-medico", tags=["paciente-medico"])

@router.post("/solicitud", response_model=PacienteMedico)
async def crear_solicitud(
    solicitud: PacienteMedicoCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        print(f"📥 Recibiendo solicitud: {solicitud.dict()}")
        
        # Verificar que el usuario actual es un paciente
        if current_user["rol"] != "paciente":
            raise HTTPException(status_code=403, detail="Solo los pacientes pueden crear solicitudes")
        
        # Obtener el id_paciente del usuario actual - USAR get_by_usuario_id (no get_by_user_id)
        paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
        if not paciente:
            raise HTTPException(status_code=404, detail="Perfil de paciente no encontrado")
        
        print(f"👤 Paciente encontrado: {paciente}")
        
        # Verificar que el médico existe y tiene perfil médico
        medico_perfil = MedicoModel.get_by_user_id(solicitud.id_medico)
        if not medico_perfil:
            raise HTTPException(status_code=404, detail="Perfil médico no encontrado")
        
        print(f"👨‍⚕️ Perfil médico encontrado: {medico_perfil}")
        
        # Verificar que el usuario médico existe y es médico
        medico_usuario = UsuarioModel.get_by_id(solicitud.id_medico)
        if not medico_usuario or medico_usuario["rol"] not in ["medico", "admin"]:
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        
        print(f"👨‍⚕️ Usuario médico encontrado: {medico_usuario}")
        
        # Verificar que no existe ya una relación
        relacion_existente = PacienteMedicoModel.verificar_relacion(paciente["id_paciente"], solicitud.id_medico)
        if relacion_existente:
            raise HTTPException(status_code=400, detail="Ya existe una solicitud con este médico")
        
        # Crear la solicitud
        solicitud_data = {
            "id_paciente": paciente["id_paciente"],
            "id_medico": solicitud.id_medico,  # id_usuario del médico
            "notas": solicitud.notas
        }
        
        print(f"📤 Creando solicitud con datos: {solicitud_data}")
        
        nueva_solicitud = PacienteMedicoModel.create_solicitud(solicitud_data)
        
        if not nueva_solicitud:
            raise HTTPException(status_code=500, detail="Error al crear solicitud")
            
        print(f"✅ Solicitud creada exitosamente: {nueva_solicitud}")
        return nueva_solicitud
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en crear_solicitud: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/solicitudes-pendientes", response_model=List[SolicitudPendiente])
async def obtener_solicitudes_pendientes(
    current_user: dict = Depends(require_medico)
):
    try:
        solicitudes = PacienteMedicoModel.get_solicitudes_pendientes_medico(current_user["id_usuario"])
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mis-medicos", response_model=List[PacienteMedicoConNombres])
async def obtener_mis_medicos(
    current_user: dict = Depends(require_paciente)
):
    try:
        # USAR get_by_usuario_id aquí también
        paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
        if not paciente:
            raise HTTPException(status_code=404, detail="Perfil de paciente no encontrado")
        
        medicos = PacienteMedicoModel.get_medicos_del_paciente(paciente["id_paciente"])
        return medicos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mis-pacientes", response_model=List[PacienteConInfo])
async def obtener_mis_pacientes(
    current_user: dict = Depends(require_medico)
):
    try:
        pacientes = PacienteMedicoModel.get_pacientes_del_medico(current_user["id_usuario"])
        return pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{relacion_id}", response_model=PacienteMedico)
async def actualizar_solicitud(
    relacion_id: int,
    actualizacion: PacienteMedicoUpdate,
    current_user: dict = Depends(require_medico)
):
    try:
        # Verificar que la relación existe y pertenece al médico
        relacion = PacienteMedicoModel.get_by_id(relacion_id)
        if not relacion:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        if relacion["id_medico"] != current_user["id_usuario"]:
            raise HTTPException(status_code=403, detail="No tiene permisos para actualizar esta solicitud")
        
        # Actualizar el estatus
        relacion_actualizada = PacienteMedicoModel.actualizar_estatus(
            relacion_id, actualizacion.estatus, actualizacion.notas
        )
        return relacion_actualizada
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{relacion_id}")
async def eliminar_solicitud(
    relacion_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        relacion = PacienteMedicoModel.get_by_id(relacion_id)
        if not relacion:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        # Solo el paciente o el médico pueden eliminar la relación
        # USAR get_by_usuario_id aquí también
        paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
        puede_eliminar = (
            (paciente and paciente["id_paciente"] == relacion["id_paciente"]) or
            current_user["id_usuario"] == relacion["id_medico"]
        )
        
        if not puede_eliminar:
            raise HTTPException(status_code=403, detail="No tiene permisos para eliminar esta solicitud")
        
        eliminado = PacienteMedicoModel.delete(relacion_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar solicitud")
        
        return {"message": "Solicitud eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))