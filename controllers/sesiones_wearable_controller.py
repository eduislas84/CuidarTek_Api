from fastapi import APIRouter, HTTPException, Depends
from models.sesiones_wearable_model import SesionesWearableModel
from models.paciente_model import PacienteModel
from schemas.sesiones_wearable_schema import SesionesWearable, SesionesWearableCreate, SesionesWearableUpdate
from auth import require_role, require_medico, get_current_active_user
from typing import List

router = APIRouter(prefix="/sesiones-wearable", tags=["sesiones_wearable"])

@router.post("/", response_model=SesionesWearable)
async def crear_sesion(
    sesion: SesionesWearableCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Pacientes solo pueden agregar sesiones a su propio perfil
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != sesion.id_paciente:
                raise HTTPException(status_code=403, detail="No puede agregar sesiones a otros pacientes")
        
        nueva_sesion = SesionesWearableModel.create(sesion.dict())
        if not nueva_sesion:
            raise HTTPException(status_code=500, detail="Error al crear sesión wearable")
        return nueva_sesion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[SesionesWearable], dependencies=[Depends(require_medico)])
async def listar_sesiones():
    try:
        sesiones = SesionesWearableModel.get_all()
        return sesiones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{sesion_id}", response_model=SesionesWearable)
async def obtener_sesion(
    sesion_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        sesion = SesionesWearableModel.get_by_id(sesion_id)
        if not sesion:
            raise HTTPException(status_code=404, detail="Sesión wearable no encontrada")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != sesion["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver esta sesión")
        
        return sesion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paciente/{paciente_id}", response_model=List[SesionesWearable])
async def obtener_sesiones_por_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != paciente_id:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver estas sesiones")
        
        sesiones = SesionesWearableModel.get_by_paciente_id(paciente_id)
        return sesiones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dispositivo/{dispositivo}", response_model=List[SesionesWearable], dependencies=[Depends(require_medico)])
async def obtener_sesiones_por_dispositivo(dispositivo: str):
    try:
        sesiones = SesionesWearableModel.get_by_dispositivo(dispositivo)
        return sesiones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{sesion_id}", response_model=SesionesWearable)
async def actualizar_sesion(
    sesion_id: int, 
    sesion: SesionesWearableUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        sesion_existente = SesionesWearableModel.get_by_id(sesion_id)
        if not sesion_existente:
            raise HTTPException(status_code=404, detail="Sesión wearable no encontrada")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != sesion_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para actualizar esta sesión")
        
        sesion_actualizada = SesionesWearableModel.update(sesion_id, sesion.dict(exclude_unset=True))
        return sesion_actualizada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{sesion_id}")
async def eliminar_sesion(
    sesion_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        sesion_existente = SesionesWearableModel.get_by_id(sesion_id)
        if not sesion_existente:
            raise HTTPException(status_code=404, detail="Sesión wearable no encontrada")
        
        # Solo médicos, admin o el propio paciente pueden eliminar
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != sesion_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para eliminar esta sesión")
        
        eliminado = SesionesWearableModel.delete(sesion_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar sesión wearable")
        
        return {"message": "Sesión wearable eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))