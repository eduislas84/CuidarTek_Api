from fastapi import APIRouter, HTTPException, Depends
from models.citas_medicas_model import CitasMedicasModel
from models.paciente_model import PacienteModel
from models.usuario_model import UsuarioModel
from schemas.citas_medicas_schema import CitasMedicas, CitasMedicasCreate, CitasMedicasUpdate
from auth import require_role, require_medico, get_current_active_user
from typing import List

router = APIRouter(prefix="/citas-medicas", tags=["citas_medicas"])

@router.post("/", response_model=CitasMedicas)
async def crear_cita(
    cita: CitasMedicasCreate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos para crear cita
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != cita.id_paciente:
                raise HTTPException(status_code=403, detail="Solo puede crear citas para su propio perfil")
        
        # Verificar que el médico existe y es médico
        medico = UsuarioModel.get_by_id(cita.id_medico)
        if not medico or medico["rol"] not in ["medico", "admin"]:
            raise HTTPException(status_code=400, detail="El médico especificado no existe o no tiene rol válido")
        
        nueva_cita = CitasMedicasModel.create(cita.dict())
        if not nueva_cita:
            raise HTTPException(status_code=500, detail="Error al crear cita médica")
        return nueva_cita
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[CitasMedicas], dependencies=[Depends(require_medico)])
async def listar_citas():
    try:
        citas = CitasMedicasModel.get_all()
        return citas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/programadas", response_model=List[CitasMedicas])
async def listar_citas_programadas(current_user: dict = Depends(get_current_active_user)):
    try:
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if paciente:
                citas = CitasMedicasModel.get_by_paciente_id(paciente["id_paciente"])
                return [c for c in citas if c["estatus"] == "programada"]
            return []
        elif current_user["rol"] == "medico":
            citas = CitasMedicasModel.get_by_medico_id(current_user["id_usuario"])
            return [c for c in citas if c["estatus"] == "programada"]
        else:
            citas = CitasMedicasModel.get_programadas()
            return citas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{cita_id}", response_model=CitasMedicas)
async def obtener_cita(
    cita_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        cita = CitasMedicasModel.get_by_id(cita_id)
        if not cita:
            raise HTTPException(status_code=404, detail="Cita médica no encontrada")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != cita["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver esta cita")
        elif current_user["rol"] == "medico" and cita["id_medico"] != current_user["id_usuario"]:
            raise HTTPException(status_code=403, detail="No tiene permisos para ver esta cita")
        
        return cita
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paciente/{paciente_id}", response_model=List[CitasMedicas])
async def obtener_citas_por_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != paciente_id:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver estas citas")
        
        citas = CitasMedicasModel.get_by_paciente_id(paciente_id)
        return citas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/medico/{medico_id}", response_model=List[CitasMedicas])
async def obtener_citas_por_medico(
    medico_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos
        if current_user["rol"] == "medico" and current_user["id_usuario"] != medico_id:
            raise HTTPException(status_code=403, detail="No tiene permisos para ver estas citas")
        
        citas = CitasMedicasModel.get_by_medico_id(medico_id)
        return citas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{cita_id}", response_model=CitasMedicas)
async def actualizar_cita(
    cita_id: int, 
    cita: CitasMedicasUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        cita_existente = CitasMedicasModel.get_by_id(cita_id)
        if not cita_existente:
            raise HTTPException(status_code=404, detail="Cita médica no encontrada")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != cita_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para actualizar esta cita")
        elif current_user["rol"] == "medico" and cita_existente["id_medico"] != current_user["id_usuario"]:
            raise HTTPException(status_code=403, detail="No tiene permisos para actualizar esta cita")
        
        cita_actualizada = CitasMedicasModel.update(cita_id, cita.dict(exclude_unset=True))
        return cita_actualizada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{cita_id}")
async def eliminar_cita(
    cita_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        cita_existente = CitasMedicasModel.get_by_id(cita_id)
        if not cita_existente:
            raise HTTPException(status_code=404, detail="Cita médica no encontrada")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != cita_existente["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para eliminar esta cita")
        elif current_user["rol"] == "medico" and cita_existente["id_medico"] != current_user["id_usuario"]:
            raise HTTPException(status_code=403, detail="No tiene permisos para eliminar esta cita")
        
        eliminado = CitasMedicasModel.delete(cita_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar cita médica")
        
        return {"message": "Cita médica eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))