from sqlalchemy.orm import Session

from app.crud.dashboard import (
    get_admin_dashboard_stats,
    get_employee_dashboard_stats,
)
from app.models.user import User
from app.models.employee import Employee


def dashboard_service(
    db: Session,
    current_user: dict,
):

    role = str(current_user.get("role") or "").strip().lower()

    # ========================================================
    # ADMIN
    # ========================================================

    if role == "admin":
        return get_admin_dashboard_stats(db), None

    # ========================================================
    # EMPLOYEE
    # ========================================================

    if role == "employee":

        user_id = current_user.get("id")

        if user_id is None:
            return None, "User ID is missing from token."

        # Find the logged-in user
        user = db.query(User).filter(
            User.id == int(user_id)
        ).first()

        if user is None:
            return None, "User not found."

        # Find the employee profile using the user's email
        employee = db.query(Employee).filter(
            Employee.email == user.email
        ).first()

        if employee is None:
            return None, "Employee profile not found."

        dashboard_data = get_employee_dashboard_stats(
            db=db,
            user_id=user.id,
            employee_id=employee.id,
        )

        if dashboard_data is None:
            return None, "Employee profile not found."

        return dashboard_data, None

    # ========================================================
    # UNSUPPORTED ROLE
    # ========================================================

    return None, "Unsupported user role."