from fastapi import APIRouter, HTTPException, status, Depends
from models.usuario_model import UsuarioModel
from schemas.auth_schema import LoginRequest, Token, UsuarioResponse
from auth import auth_handler, get_current_active_user

router = APIRouter(prefix="/auth", tags=["autenticacion"])

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    # Buscar usuario por correo
    usuario = UsuarioModel.get_by_email(login_data.correo)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Verificar contraseña (en producción, debería estar hasheada)
    if not auth_handler.verify_password(login_data.password, usuario["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Verificar que el usuario esté activo
    if usuario["estatus"] != "Activo":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )
    
    # Crear token
    access_token = auth_handler.create_access_token(
        data={"sub": str(usuario["id_usuario"])}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UsuarioResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    return current_user

@router.post("/register")
async def register_user(login_data: LoginRequest, nombre: str, rol: str = "paciente"):
    # Verificar si el correo ya existe
    usuario_existente = UsuarioModel.get_by_email(login_data.correo)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    # Hashear contraseña
    hashed_password = auth_handler.get_password_hash(login_data.password)
    
    # Crear usuario
    nuevo_usuario = UsuarioModel.create({
        "nombre": nombre,
        "correo": login_data.correo,
        "password": hashed_password,
        "rol": rol,
        "estatus": "Activo"
    })
    
    return {"message": "Usuario registrado exitosamente", "id_usuario": nuevo_usuario["id_usuario"]}