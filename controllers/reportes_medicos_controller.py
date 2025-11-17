from fastapi import APIRouter, HTTPException, Depends
from models.reportes_medicos_model import ReportesMedicosModel
from models.paciente_model import PacienteModel
from models.usuario_model import UsuarioModel
from schemas.reportes_medicos_schema import ReportesMedicos, ReportesMedicosCreate, ReportesMedicosUpdate
from auth import require_role, require_medico, get_current_active_user
from typing import List

router = APIRouter(prefix="/reportes-medicos", tags=["reportes_medicos"])

@router.post("/", response_model=ReportesMedicos, dependencies=[Depends(require_medico)])
async def crear_reporte(reporte: ReportesMedicosCreate):
    try:
        # Verificar que el médico existe y es médico
        medico = UsuarioModel.get_by_id(reporte.id_medico)
        if not medico or medico["rol"] not in ["medico", "admin"]:
            raise HTTPException(status_code=400, detail="El médico especificado no existe o no tiene rol válido")
        
        nuevo_reporte = ReportesMedicosModel.create(reporte.dict())
        if not nuevo_reporte:
            raise HTTPException(status_code=500, detail="Error al crear reporte médico")
        return nuevo_reporte
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ReportesMedicos], dependencies=[Depends(require_medico)])
async def listar_reportes():
    try:
        reportes = ReportesMedicosModel.get_all()
        return reportes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{reporte_id}", response_model=ReportesMedicos)
async def obtener_reporte(
    reporte_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        reporte = ReportesMedicosModel.get_by_id(reporte_id)
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte médico no encontrado")
        
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != reporte["id_paciente"]:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver este reporte")
        elif current_user["rol"] == "medico" and reporte["id_medico"] != current_user["id_usuario"]:
            raise HTTPException(status_code=403, detail="No tiene permisos para ver este reporte")
        
        return reporte
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paciente/{paciente_id}", response_model=List[ReportesMedicos])
async def obtener_reportes_por_paciente(
    paciente_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos
        if current_user["rol"] == "paciente":
            paciente = PacienteModel.get_by_usuario_id(current_user["id_usuario"])
            if not paciente or paciente["id_paciente"] != paciente_id:
                raise HTTPException(status_code=403, detail="No tiene permisos para ver estos reportes")
        
        reportes = ReportesMedicosModel.get_by_paciente_id(paciente_id)
        return reportes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/medico/{medico_id}", response_model=List[ReportesMedicos])
async def obtener_reportes_por_medico(
    medico_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        # Verificar permisos
        if current_user["rol"] == "medico" and current_user["id_usuario"] != medico_id:
            raise HTTPException(status_code=403, detail="No tiene permisos para ver estos reportes")
        
        reportes = ReportesMedicosModel.get_by_medico_id(medico_id)
        return reportes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{reporte_id}", response_model=ReportesMedicos, dependencies=[Depends(require_medico)])
async def actualizar_reporte(reporte_id: int, reporte: ReportesMedicosUpdate):
    try:
        reporte_existente = ReportesMedicosModel.get_by_id(reporte_id)
        if not reporte_existente:
            raise HTTPException(status_code=404, detail="Reporte médico no encontrado")
        
        reporte_actualizado = ReportesMedicosModel.update(reporte_id, reporte.dict(exclude_unset=True))
        return reporte_actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{reporte_id}", dependencies=[Depends(require_medico)])
async def eliminar_reporte(reporte_id: int):
    try:
        reporte_existente = ReportesMedicosModel.get_by_id(reporte_id)
        if not reporte_existente:
            raise HTTPException(status_code=404, detail="Reporte médico no encontrado")
        
        eliminado = ReportesMedicosModel.delete(reporte_id)
        if not eliminado:
            raise HTTPException(status_code=500, detail="Error al eliminar reporte médico")
        
        return {"message": "Reporte médico eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))