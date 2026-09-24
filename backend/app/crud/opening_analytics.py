from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.opening import Opening


def get_opening_analytics(db: Session):

    # Total openings
    total_openings = (
        db.query(func.count(Opening.id))
        .scalar()
    )

    # Status-wise openings
    status_summary = (
        db.query(
            Opening.status,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.status)
        .all()
    )

    # Department-wise openings
    department_summary = (
        db.query(
            Opening.department,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.department)
        .all()
    )

    # Employment type-wise openings
    employment_type_summary = (
        db.query(
            Opening.employment_type,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.employment_type)
        .all()
    )

    # Experience-wise openings
    experience_summary = (
        db.query(
            Opening.experience,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.experience)
        .all()
    )

    # Job-title-wise openings
    job_title_summary = (
        db.query(
            Opening.job_title,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.job_title)
        .all()
    )

    # Location-wise openings
    location_summary = (
        db.query(
            Opening.location,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.location)
        .all()
    )

    return {
        "total_openings": total_openings,

        "status_summary": [
            {
                "status": status,
                "count": count
            }
            for status, count in status_summary
        ],

        "department_summary": [
            {
                "department": department,
                "count": count
            }
            for department, count in department_summary
        ],

        "employment_type_summary": [
            {
                "employment_type": employment_type,
                "count": count
            }
            for employment_type, count in employment_type_summary
        ],

        "experience_summary": [
            {
                "experience": experience,
                "count": count
            }
            for experience, count in experience_summary
        ],

        "job_title_summary": [
            {
                "job_title": job_title,
                "count": count
            }
            for job_title, count in job_title_summary
        ],

        "location_summary": [
            {
                "location": location,
                "count": count
            }
            for location, count in location_summary
        ]
    }