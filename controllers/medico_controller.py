from fastapi import APIRouter, HTTPException, Depends
from models.medico_model import MedicoModel
from models.usuario_model import UsuarioModel
from schemas.medico_schema import Medico, MedicoCreate, MedicoUpdate, MedicoConUsuario, MedicoConPacientes
from auth import get_current_active_user, require_admin, require_medico
from typing import List

router = APIRouter(prefix="/medicos", tags=["medicos"])

@router.post("/", response_model=Medico, dependencies=[Depends(require_admin)])
async def crear_medico(medico: MedicoCreate):
    try:
        # Verificar que el usuario existe
        usuario = UsuarioModel.get_by_id(medico.id_usuario)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar que el usuario tiene rol médico
        if usuario["rol"] not in ["medico", "admin"]:
            raise HTTPException(status_code=400, detail="El usuario debe tener rol médico o admin")
        
        # Verificar que no existe ya un perfil médico
        medico_existente = MedicoModel.get_by_user_id(medico.id_usuario)
        if medico_existente:
            raise HTTPException(status_code=400, detail="El usuario ya tiene un perfil médico")
        
        nuevo_medico = MedicoModel.create(medico.dict())
        if not nuevo_medico:
            raise HTTPException(status_code=500, detail="Error al crear perfil médico")
        return nuevo_medico
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[MedicoConPacientes])
async def listar_medicos():
    try:
        medicos = MedicoModel.get_medicos_activos()
        return medicos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{medico_id}", response_model=MedicoConUsuario)
async def obtener_medico(medico_id: int):
    try:
        medico = MedicoModel.get_by_id(medico_id)
        if not medico:
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        return medico
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usuario/{usuario_id}", response_model=MedicoConUsuario)
async def obtener_medico_por_usuario(usuario_id: int):
    try:
        medico = MedicoModel.get_by_user_id(usuario_id)
        if not medico:
            raise HTTPException(status_code=404, detail="Perfil médico no encontrado")
        return medico
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{medico_id}", response_model=Medico)
async def actualizar_medico(
    medico_id: int, 
    medico: MedicoUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar que el médico existe
        medico_existente = MedicoModel.get_by_id(medico_id)
        if not medico_existente:
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        
        # Solo el propio médico o admin pueden actualizar
        if current_user["rol"] != "admin" and current_user["id_usuario"] != medico_existente["id_usuario"]:
            raise HTTPException(status_code=403, detail="No tiene permisos para actualizar este perfil")
        
        medico_actualizado = MedicoModel.update(medico_id, medico.dict(exclude_unset=True))
        return medico_actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{medico_id}", dependencies=[Depends(require_admin)])
async def eliminar_medico(medico_id: int):
    try:
        # Verificar que el médico existe
        medico_existente = MedicoModel.get_by_id(medico_id)
        if not medico_existente:
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        
        eliminado = MedicoModel.delete(medico_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar médico")
        
        return {"message": "Perfil médico eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))