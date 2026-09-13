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
    update_leave_status_by_employee_service,
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
    role = (current_user.get("role") or "").lower()

    if role != "employee":
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
    role = (current_user.get("role") or "").lower()

    if role != "employee":
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
    role = (current_user.get("role") or "").lower()

    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    return get_all_leaves_service(db)


# ============================================================
# ADMIN - GET LEAVES BY EMPLOYEE ID
# ============================================================

@router.get(
    "/{employee_id}",
    response_model=List[LeaveResponse],
)
<<<<<<< HEAD
def get_employee_leaves(
    employee_id: int,
=======
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

    role = (current_user.get("role") or "").lower()

    # Admin can access any leave
    if role == "admin":
        return leave

    # Employee can access only their own leave
    if role == "employee":
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
>>>>>>> 36d1fe10b278c0e38770957407e73ad3717adbd8
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if (current_user.get("role") or "").lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    employee = (
        db.query(Employee)
        .filter(
            Employee.id == employee_id
        )
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    return get_employee_leaves_service(
        db,
        employee_id,
    )


# ============================================================
# ADMIN - APPROVE LEAVE BY EMPLOYEE ID
# ============================================================

@router.put(
    "/{employee_id}/approve",
    response_model=LeaveResponse,
)
def approve_leave(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.get("role") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    updated_leave, error = (
        update_leave_status_by_employee_service(
            db=db,
            employee_id=employee_id,
            status="Approved",
        )
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error,
        )

    return updated_leave


# ============================================================
# ADMIN - REJECT LEAVE BY EMPLOYEE ID
# ============================================================

@router.put(
    "/{employee_id}/reject",
    response_model=LeaveResponse,
)
def reject_leave(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if (current_user.get("role") or "").lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    updated_leave, error = (
        update_leave_status_by_employee_service(
            db=db,
            employee_id=employee_id,
            status="Rejected",
        )
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error,
        )

    return updated_leave