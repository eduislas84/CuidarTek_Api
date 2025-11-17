from fastapi import APIRouter, HTTPException, Depends
from models.recomendaciones_model import RecomendacionesModel
from models.paciente_model import PacienteModel
from schemas.recomendaciones_schema import Recomendaciones, RecomendacionesCreate, RecomendacionesUpdate
from auth import get_current_active_user
from typing import List

router = APIRouter(prefix="/recomendaciones", tags=["recomendaciones"])

@router.post("/", response_model=Recomendaciones)
async def crear_recomendacion(
    recomendacion: RecomendacionesCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos según el rol
        if current_user["rol"] == "paciente":
            # Pacientes solo pueden crear recomendaciones para sí mismos
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != recomendacion.id_paciente:
                raise HTTPException(
                    status_code=403, 
                    detail="Solo puedes crear recomendaciones para tu propio perfil"
                )
        
        # Médicos y admin pueden crear recomendaciones para cualquier paciente
        # No necesitan verificación adicional
        
        nueva_recomendacion = RecomendacionesModel.create(recomendacion.dict())
        if not nueva_recomendacion:
            raise HTTPException(status_code=500, detail="Error al crear recomendación")
        return nueva_recomendacion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Recomendaciones])
async def listar_recomendaciones(current_user: dict = Depends(get_current_active_user)):
    try:
        # Solo médicos y admin pueden ver todas las recomendaciones
        if current_user["rol"] not in ["medico", "admin"]:
            raise HTTPException(
                status_code=403, 
                detail="No tiene permisos para listar todas las recomendaciones"
            )
        
        recomendaciones = RecomendacionesModel.get_all()
        return recomendaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{recomendacion_id}", response_model=Recomendaciones)
async def obtener_recomendacion(
    recomendacion_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        recomendacion = RecomendacionesModel.get_by_id(recomendacion_id)
        if not recomendacion:
            raise HTTPException(status_code=404, detail="Recomendación no encontrada")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != recomendacion["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver esta recomendación")
        
        return recomendacion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paciente/{paciente_id}", response_model=List[Recomendaciones])
async def obtener_recomendaciones_por_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != paciente_id:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver estas recomendaciones")
        
        # Médicos pueden ver recomendaciones de cualquier paciente
        # Admin puede ver todas las recomendaciones
        
        recomendaciones = RecomendacionesModel.get_by_paciente_id(paciente_id)
        return recomendaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{recomendacion_id}", response_model=Recomendaciones)
async def actualizar_recomendacion(
    recomendacion_id: int, 
    recomendacion: RecomendacionesUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        recomendacion_existente = RecomendacionesModel.get_by_id(recomendacion_id)
        if not recomendacion_existente:
            raise HTTPException(status_code=404, detail="Recomendación no encontrada")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != recomendacion_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para actualizar esta recomendación")
        
        recomendacion_actualizada = RecomendacionesModel.update(recomendacion_id, recomendacion.dict(exclude_unset=True))
        return recomendacion_actualizada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{recomendacion_id}")
async def eliminar_recomendacion(
    recomendacion_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        recomendacion_existente = RecomendacionesModel.get_by_id(recomendacion_id)
        if not recomendacion_existente:
            raise HTTPException(status_code=404, detail="Recomendación no encontrada")
        
        # Solo médicos, admin o el paciente dueño pueden eliminar
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != recomendacion_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para eliminar esta recomendación")
        
        eliminado = RecomendacionesModel.delete(recomendacion_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar recomendación")
        
        return {"message": "Recomendación eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))