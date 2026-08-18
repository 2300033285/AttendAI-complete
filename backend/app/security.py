from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# PASSWORD HASHING
# =====================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =====================================================
# JWT SETTINGS
# =====================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is missing! Check your .env file."
    )


ALGORITHM = "HS256"

# Token expires after 24 hours
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# =====================================================
# BEARER AUTHENTICATION
# =====================================================

security = HTTPBearer()


# =====================================================
# JWT TOKEN CREATION
# =====================================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# =====================================================
# GET CURRENT USER
# =====================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    # Extra safety in case "Bearer " is included
    if token.startswith("Bearer "):
        token = token[7:]

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError as e:

        print("JWT Error:", e)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Token"
        )


# =====================================================
# ROLE BASED ACCESS CONTROL
# =====================================================

def require_roles(allowed_roles: list):

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        user_role = current_user.get("role")

        if user_role not in allowed_roles:

            # Same message for VS Code terminal and API response
            message = (
                "Access denied. You do not have permission to "
                "perform this action. Please contact your "
                "administrator if you require access."
            )

            # Show in VS Code terminal
            print(message)

            # Show in Swagger / Frontend
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=message
            )

        return current_user

    return role_checker