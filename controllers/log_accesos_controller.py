from fastapi import APIRouter, HTTPException, Depends
from models.log_accesos_model import LogAccesosModel
from schemas.log_accesos_schema import LogAccesos, LogAccesosCreate, LogAccesosUpdate
from auth import require_admin, get_current_active_user
from typing import List

router = APIRouter(prefix="/log-accesos", tags=["log_accesos"])

@router.post("/", response_model=LogAccesos)
async def crear_log(
    log: LogAccesosCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Usuarios solo pueden crear logs para sí mismos
        if current_user["rol"] != "admin" and current_user["id_usuario"] != log.id_usuario:
            raise HTTPException(status_code=403, detail="No puede crear logs para otros usuarios")
        
        nuevo_log = LogAccesosModel.create(log.dict())
        if not nuevo_log:
            raise HTTPException(status_code=500, detail="Error al crear registro de log")
        return nuevo_log
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[LogAccesos], dependencies=[Depends(require_admin)])
async def listar_logs():
    try:
        logs = LogAccesosModel.get_all()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{log_id}", response_model=LogAccesos)
async def obtener_log(
    log_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        log = LogAccesosModel.get_by_id(log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Registro de log no encontrado")
        
        # Usuarios solo pueden ver sus propios logs, admin puede ver todo
        if current_user["rol"] != "admin" and current_user["id_usuario"] != log["id_usuario"]:
            raise HTTPException(status_code=403, detail="No tiene permisos para ver este registro")
        
        return log
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usuario/{usuario_id}", response_model=List[LogAccesos])
async def obtener_logs_por_usuario(
    usuario_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Usuarios solo pueden ver sus propios logs
        if current_user["rol"] != "admin" and current_user["id_usuario"] != usuario_id:
            raise HTTPException(status_code=403, detail="No tiene permisos para ver estos registros")
        
        logs = LogAccesosModel.get_by_usuario_id(usuario_id)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/accion/{accion}", response_model=List[LogAccesos], dependencies=[Depends(require_admin)])
async def obtener_logs_por_accion(accion: str):
    try:
        logs = LogAccesosModel.get_by_accion(accion)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{log_id}", response_model=LogAccesos, dependencies=[Depends(require_admin)])
async def actualizar_log(log_id: int, log: LogAccesosUpdate):
    try:
        log_existente = LogAccesosModel.get_by_id(log_id)
        if not log_existente:
            raise HTTPException(status_code=404, detail="Registro de log no encontrado")
        
        log_actualizado = LogAccesosModel.update(log_id, log.dict(exclude_unset=True))
        return log_actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{log_id}", dependencies=[Depends(require_admin)])
async def eliminar_log(log_id: int):
    try:
        log_existente = LogAccesosModel.get_by_id(log_id)
        if not log_existente:
            raise HTTPException(status_code=404, detail="Registro de log no encontrado")
        
        eliminado = LogAccesosModel.delete(log_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar registro de log")
        
        return {"message": "Registro de log eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))