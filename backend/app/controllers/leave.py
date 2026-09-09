from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user

from app.models.employee import Employee
from app.schemas.leave import (
    LeaveCreate,
    LeaveResponse,
)

from app.services.leave_service import (
    apply_leave_service,
    get_employee_leaves_service,
    get_all_leaves_service,
    get_leave_service,
    update_leave_status_service,
)


router = APIRouter(
    prefix="/leave",
    tags=["Leave Management"],
)


# ============================================================
# EMPLOYEE - APPLY LEAVE
# ============================================================

@router.post(
    "/",
    response_model=LeaveResponse,
    status_code=status.HTTP_201_CREATED,
)
def apply_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    role = current_user.get("role")

    if role != "Employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can apply for leave.",
        )

    employee = (
        db.query(Employee)
        .filter(
            Employee.email == current_user.get("sub")
        )
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found.",
        )

    created_leave, error = apply_leave_service(
        db=db,
        employee_id=employee.id,
        leave=leave,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return created_leave


# ============================================================
# EMPLOYEE - VIEW OWN LEAVES
# ============================================================

@router.get(
    "/my",
    response_model=List[LeaveResponse],
)
def get_my_leaves(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    role = current_user.get("role")

    if role != "Employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can access their leave history.",
        )

    employee = (
        db.query(Employee)
        .filter(
            Employee.email == current_user.get("sub")
        )
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found.",
        )

    return get_employee_leaves_service(
        db,
        employee.id,
    )


# ============================================================
# ADMIN - VIEW ALL LEAVES
# ============================================================

@router.get(
    "/all",
    response_model=List[LeaveResponse],
)
def get_all_leaves(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    role = current_user.get("role")

    if role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    return get_all_leaves_service(db)


# ============================================================
# GET SINGLE LEAVE
# ============================================================

@router.get(
    "/{leave_id}",
    response_model=LeaveResponse,
)
def get_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    leave = get_leave_service(
        db,
        leave_id,
    )

    if leave is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave not found.",
        )

    role = current_user.get("role")

    # Admin can access any leave
    if role == "Admin":
        return leave

    # Employee can access only their own leave
    if role == "Employee":
        employee = (
            db.query(Employee)
            .filter(
                Employee.email == current_user.get("sub")
            )
            .first()
        )

        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee profile not found.",
            )

        if leave.employee_id != employee.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own leave.",
            )

        return leave

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied.",
    )


# ============================================================
# ADMIN - APPROVE LEAVE
# ============================================================

@router.put(
    "/{leave_id}/approve",
    response_model=LeaveResponse,
)
def approve_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.get("role") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    updated_leave, error = update_leave_status_service(
        db=db,
        leave_id=leave_id,
        status="Approved",
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return updated_leave


# ============================================================
# ADMIN - REJECT LEAVE
# ============================================================

@router.put(
    "/{leave_id}/reject",
    response_model=LeaveResponse,
)
def reject_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.get("role") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    updated_leave, error = update_leave_status_service(
        db=db,
        leave_id=leave_id,
        status="Rejected",
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return updated_leave