from fastapi import APIRouter, HTTPException, Depends
from models.retos_model import RetosModel
from models.paciente_model import PacienteModel
from schemas.retos_schema import Retos, RetosCreate, RetosUpdate
from auth import require_role, require_medico, get_current_active_user
from typing import List

router = APIRouter(prefix="/retos", tags=["retos"])

@router.post("/", response_model=Retos)
async def crear_reto(
    reto: RetosCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Médicos pueden crear retos para cualquier paciente, pacientes solo para sí mismos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != reto.id_paciente:
                raise HTTPException(status_code=403, detail="Solo puede crear retos para su propio perfil")
        
        nuevo_reto = RetosModel.create(reto.dict())
        if not nuevo_reto:
            raise HTTPException(status_code=500, detail="Error al crear reto")
        return nuevo_reto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Retos], dependencies=[Depends(require_medico)])
async def listar_retos():
    try:
        retos = RetosModel.get_all()
        return retos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/activos", response_model=List[Retos])
async def listar_retos_activos(current_user: dict = Depends(get_current_active_user)):
    try:
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if paciente:
                retos = RetosModel.get_by_paciente_id(paciente["id_paciente"])
                return [r for r in retos if r["progreso"] < 100]
            return []
        else:
            retos = RetosModel.get_activos()
            return retos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{reto_id}", response_model=Retos)
async def obtener_reto(
    reto_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        reto = RetosModel.get_by_id(reto_id)
        if not reto:
            raise HTTPException(status_code=404, detail="Reto no encontrado")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != reto["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver este reto")
        
        return reto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paciente/{paciente_id}", response_model=List[Retos])
async def obtener_retos_por_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != paciente_id:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver estos retos")
        
        retos = RetosModel.get_by_paciente_id(paciente_id)
        return retos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{reto_id}", response_model=Retos)
async def actualizar_reto(
    reto_id: int, 
    reto: RetosUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        reto_existente = RetosModel.get_by_id(reto_id)
        if not reto_existente:
            raise HTTPException(status_code=404, detail="Reto no encontrado")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != reto_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para actualizar este reto")
        
        reto_actualizado = RetosModel.update(reto_id, reto.dict(exclude_unset=True))
        return reto_actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{reto_id}")
async def eliminar_reto(
    reto_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        reto_existente = RetosModel.get_by_id(reto_id)
        if not reto_existente:
            raise HTTPException(status_code=404, detail="Reto no encontrado")
        
        # Solo médicos, admin o el propio paciente pueden eliminar
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != reto_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para eliminar este reto")
        
        eliminado = RetosModel.delete(reto_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar reto")
        
        return {"message": "Reto eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))