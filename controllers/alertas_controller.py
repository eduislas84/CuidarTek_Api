from fastapi import APIRouter, HTTPException, Depends
from models.alertas_model import AlertasModel
from models.paciente_model import PacienteModel
from schemas.alertas_schema import Alertas, AlertasCreate, AlertasUpdate
from auth import get_current_active_user
from typing import List

router = APIRouter(prefix="/alertas", tags=["alertas"])

@router.post("/", response_model=Alertas)
async def crear_alerta(
    alerta: AlertasCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos según el rol
        if current_user["rol"] == "paciente":
            # Pacientes solo pueden crear alertas para sí mismos
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != alerta.id_paciente:
                raise HTTPException(
                    status_code=403, 
                    detail="Solo puedes crear alertas para tu propio perfil"
                )
        
        # Médicos y admin pueden crear alertas para cualquier paciente
        # No necesitan verificación adicional
        
        nueva_alerta = AlertasModel.create(alerta.dict())
        if not nueva_alerta:
            raise HTTPException(status_code=500, detail="Error al crear alerta")
        return nueva_alerta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Alertas])
async def listar_alertas(current_user: dict = Depends(get_current_active_user)):
    try:
        # Solo médicos y admin pueden ver todas las alertas
        if current_user["rol"] not in ["medico", "admin"]:
            raise HTTPException(
                status_code=403, 
                detail="No tiene permisos para listar todas las alertas"
            )
        
        alertas = AlertasModel.get_all()
        return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pendientes/", response_model=List[Alertas])
async def listar_alertas_pendientes(current_user: dict = Depends(get_current_active_user)):
    try:
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if paciente:
                alertas = AlertasModel.get_by_paciente_id(paciente["id_paciente"])
                return [a for a in alertas if a["estatus"] == "pendiente"]
            return []
        else:
            # Médicos y admin ven todas las alertas pendientes
            alertas = AlertasModel.get_pendientes()
            return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{alerta_id}", response_model=Alertas)
async def obtener_alerta(
    alerta_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        alerta = AlertasModel.get_by_id(alerta_id)
        if not alerta:
            raise HTTPException(status_code=404, detail="Alerta no encontrada")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != alerta["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver esta alerta")
        
        return alerta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paciente/{paciente_id}", response_model=List[Alertas])
async def obtener_alertas_por_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != paciente_id:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver estas alertas")
        
        # Médicos pueden ver alertas de cualquier paciente
        # Admin puede ver todas las alertas
        
        alertas = AlertasModel.get_by_paciente_id(paciente_id)
        return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{alerta_id}", response_model=Alertas)
async def actualizar_alerta(
    alerta_id: int, 
    alerta: AlertasUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        alerta_existente = AlertasModel.get_by_id(alerta_id)
        if not alerta_existente:
            raise HTTPException(status_code=404, detail="Alerta no encontrada")
        
        # Solo médicos, admin o el paciente dueño pueden actualizar
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != alerta_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para actualizar esta alerta")
        
        alerta_actualizada = AlertasModel.update(alerta_id, alerta.dict(exclude_unset=True))
        return alerta_actualizada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{alerta_id}")
async def eliminar_alerta(
    alerta_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        alerta_existente = AlertasModel.get_by_id(alerta_id)
        if not alerta_existente:
            raise HTTPException(status_code=404, detail="Alerta no encontrada")
        
        # Solo médicos, admin o el paciente dueño pueden eliminar
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != alerta_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para eliminar esta alerta")
        
        eliminado = AlertasModel.delete(alerta_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar alerta")
        
        return {"message": "Alerta eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))