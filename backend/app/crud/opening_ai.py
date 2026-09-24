from sqlalchemy.orm import Session

from app.models.opening import Opening


def get_opening_ai_data(db: Session):

    openings = (
        db.query(Opening)
        .all()
    )

    ai_data = []

    for opening in openings:

        ai_data.append(
            {
                "opening_id": opening.id,
                "job_title": opening.job_title,
                "department": opening.department,
                "location": opening.location,
                "employment_type": opening.employment_type,
                "experience": opening.experience,
                "status": opening.status,
                "created_at": opening.created_at,
            }
        )

    return {
        "total_records": len(ai_data),
        "features": [
            "job_title",
            "department",
            "location",
            "employment_type",
            "experience",
            "status",
            "created_at",
        ],
        "data": ai_data,
    }