from pydantic import BaseModel, Field
from datetime import date

class MuestraBase(BaseModel):
    tipo_de_muestra: str = Field(...)
    cantidad: float = Field(..., gt=0)
    tipo_de_sangre: str = Field(...)
    fecha_de_recoleccion: date

class MuestraCreate(MuestraBase):
    id: str

class MuestraResponse(MuestraBase):
    id: str
    class Config:
        orm_mode = True

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    role: str = "usuario_laboratorio"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
