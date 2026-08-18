from pydantic import BaseModel, EmailStr, ConfigDict


# ==========================================
# CREATE USER
# ==========================================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "Employee"

    department: str = "General"
    phone: str = "Not Provided"


# ==========================================
# UPDATE USER
# ==========================================

class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    department: str
    phone: str
    role: str


# ==========================================
# LOGIN USER
# ==========================================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ==========================================
# USER RESPONSE
# ==========================================

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    department: str
    phone: str
    role: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================
# TOKEN RESPONSE
# ==========================================

class Token(BaseModel):
    access_token: str
    token_type: str