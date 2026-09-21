from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.schemas.referral import (
    ReferralCreate,
    ReferralUpdate,
    ReferralResponse,
)

from app.services.referral_service import (
    create_referral_service,
    get_all_referrals_service,
    get_referral_service,
    get_employee_referrals_service,
    update_referral_service,
    delete_referral_service,
)


router = APIRouter(
    prefix="/referrals",
    tags=["Employee Referral System"],
)


# =====================================================
# CREATE REFERRAL - EMPLOYEE ONLY
# =====================================================

@router.post(
    "/",
    response_model=ReferralResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_referral(
    referral: ReferralCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Employee"])
    ),
):
    # JWT payload is a dictionary
    employee_id_value = current_user.get("employee_id")

    if employee_id_value is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee profile is not linked to this user.",
        )

    # Convert employee ID from string to integer
    try:
        employee_id = int(employee_id_value)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid employee ID associated with this user.",
        )

    created_referral, error = create_referral_service(
        db=db,
        referral=referral,
        employee_id=employee_id,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return created_referral


# =====================================================
# GET ALL REFERRALS - ADMIN ONLY
# =====================================================

@router.get(
    "/",
    response_model=List[ReferralResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_referrals(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    return get_all_referrals_service(db)


# =====================================================
# GET MY REFERRALS - EMPLOYEE ONLY
# =====================================================

@router.get(
    "/my",
    response_model=List[ReferralResponse],
    status_code=status.HTTP_200_OK,
)
def get_my_referrals(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Employee"])
    ),
):
    # JWT payload is a dictionary
    employee_id_value = current_user.get("employee_id")

    if employee_id_value is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee profile is not linked to this user.",
        )

    # Convert employee ID from string to integer
    try:
        employee_id = int(employee_id_value)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid employee ID associated with this user.",
        )

    return get_employee_referrals_service(
        db=db,
        employee_id=employee_id,
    )


# =====================================================
# GET REFERRAL BY ID - ADMIN ONLY
# =====================================================

@router.get(
    "/{referral_id}",
    response_model=ReferralResponse,
    status_code=status.HTTP_200_OK,
)
def get_referral(
    referral_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    referral = get_referral_service(
        db=db,
        referral_id=referral_id,
    )

    if referral is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referral not found.",
        )

    return referral


# =====================================================
# UPDATE REFERRAL - ADMIN ONLY
# =====================================================

@router.put(
    "/{referral_id}",
    response_model=ReferralResponse,
    status_code=status.HTTP_200_OK,
)
def update_referral(
    referral_id: int,
    referral: ReferralUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    updated_referral, error = update_referral_service(
        db=db,
        referral_id=referral_id,
        referral=referral,
    )

    if error:
        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
                if error == "Referral not found."
                else status.HTTP_400_BAD_REQUEST
            ),
            detail=error,
        )

    return updated_referral


# =====================================================
# DELETE REFERRAL - ADMIN ONLY
# =====================================================

@router.delete(
    "/{referral_id}",
    status_code=status.HTTP_200_OK,
)
def delete_referral(
    referral_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    deleted_referral, error = delete_referral_service(
        db=db,
        referral_id=referral_id,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error,
        )

    return {
        "message": "Referral deleted successfully.",
        "referral_id": deleted_referral.id,
    }