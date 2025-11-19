from fastapi import APIRouter, HTTPException, Depends
from models.paciente_model import PacienteModel
from schemas.paciente_schema import Paciente, PacienteCreate, PacienteUpdate
from auth import require_role, require_any_user, get_current_active_user
from typing import List

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

@router.post("/", response_model=Paciente)
async def crear_paciente(
    paciente: PacienteCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # ✅ PERMITIR que pacientes creen su propio perfil
        # Verificar que el usuario esté creando su propio perfil
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
        
        nuevo_paciente = PacienteModel.create(paciente.dict())
        if not nuevo_paciente:
            raise HTTPException(status_code=500, detail="Error al crear paciente")
        return nuevo_paciente
    except Exception as e:
        if "detail" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Paciente], dependencies=[Depends(require_role(["medico", "admin"]))])
async def listar_pacientes():
    try:
        pacientes = PacienteModel.get_all()
        return pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{paciente_id}", response_model=Paciente)
async def obtener_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        paciente = PacienteModel.get_by_id(paciente_id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        # ✅ PERMITIR que pacientes vean su propia información
        if current_user["rol"] == "paciente":
            # Verificar que el paciente esté viendo su propia información
            paciente_del_usuario = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente_del_usuario or paciente_del_usuario["id_paciente"] != paciente_id:
                raise HTTPException(
                    status_code=403,
                    detail="No tienes permisos para ver este paciente"
                )
        
        return paciente
    except Exception as e:
        if "detail" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usuario/{usuario_id}", response_model=Paciente)
async def obtener_paciente_por_usuario(
    usuario_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # ✅ PERMITIR que usuarios vean su propia información
        if current_user["rol"] == "paciente" and current_user["id_usuario"] != usuario_id:
            raise HTTPException(
                status_code=403,
                detail="Solo puedes ver tu propia información"
            )
        
        paciente = PacienteModel.get_by_usuario_id(usuario_id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado para este usuario")
        return paciente
    except Exception as e:
        if "detail" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{paciente_id}", response_model=Paciente)
async def actualizar_paciente(
    paciente_id: int, 
    paciente: PacienteUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar si el paciente existe
        paciente_existente = PacienteModel.get_by_id(paciente_id)
        if not paciente_existente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        # ✅ PERMITIR que pacientes actualicen su propia información
        if current_user["rol"] == "paciente":
            # Verificar que el paciente esté actualizando su propia información
            paciente_del_usuario = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente_del_usuario or paciente_del_usuario["id_paciente"] != paciente_id:
                raise HTTPException(
                    status_code=403,
                    detail="Solo puedes actualizar tu propia información"
                )
        
        paciente_actualizado = PacienteModel.update(paciente_id, paciente.dict(exclude_unset=True))
        return paciente_actualizado
    except Exception as e:
        if "detail" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{paciente_id}", dependencies=[Depends(require_role(["medico", "admin"]))])
async def eliminar_paciente(paciente_id: int):
    try:
        paciente_existente = PacienteModel.get_by_id(paciente_id)
        if not paciente_existente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        eliminado = PacienteModel.delete(paciente_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar paciente")
        
        return {"message": "Paciente eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))