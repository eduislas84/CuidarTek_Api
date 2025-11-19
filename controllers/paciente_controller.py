# paciente_controllers.py
from fastapi import APIRouter, HTTPException, Depends
from models.paciente_model import PacienteModel
from schemas.paciente_schema import Paciente, PacienteCreate, PacienteUpdate
from auth import get_current_active_user
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

@router.post("/", response_model=Paciente, status_code=201)
async def crear_paciente(
    paciente: PacienteCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Permitir que pacientes creen su propio perfil
        if current_user["rol"] == "paciente" and current_user["id_usuario"] != paciente.id_usuario:
            raise HTTPException(
                status_code=403,
                detail="Solo puedes crear tu propio perfil de paciente"
            )
        
        # Verificar si ya existe un perfil para este usuario
        paciente_existente = PacienteModel.get_by_usuario_id(paciente.id_usuario)
        if paciente_existente:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un perfil de paciente para este usuario"
            )

        # Convertir a dict y asegurar campos explícitos (incluir doctor_asignado si viene)
        paciente_dict = paciente.dict()
        nuevo_paciente = PacienteModel.create(paciente_dict)
        if not nuevo_paciente:
            raise HTTPException(status_code=500, detail="Error al crear paciente")
        return nuevo_paciente
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error en crear_paciente")
        raise HTTPException(status_code=500, detail="Error interno al crear paciente")

@router.get("/", response_model=List[Paciente])
async def listar_pacientes(current_user: dict = Depends(get_current_active_user)):
    try:
        if current_user["rol"] not in ["medico", "admin"]:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para listar pacientes"
            )
        
        pacientes = PacienteModel.get_all()
        return pacientes
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error en listar_pacientes")
        raise HTTPException(status_code=500, detail="Error interno al listar pacientes")

@router.get("/{paciente_id}", response_model=Paciente)
async def obtener_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        paciente = PacienteModel.get_by_id(paciente_id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        if current_user["rol"] == "paciente":
            paciente_del_usuario = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente_del_usuario or paciente_del_usuario.get("id_paciente") != paciente_id:
                raise HTTPException(
                    status_code=403,
                    detail="No tienes permisos para ver este paciente"
                )
        
        return paciente
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error en obtener_paciente")
        raise HTTPException(status_code=500, detail="Error interno al obtener paciente")

@router.get("/usuario/{usuario_id}", response_model=Paciente)
async def obtener_paciente_por_usuario(
    usuario_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        if current_user["rol"] == "paciente" and current_user["id_usuario"] != usuario_id:
            raise HTTPException(
                status_code=403,
                detail="Solo puedes ver tu propia información"
            )
        
        paciente = PacienteModel.get_by_usuario_id(usuario_id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado para este usuario")
        return paciente
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error en obtener_paciente_por_usuario")
        raise HTTPException(status_code=500, detail="Error interno al obtener paciente por usuario")

@router.put("/{paciente_id}", response_model=Paciente)
async def actualizar_paciente(
    paciente_id: int, 
    paciente: PacienteUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        paciente_existente = PacienteModel.get_by_id(paciente_id)
        if not paciente_existente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        if current_user["rol"] == "paciente":
            paciente_del_usuario = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente_del_usuario or paciente_del_usuario.get("id_paciente") != paciente_id:
                raise HTTPException(
                    status_code=403,
                    detail="Solo puedes actualizar tu propia información"
                )
        
        paciente_actualizado = PacienteModel.update(paciente_id, paciente.dict(exclude_unset=True))
        if not paciente_actualizado:
            raise HTTPException(status_code=500, detail="Error al actualizar paciente")
        return paciente_actualizado
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error en actualizar_paciente")
        raise HTTPException(status_code=500, detail="Error interno al actualizar paciente")

@router.delete("/{paciente_id}")
async def eliminar_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        if current_user["rol"] not in ["medico", "admin"]:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para eliminar pacientes"
            )
        
        paciente_existente = PacienteModel.get_by_id(paciente_id)
        if not paciente_existente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        eliminado = PacienteModel.delete(paciente_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar paciente")
        
        return {"message": "Paciente eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error en eliminar_paciente")
        raise HTTPException(status_code=500, detail="Error interno al eliminar paciente")
