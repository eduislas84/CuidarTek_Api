from fastapi import APIRouter, HTTPException, Depends
from models.mensajes_model import MensajesModel
from schemas.mensajes_schema import Mensaje, MensajeCreate, MensajeUpdate, MensajeConNombres, ConversacionResponse
from auth import get_current_active_user, require_any_user
from typing import List

router = APIRouter(prefix="/mensajes", tags=["mensajes"])

@router.post("/", response_model=Mensaje)
async def enviar_mensaje(
    mensaje: MensajeCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar que el remitente sea el usuario actual
        if current_user["id_usuario"] != mensaje.id_remitente:
            raise HTTPException(status_code=403, detail="Solo puede enviar mensajes como usted mismo")
        
        # Verificar que no se envíe mensaje a sí mismo
        if mensaje.id_remitente == mensaje.id_destinatario:
            raise HTTPException(status_code=400, detail="No puede enviarse mensajes a sí mismo")
        
        nuevo_mensaje = MensajesModel.create(mensaje.dict())
        if not nuevo_mensaje:
            raise HTTPException(status_code=500, detail="Error al enviar mensaje")
        return nuevo_mensaje
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enviados", response_model=List[MensajeConNombres])
async def obtener_mensajes_enviados(
    current_user: dict = Depends(get_current_active_user)
):
    try:
        mensajes = MensajesModel.get_by_remitente(current_user["id_usuario"])
        return mensajes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recibidos", response_model=List[MensajeConNombres])
async def obtener_mensajes_recibidos(
    current_user: dict = Depends(get_current_active_user)
):
    try:
        mensajes = MensajesModel.get_by_destinatario(current_user["id_usuario"])
        return mensajes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversacion/{usuario2_id}", response_model=ConversacionResponse)
async def obtener_conversacion(
    usuario2_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        conversacion = MensajesModel.get_conversacion(current_user["id_usuario"], usuario2_id)
        return ConversacionResponse(
            conversacion=conversacion,
            usuario1_id=current_user["id_usuario"],
            usuario2_id=usuario2_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{mensaje_id}", response_model=MensajeConNombres)
async def obtener_mensaje(
    mensaje_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        mensaje = MensajesModel.get_by_id(mensaje_id)
        if not mensaje:
            raise HTTPException(status_code=404, detail="Mensaje no encontrado")
        
        # Solo el remitente o destinatario pueden ver el mensaje
        if (current_user["id_usuario"] != mensaje["id_remitente"] and 
            current_user["id_usuario"] != mensaje["id_destinatario"]):
            raise HTTPException(status_code=403, detail="No tiene permisos para ver este mensaje")
        
        # Si es el destinatario, marcar como leído
        if current_user["id_usuario"] == mensaje["id_destinatario"] and not mensaje["leido"]:
            mensaje = MensajesModel.marcar_como_leido(mensaje_id)
        
        return mensaje
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{mensaje_id}/leer", response_model=Mensaje)
async def marcar_mensaje_como_leido(
    mensaje_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        mensaje = MensajesModel.get_by_id(mensaje_id)
        if not mensaje:
            raise HTTPException(status_code=404, detail="Mensaje no encontrado")
        
        # Solo el destinatario puede marcar como leído
        if current_user["id_usuario"] != mensaje["id_destinatario"]:
            raise HTTPException(status_code=403, detail="Solo el destinatario puede marcar el mensaje como leído")
        
        mensaje_actualizado = MensajesModel.marcar_como_leido(mensaje_id)
        return mensaje_actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{mensaje_id}", response_model=Mensaje)
async def actualizar_mensaje(
    mensaje_id: int,
    mensaje_update: MensajeUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        mensaje = MensajesModel.get_by_id(mensaje_id)
        if not mensaje:
            raise HTTPException(status_code=404, detail="Mensaje no encontrado")
        
        # Solo el remitente puede editar el mensaje
        if current_user["id_usuario"] != mensaje["id_remitente"]:
            raise HTTPException(status_code=403, detail="Solo el remitente puede editar el mensaje")
        
        # No permitir editar si ya fue leído
        if mensaje["leido"]:
            raise HTTPException(status_code=400, detail="No se puede editar un mensaje ya leído")
        
        mensaje_actualizado = MensajesModel.update(mensaje_id, mensaje_update.dict(exclude_unset=True))
        return mensaje_actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{mensaje_id}")
async def eliminar_mensaje(
    mensaje_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        mensaje = MensajesModel.get_by_id(mensaje_id)
        if not mensaje:
            raise HTTPException(status_code=404, detail="Mensaje no encontrado")
        
        # Solo el remitente puede eliminar el mensaje
        if current_user["id_usuario"] != mensaje["id_remitente"]:
            raise HTTPException(status_code=403, detail="Solo el remitente puede eliminar el mensaje")
        
        eliminado = MensajesModel.delete(mensaje_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar mensaje")
        
        return {"message": "Mensaje eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))