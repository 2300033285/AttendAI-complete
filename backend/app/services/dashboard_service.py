from sqlalchemy.orm import Session

from app.crud.dashboard import (
    get_admin_dashboard_stats,
    get_employee_dashboard_stats,
)


def dashboard_service(
    db: Session,
    current_user: dict,
):

    role = current_user.get("role")

    # ========================================================
    # ADMIN
    # ========================================================

    if role == "Admin":
        return get_admin_dashboard_stats(db), None

    # ========================================================
    # EMPLOYEE
    # ========================================================

    if role == "Employee":

        user_id = current_user.get("id")
        employee_id_value = current_user.get("employee_id")

        if user_id is None:
            return None, "User ID is missing from token."

        if employee_id_value is None:
            return None, "Employee profile is not linked to this user."

        try:
            employee_id = int(employee_id_value)
        except (TypeError, ValueError):
            return None, "Invalid employee ID associated with this user."

        dashboard_data = get_employee_dashboard_stats(
            db=db,
            user_id=int(user_id),
            employee_id=employee_id,
        )

        if dashboard_data is None:
            return None, "Employee profile not found."

        return dashboard_data, None

    # ========================================================
    # UNSUPPORTED ROLE
    # ========================================================

    return None, "Unsupported user role."