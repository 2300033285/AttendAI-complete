from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.security import hash_password


# ==========================================
# CREATE USER
# ==========================================

def create_user(db: Session, user: UserCreate):

    print("\n========== CREATE USER DEBUG ==========")
    print("REGISTER EMAIL:", user.email)

    # Check existing email
    existing_user = (
        db.query(User)
        .filter(User.email == user.email.lower())
        .first()
    )

    print("EXISTING USER:", existing_user)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    print(
        "PASSWORD HASH CREATED:",
        hashed_password[:20] + "..."
    )

    # Create user
    new_user = User(
        username=user.username,
        email=user.email.lower(),
        password=hashed_password,
        role=user.role,
        department=user.department,
        phone=user.phone,
        is_active=True
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print("USER CREATED SUCCESSFULLY")
        print("USER ID:", new_user.id)
        print("EMAIL:", new_user.email)
        print("=====================================\n")

        return new_user

    except Exception as e:

        db.rollback()

        print("\n========== DATABASE ERROR ==========")
        print(str(e))
        print("====================================\n")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


# ==========================================
# GET ALL USERS
# ==========================================

def get_users(db: Session):
    return db.query(User).all()


# ==========================================
# GET USER BY ID
# ==========================================

def get_user_by_id(db: Session, user_id: int):

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


# ==========================================
# GET USER BY EMAIL
# ==========================================

def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(User.email == email.lower())
        .first()
    )


# ==========================================
# GET PROFILE
# ==========================================

def get_profile(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(User.email == email.lower())
        .first()
    )


# ==========================================
# UPDATE USER
# ==========================================

def update_user(
    db: Session,
    user_id: int,
    user: UserUpdate
):

    existing_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if existing_user is None:
        return None

    existing_user.username = user.username
    existing_user.email = user.email.lower()
    existing_user.department = user.department
    existing_user.phone = user.phone
    existing_user.role = user.role

    db.commit()
    db.refresh(existing_user)

    return existing_user


# ==========================================
# DELETE USER
# ==========================================

def delete_user(
    db: Session,
    user_id: int
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        return None

    db.delete(user)
    db.commit()

    return user