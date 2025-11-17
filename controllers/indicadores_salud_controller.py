from fastapi import APIRouter, HTTPException, Depends
from models.indicadores_salud_model import IndicadoresSaludModel
from models.paciente_model import PacienteModel
from schemas.indicadores_salud_schema import IndicadoresSalud, IndicadoresSaludCreate, IndicadoresSaludUpdate
from auth import require_role, require_any_user, get_current_active_user
from typing import List

router = APIRouter(prefix="/indicadores-salud", tags=["indicadores_salud"])

@router.post("/", response_model=IndicadoresSalud)
async def crear_indicador(
    indicador: IndicadoresSaludCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Pacientes solo pueden agregar indicadores a su propio perfil
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != indicador.id_paciente:
                raise HTTPException(status_code=403, detail="No puede agregar indicadores a otros pacientes")
        
        nuevo_indicador = IndicadoresSaludModel.create(indicador.dict())
        if not nuevo_indicador:
            raise HTTPException(status_code=500, detail="Error al crear indicador de salud")
        return nuevo_indicador
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[IndicadoresSalud], dependencies=[Depends(require_role(["medico", "admin"]))])
async def listar_indicadores():
    try:
        indicadores = IndicadoresSaludModel.get_all()
        return indicadores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{indicador_id}", response_model=IndicadoresSalud)
async def obtener_indicador(
    indicador_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        indicador = IndicadoresSaludModel.get_by_id(indicador_id)
        if not indicador:
            raise HTTPException(status_code=404, detail="Indicador de salud no encontrado")
        
        # Verificar permisos para ver este indicador
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != indicador["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver este indicador")
        
        return indicador
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paciente/{paciente_id}", response_model=List[IndicadoresSalud])
async def obtener_indicadores_por_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != paciente_id:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver estos indicadores")
        
        indicadores = IndicadoresSaludModel.get_by_paciente_id(paciente_id)
        return indicadores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{indicador_id}", response_model=IndicadoresSalud)
async def actualizar_indicador(
    indicador_id: int, 
    indicador: IndicadoresSaludUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        indicador_existente = IndicadoresSaludModel.get_by_id(indicador_id)
        if not indicador_existente:
            raise HTTPException(status_code=404, detail="Indicador de salud no encontrado")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != indicador_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para actualizar este indicador")
        
        indicador_actualizado = IndicadoresSaludModel.update(indicador_id, indicador.dict(exclude_unset=True))
        return indicador_actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{indicador_id}")
async def eliminar_indicador(
    indicador_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        indicador_existente = IndicadoresSaludModel.get_by_id(indicador_id)
        if not indicador_existente:
            raise HTTPException(status_code=404, detail="Indicador de salud no encontrado")
        
        # Solo médicos, admin o el propio paciente pueden eliminar
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != indicador_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para eliminar este indicador")
        
        eliminado = IndicadoresSaludModel.delete(indicador_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar indicador de salud")
        
        return {"message": "Indicador de salud eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))