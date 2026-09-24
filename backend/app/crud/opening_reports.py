from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.opening import Opening


def get_opening_report(db: Session):

    # Overall summary
    total_openings = (
        db.query(func.count(Opening.id))
        .scalar()
    )

    # Status report
    status_report = (
        db.query(
            Opening.status,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.status)
        .all()
    )

    # Department report
    department_report = (
        db.query(
            Opening.department,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.department)
        .all()
    )

    # Job title report
    job_title_report = (
        db.query(
            Opening.job_title,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.job_title)
        .all()
    )

    # Location report
    location_report = (
        db.query(
            Opening.location,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.location)
        .all()
    )

    # Employment type report
    employment_type_report = (
        db.query(
            Opening.employment_type,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.employment_type)
        .all()
    )

    # Experience report
    experience_report = (
        db.query(
            Opening.experience,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.experience)
        .all()
    )

    return {
        "total_openings": total_openings,

        "status_report": [
            {
                "status": status,
                "count": count
            }
            for status, count in status_report
        ],

        "department_report": [
            {
                "department": department,
                "count": count
            }
            for department, count in department_report
        ],

        "job_title_report": [
            {
                "job_title": job_title,
                "count": count
            }
            for job_title, count in job_title_report
        ],

        "location_report": [
            {
                "location": location,
                "count": count
            }
            for location, count in location_report
        ],

        "employment_type_report": [
            {
                "employment_type": employment_type,
                "count": count
            }
            for employment_type, count in employment_type_report
        ],

        "experience_report": [
            {
                "experience": experience,
                "count": count
            }
            for experience, count in experience_report
        ]
    }