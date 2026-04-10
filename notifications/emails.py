from django.core.mail import send_mail
from django.conf import settings


def _send(subject, message, recipient_email):
    """Send a single email, silently skip if no recipient email."""
    if not recipient_email:
        return
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=True,
        )
    except Exception:
        pass


# ── Attendance ────────────────────────────────────────────────────────────────

def notify_absent(student, date, marked_by=''):
    """Email parent when student is marked absent."""
    parent = student.parent_user
    if not parent or not parent.email:
        return

    subject = f"Attendance Alert — {student.full_name()} was absent on {date}"
    message = (
        f"Dear {parent.get_full_name() or parent.username},\n\n"
        f"This is to inform you that your child {student.full_name()} "
        f"(Roll No: {student.roll_number}, Class {student.student_class}-{student.section}) "
        f"was marked ABSENT on {date}.\n\n"
        f"If this is incorrect, please contact the school.\n\n"
        f"Regards,\nEduTrack — School Management System"
    )
    _send(subject, message, parent.email)


def notify_late(student, date):
    """Email parent when student is marked late."""
    parent = student.parent_user
    if not parent or not parent.email:
        return

    subject = f"Attendance Notice — {student.full_name()} arrived late on {date}"
    message = (
        f"Dear {parent.get_full_name() or parent.username},\n\n"
        f"Your child {student.full_name()} (Roll No: {student.roll_number}) "
        f"was marked LATE on {date}.\n\n"
        f"Regards,\nEduTrack — School Management System"
    )
    _send(subject, message, parent.email)


# ── Fees ──────────────────────────────────────────────────────────────────────

def notify_fee_due(student, fee_payment):
    """Email student (and parent) about a pending fee."""
    balance = fee_payment.balance()
    fee_type = fee_payment.fee_structure.fee_type if fee_payment.fee_structure else "Fee"

    subject = f"Fee Reminder — {fee_type} due for {student.full_name()}"
    message = (
        f"Dear {student.full_name()},\n\n"
        f"This is a reminder that your {fee_type} payment is pending.\n\n"
        f"  Amount Due  : ₹{fee_payment.amount_due}\n"
        f"  Amount Paid : ₹{fee_payment.amount_paid}\n"
        f"  Balance     : ₹{balance}\n"
        f"  Status      : {fee_payment.status.title()}\n\n"
        f"Please clear the dues at the earliest.\n\n"
        f"Regards,\nEduTrack — School Management System"
    )

    # Email student's linked user account
    if student.user and student.user.email:
        _send(subject, message, student.user.email)

    # Also email parent
    if student.parent_user and student.parent_user.email:
        parent_msg = message.replace(
            f"Dear {student.full_name()},",
            f"Dear {student.parent_user.get_full_name() or student.parent_user.username},"
        )
        _send(subject, parent_msg, student.parent_user.email)


def notify_fee_paid(student, fee_payment):
    """Email student confirming fee payment."""
    fee_type = fee_payment.fee_structure.fee_type if fee_payment.fee_structure else "Fee"

    subject = f"Payment Confirmed — {fee_type} for {student.full_name()}"
    message = (
        f"Dear {student.full_name()},\n\n"
        f"Your {fee_type} payment has been recorded successfully.\n\n"
        f"  Amount Paid  : ₹{fee_payment.amount_paid}\n"
        f"  Receipt No   : {fee_payment.receipt_number or 'N/A'}\n"
        f"  Payment Date : {fee_payment.payment_date or 'N/A'}\n\n"
        f"Thank you!\n\n"
        f"Regards,\nEduTrack — School Management System"
    )

    if student.user and student.user.email:
        _send(subject, message, student.user.email)
