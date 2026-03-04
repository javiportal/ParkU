from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    contrasena: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@parku.edu.sv",
                "contrasena": "admin123",
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
