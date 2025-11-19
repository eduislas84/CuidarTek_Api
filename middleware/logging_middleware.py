from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from models.log_accesos_model import LogAccesosModel
from auth import AuthHandler
import time

# Crear instancia de AuthHandler para el middleware
auth_handler_middleware = AuthHandler()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Excluir endpoints públicos
        public_paths = ["/", "/auth/login", "/auth/register", "/docs", "/openapi.json", "/status/database"]
        if request.url.path in public_paths:
            response = await call_next(request)
            return response
        
        start_time = time.time()
        
        try:
            # Intentar obtener el usuario del token
            usuario_id = None
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                try:
                    token = auth_header.replace("Bearer ", "")
                    usuario_id = auth_handler_middleware.verify_token_manual(token)
                except:
                    pass
            
            response = await call_next(request)
            
            # Registrar el acceso (solo si es exitoso y tenemos usuario)
            if usuario_id and response.status_code < 400:
                accion = self._get_accion_from_request(request)
                ip_origen = request.client.host if request.client else "Unknown"
                
                try:
                    LogAccesosModel.create({
                        "id_usuario": usuario_id,
                        "accion": accion,
                        "ip_origen": ip_origen
                    })
                except Exception as e:
                    # Si falla el logging, no interrumpir la respuesta
                    print(f"Error registrando log: {e}")
            
            return response
            
        except Exception as e:
            # Si hay un error, dejar que FastAPI lo maneje
            raise e
        finally:
            process_time = time.time() - start_time
            print(f"{request.method} {request.url.path} - {process_time:.2f}s")
    
    def _get_accion_from_request(self, request: Request) -> str:
        method = request.method
        path = request.url.path
        
        # ✅ ACCIONES MÁS CORTAS para evitar el error de truncamiento
        if method == "GET":
            return "consulta"
        elif method == "POST":
            if "/auth/" in path:
                return "login"
            return "crear"
        elif method == "PUT":
            return "actualizar"
        elif method == "DELETE":
            return "eliminar"
        else:
            return "otra"