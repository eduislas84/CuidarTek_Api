from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import db
from middleware.logging_middleware import LoggingMiddleware
from controllers import (
    auth_controller,
    usuario_controller, 
    paciente_controller,
    indicadores_salud_controller,
    alertas_controller,
    recomendaciones_controller,
    retos_controller,
    citas_medicas_controller,
    reportes_medicos_controller,
    sesiones_wearable_controller,
    log_accesos_controller,
    mensajes_controller,
    paciente_medico_controller,
    medico_controller
)

app = FastAPI(
    title="CuidarTek API",
    description="API para el sistema de monitoreo de salud CuidarTek - Con autenticación JWT y control de roles",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de logging
app.add_middleware(LoggingMiddleware)

# Crear base de datos al iniciar
@app.on_event("startup")
async def startup_event():
    db.create_database_and_tables()

@app.get("/")
async def root():
    return {"message": "Bienvenido a CuidarTek API", "status": "active", "version": "2.0.0"}

# Incluir routers de todos los controladores
app.include_router(auth_controller.router)
app.include_router(usuario_controller.router)
app.include_router(paciente_controller.router)
app.include_router(indicadores_salud_controller.router)
app.include_router(alertas_controller.router)
app.include_router(recomendaciones_controller.router)
app.include_router(retos_controller.router)
app.include_router(citas_medicas_controller.router)
app.include_router(reportes_medicos_controller.router)
app.include_router(sesiones_wearable_controller.router)
app.include_router(log_accesos_controller.router)
app.include_router(mensajes_controller.router)
app.include_router(paciente_medico_controller.router)
app.include_router(medico_controller.router)

@app.get("/status/database")
async def verificar_estado_db():
    connection = db.get_connection()
    if connection:
        connection.close()
        return {"status": "Conectado", "database": db.database}
    else:
        return {"status": "Desconectado", "database": db.database}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)