from datetime import date
# ---------------- DISPLAY STATUS ----------------
def get_display_status(status, start_date, end_date):
    today = date.today()
    status = (status or "").lower()

    if status == "approved":
        if start_date <= today <= end_date:
            return "on-leave"
        elif today > end_date:
            return "completed"

    return status
