from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.security import get_current_user, require_roles

from app.crud.shift_analytics import get_shift_analytics
from app.schemas.shift_analytics import ShiftAnalyticsResponse

# =====================================================
# IMPORT MODELS
# =====================================================

from app.models.user import User
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.shift import Shift
from app.models.qr_attendance import QRAttendance

# =====================================================
# IMPORT CONTROLLERS
# =====================================================

from app.controllers import dashboard
from app.controllers import reports
from app.controllers import analytics
from app.controllers import employee_analytics
from app.controllers import ai_prediction
from app.controllers import insights
from app.controllers import anomaly
from app.controllers import shift
from app.controllers import auth
from app.controllers import employee
from app.controllers import attendance
from app.controllers import qr_attendance

# =====================================================
# USER CRUD
# =====================================================

from app.crud.user import (
    get_users,
    get_user_by_id,
    update_user,
    delete_user,
)

# =====================================================
# USER SCHEMAS
# =====================================================

from app.schemas.user import UserUpdate, UserResponse

# =====================================================
# SERVICES
# =====================================================

from app.services.user_service import profile_service


# =====================================================
# MODELS LOADED
# =====================================================

print("Models Loaded:", Base.metadata.tables.keys())


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="AttendAI Backend",
    description="Backend API for AttendAI Internship Project",
    version="1.0.0",
)


# =====================================================
# CORS CONFIGURATION
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# REGISTER ROUTERS
# =====================================================

app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(shift.router)
app.include_router(attendance.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(analytics.router)
app.include_router(employee_analytics.router)
app.include_router(ai_prediction.router)
app.include_router(insights.router)
app.include_router(anomaly.router)
app.include_router(qr_attendance.router)

# =====================================================
# HOME
# =====================================================

@app.get(
    "/",
    tags=["Home"],
    summary="Welcome",
    description="Welcome endpoint of AttendAI Backend.",
)
def root():
    return {
        "message": "Welcome to AttendAI Backend"
    }


# =====================================================
# DATABASE TEST
# =====================================================

@app.get(
    "/db-test",
    tags=["Database"],
    summary="Database Connection Test",
    description="Checks whether the PostgreSQL database is connected successfully.",
)
def db_test():

    try:

        connection = engine.connect()
        connection.close()

        return {
            "message": "Database Connected Successfully ✅"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================================
# GET MY PROFILE
# =====================================================

@app.get(
    "/profile",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get My Profile",
    description="Returns the profile details of the currently logged-in user.",
)
def profile(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return profile_service(
        db,
        current_user
    )


# =====================================================
# GET ALL USERS
# =====================================================

@app.get(
    "/users",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get All Users",
    description="Returns all registered users. Accessible by Admin, HR and Manager.",
)
def users(
    current_user=Depends(
        require_roles(["Admin", "HR", "Manager"])
    ),
    db: Session = Depends(get_db),
):

    return get_users(db)


# =====================================================
# GET USER BY ID
# =====================================================

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get User by ID",
    description="Returns details of a specific user.",
)
def user_by_id(
    user_id: int,
    current_user=Depends(
        require_roles(["Admin", "HR", "Manager"])
    ),
    db: Session = Depends(get_db),
):

    user = get_user_by_id(
        db,
        user_id
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# =====================================================
# UPDATE USER
# =====================================================

@app.put(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Update User",
    description="Updates an existing user's details. Accessible by Admin and HR.",
)
def update_user_api(
    user_id: int,
    user: UserUpdate,
    current_user=Depends(
        require_roles(["Admin", "HR"])
    ),
    db: Session = Depends(get_db),
):

    updated_user = update_user(
        db,
        user_id,
        user
    )

    if updated_user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return updated_user


# =====================================================
# DELETE USER
# =====================================================

@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Delete User",
    description="Deletes a user from the system. Accessible only by Admin.",
)
def delete(
    user_id: int,
    current_user=Depends(
        require_roles(["Admin"])
    ),
    db: Session = Depends(get_db),
):

    deleted = delete_user(
        db,
        user_id
    )

    if deleted is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }


# =====================================================
# SHIFT ANALYTICS
# =====================================================

@app.get(
    "/shift-analytics",
    response_model=ShiftAnalyticsResponse,
    tags=["Shift Analytics"],
    summary="Get Shift Analytics",
    description="Returns analytics calculated from Shift Management data.",
)
def shift_analytics(
    db: Session = Depends(get_db),
):

    return get_shift_analytics(db)