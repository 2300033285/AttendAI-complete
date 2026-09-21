from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user, require_roles

from app.schemas.opening import (
    OpeningCreate,
    OpeningUpdate,
    OpeningResponse,
)

from app.services.opening_service import (
    create_opening_service,
    get_all_openings_service,
    get_opening_service,
    update_opening_service,
    delete_opening_service,
)


router = APIRouter(
    prefix="/openings",
    tags=["Openings Management"],
)


# =====================================================
# CREATE OPENING - ADMIN ONLY
# =====================================================

@router.post(
    "/",
    response_model=OpeningResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_opening(
    opening: OpeningCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    created_opening, error = create_opening_service(
        db=db,
        opening=opening,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return created_opening


# =====================================================
# GET ALL OPENINGS - ADMIN + EMPLOYEE
# =====================================================

@router.get(
    "/",
    response_model=List[OpeningResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_openings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_all_openings_service(db)


# =====================================================
# GET OPENING BY ID - ADMIN + EMPLOYEE
# =====================================================

@router.get(
    "/{opening_id}",
    response_model=OpeningResponse,
    status_code=status.HTTP_200_OK,
)
def get_opening(
    opening_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    opening = get_opening_service(
        db=db,
        opening_id=opening_id,
    )

    if opening is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opening not found.",
        )

    return opening


# =====================================================
# UPDATE OPENING - ADMIN ONLY
# =====================================================

@router.put(
    "/{opening_id}",
    response_model=OpeningResponse,
    status_code=status.HTTP_200_OK,
)
def update_opening(
    opening_id: int,
    opening: OpeningUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    updated_opening, error = update_opening_service(
        db=db,
        opening_id=opening_id,
        opening=opening,
    )

    if error:
        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
                if error == "Opening not found."
                else status.HTTP_400_BAD_REQUEST
            ),
            detail=error,
        )

    return updated_opening


# =====================================================
# DELETE OPENING - ADMIN ONLY
# =====================================================

@router.delete(
    "/{opening_id}",
    status_code=status.HTTP_200_OK,
)
def delete_opening(
    opening_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    deleted_opening, error = delete_opening_service(
        db=db,
        opening_id=opening_id,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error,
        )

    return {
        "message": "Opening deleted successfully.",
        "opening_id": deleted_opening.id,
    }