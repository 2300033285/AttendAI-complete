from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.referral import Referral


def get_referral_insights(db: Session):

    total_referrals = (
        db.query(func.count(Referral.id))
        .scalar()
        or 0
    )

    pending_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status == "Pending")
        .scalar()
        or 0
    )

    reviewed_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status == "Reviewed")
        .scalar()
        or 0
    )

    rejected_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status == "Rejected")
        .scalar()
        or 0
    )

    selected_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status == "Selected")
        .scalar()
        or 0
    )

    if total_referrals > 0:
        selection_rate = round(
            (selected_referrals / total_referrals) * 100,
            2
        )

        pending_rate = round(
            (pending_referrals / total_referrals) * 100,
            2
        )
    else:
        selection_rate = 0
        pending_rate = 0

    return {
        "total_referrals": total_referrals,
        "pending_referrals": pending_referrals,
        "reviewed_referrals": reviewed_referrals,
        "rejected_referrals": rejected_referrals,
        "selected_referrals": selected_referrals,
        "selection_rate": selection_rate,
        "pending_rate": pending_rate,
    }