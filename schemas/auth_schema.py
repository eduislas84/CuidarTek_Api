from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    usuario_id: Optional[int] = None

class LoginRequest(BaseModel):
    correo: str
    password: str

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    rol: str
    estatus: str

    class Config:
        from_attributes = True