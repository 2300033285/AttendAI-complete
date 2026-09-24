from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.referral import Referral


# =========================================================
# OVERALL REFERRAL ANALYTICS
# =========================================================

def get_referral_analytics(db: Session):

    total_referrals = (
        db.query(func.count(Referral.id))
        .scalar()
        or 0
    )

    pending_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status.ilike("Pending"))
        .scalar()
        or 0
    )

    rejected_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status.ilike("Rejected"))
        .scalar()
        or 0
    )

    accepted_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status.ilike("Accepted"))
        .scalar()
        or 0
    )

    return {
        "total_referrals": total_referrals,
        "pending_referrals": pending_referrals,
        "accepted_referrals": accepted_referrals,
        "rejected_referrals": rejected_referrals,
    }


# =========================================================
# STATUS-WISE REFERRAL ANALYTICS
# =========================================================

def get_referral_status_analytics(db: Session):

    results = (
        db.query(
            Referral.status,
            func.count(Referral.id).label("referral_count"),
        )
        .group_by(Referral.status)
        .order_by(func.count(Referral.id).desc())
        .all()
    )

    return [
        {
            "status": row.status,
            "referral_count": row.referral_count,
        }
        for row in results
    ]


# =========================================================
# EMPLOYEE-WISE REFERRAL ANALYTICS
# =========================================================

def get_employee_referral_analytics(db: Session):

    results = (
        db.query(
            Referral.employee_id,
            func.count(Referral.id).label("referral_count"),
        )
        .group_by(Referral.employee_id)
        .order_by(func.count(Referral.id).desc())
        .all()
    )

    return [
        {
            "employee_id": row.employee_id,
            "referral_count": row.referral_count,
        }
        for row in results
    ]


# =========================================================
# OPENING-WISE REFERRAL ANALYTICS
# =========================================================

def get_opening_referral_analytics(db: Session):

    results = (
        db.query(
            Referral.opening_id,
            func.count(Referral.id).label("referral_count"),
        )
        .group_by(Referral.opening_id)
        .order_by(func.count(Referral.id).desc())
        .all()
    )

    return [
        {
            "opening_id": row.opening_id,
            "referral_count": row.referral_count,
        }
        for row in results
    ]


# =========================================================
# MONTHLY REFERRAL ANALYTICS
# =========================================================

def get_monthly_referral_analytics(db: Session):

    results = (
        db.query(
            extract("year", Referral.created_at).label("year"),
            extract("month", Referral.created_at).label("month"),
            func.count(Referral.id).label("referral_count"),
        )
        .group_by(
            extract("year", Referral.created_at),
            extract("month", Referral.created_at),
        )
        .order_by(
            extract("year", Referral.created_at),
            extract("month", Referral.created_at),
        )
        .all()
    )

    return [
        {
            "year": int(row.year),
            "month": int(row.month),
            "referral_count": row.referral_count,
        }
        for row in results
    ]