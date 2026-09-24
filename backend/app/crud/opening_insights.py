from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.opening import Opening


def get_opening_insights(db: Session):

    total_openings = (
        db.query(func.count(Opening.id))
        .scalar()
    )

    open_openings = (
        db.query(func.count(Opening.id))
        .filter(Opening.status.ilike("Open"))
        .scalar()
    )

    closed_openings = (
        db.query(func.count(Opening.id))
        .filter(Opening.status.ilike("Closed"))
        .scalar()
    )

    # Department with highest number of openings
    top_department = (
        db.query(
            Opening.department,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.department)
        .order_by(func.count(Opening.id).desc())
        .first()
    )

    # Job title with highest number of openings
    top_job_title = (
        db.query(
            Opening.job_title,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.job_title)
        .order_by(func.count(Opening.id).desc())
        .first()
    )

    # Location with highest number of openings
    top_location = (
        db.query(
            Opening.location,
            func.count(Opening.id).label("count")
        )
        .group_by(Opening.location)
        .order_by(func.count(Opening.id).desc())
        .first()
    )

    insights = []

    if total_openings > 0:
        insights.append(
            f"Total of {total_openings} openings are available."
        )

    insights.append(
        f"{open_openings} openings are currently open "
        f"and {closed_openings} are closed."
    )

    if top_department:
        insights.append(
            f"{top_department[0]} has the highest number "
            f"of openings with {top_department[1]}."
        )

    if top_job_title:
        insights.append(
            f"{top_job_title[0]} currently has "
            f"{top_job_title[1]} opening(s)."
        )

    if top_location:
        insights.append(
            f"{top_location[0]} has {top_location[1]} opening(s)."
        )

    return {
        "total_openings": total_openings,
        "open_openings": open_openings,
        "closed_openings": closed_openings,
        "top_department": (
            {
                "department": top_department[0],
                "count": top_department[1]
            }
            if top_department
            else None
        ),
        "top_job_title": (
            {
                "job_title": top_job_title[0],
                "count": top_job_title[1]
            }
            if top_job_title
            else None
        ),
        "top_location": (
            {
                "location": top_location[0],
                "count": top_location[1]
            }
            if top_location
            else None
        ),
        "insights": insights
    }