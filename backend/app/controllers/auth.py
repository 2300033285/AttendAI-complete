from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token
from app.services.auth_service import register_service, login_service
from app.security import get_current_user
from app.services.attendance_service import check_out_service


router = APIRouter(tags=["Authentication"])


@router.post(
    "/register",
    tags=["Authentication"],
    summary="Register a New User",
    description="Creates a new user account in the AttendAI system."
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = register_service(db, user)

    return {
        "message": "User Registered Successfully",
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role,
    }


@router.post(
    "/login",
    response_model=Token,
    tags=["Authentication"],
    summary="User Login",
    description="Authenticates a user and returns a JWT access token."
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return login_service(db, user)


@router.post(
    "/logout",
    tags=["Authentication"],
    summary="User Logout",
    description="Logs out the current user and records attendance check-out."
)
def logout(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Get user ID from JWT
    user_id = current_user["id"]

    # Perform attendance check-out
    attendance, error = check_out_service(
        db,
        user_id
    )

    # Handle check-out errors
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    return {
        "message": "Logout successful. Check-out recorded.",
        "user_id": user_id,
        "attendance_id": attendance.id,
        "date": attendance.date,
        "check_in": attendance.check_in,
        "check_out": attendance.check_out,
        "status": attendance.status
    }