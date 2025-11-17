from fastapi import APIRouter, HTTPException, Depends
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import Usuario, UsuarioCreate, UsuarioUpdate
from auth import require_role, require_admin, get_current_active_user
from typing import List

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=Usuario, dependencies=[Depends(require_admin)])
async def crear_usuario(usuario: UsuarioCreate):
    try:
        # Verificar si el correo ya existe
        usuario_existente = UsuarioModel.get_by_email(usuario.correo)
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        
        nuevo_usuario = UsuarioModel.create(usuario.dict())
        if not nuevo_usuario:
            raise HTTPException(status_code=500, detail="Error al crear usuario")
        return nuevo_usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Usuario], dependencies=[Depends(require_admin)])
async def listar_usuarios():
    try:
        usuarios = UsuarioModel.get_all()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{usuario_id}", response_model=Usuario)
async def obtener_usuario(
    usuario_id: int, 
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Usuarios solo pueden ver su propia información, admin puede ver todo
        if current_user["rol"] != "admin" and current_user["id_usuario"] != usuario_id:
            raise HTTPException(status_code=403, detail="No tiene permisos para ver este usuario")
        
        usuario = UsuarioModel.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{usuario_id}", response_model=Usuario)
async def actualizar_usuario(
    usuario_id: int, 
    usuario: UsuarioUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Usuarios solo pueden actualizar su propia información, admin puede actualizar todo
        if current_user["rol"] != "admin" and current_user["id_usuario"] != usuario_id:
            raise HTTPException(status_code=403, detail="No tiene permisos para actualizar este usuario")
        
        # Verificar si el usuario existe
        usuario_existente = UsuarioModel.get_by_id(usuario_id)
        if not usuario_existente:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar usuario
        usuario_actualizado = UsuarioModel.update(usuario_id, usuario.dict(exclude_unset=True))
        return usuario_actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{usuario_id}", dependencies=[Depends(require_admin)])
async def eliminar_usuario(usuario_id: int):
    try:
        # Verificar si el usuario existe
        usuario_existente = UsuarioModel.get_by_id(usuario_id)
        if not usuario_existente:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        eliminado = UsuarioModel.delete(usuario_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar usuario")
        
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))