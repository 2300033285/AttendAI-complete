from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate, UserLogin
from app.security import (
    verify_password,
    create_access_token
)


# =========================
# REGISTER USER
# =========================

def register_service(
    db: Session,
    user: UserCreate
):

    print("\n========== REGISTER DEBUG ==========")
    print("REGISTER EMAIL:", user.email)

    new_user = create_user(db, user)

    print("USER CREATED SUCCESSFULLY")
    print("USER ID:", new_user.id)
    print("EMAIL:", new_user.email)
    print("====================================\n")

    return new_user


# =========================
# LOGIN USER
# =========================

def login_service(
    db: Session,
    user: UserLogin
):

    print("\n========== LOGIN DEBUG ==========")
    print("LOGIN EMAIL:", user.email)

    # Find user by email
    db_user = get_user_by_email(
        db,
        user.email
    )

    print("DATABASE USER:", db_user)

    # User does not exist
    if db_user is None:

        print("RESULT: USER NOT FOUND")
        print("=================================\n")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password"
        )

    print("USER FOUND!")
    print("USER ID:", db_user.id)
    print("STORED EMAIL:", db_user.email)
    print("STORED PASSWORD HASH:", db_user.password)

    # Verify password
    password_valid = verify_password(
        user.password,
        db_user.password
    )

    print("PASSWORD VALID:", password_valid)

    # Password is incorrect
    if not password_valid:

        print("RESULT: PASSWORD INCORRECT")
        print("=================================\n")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    print("RESULT: LOGIN SUCCESSFUL")
    print("TOKEN CREATED SUCCESSFULLY")
    print("=================================\n")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }