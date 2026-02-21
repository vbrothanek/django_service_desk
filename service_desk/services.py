from .models import Ticket, TicketReadStatus
import os
from django import forms

def mark_existing_tickets_as_read(user):
    """
    Mark all existing tickets as read
    """
    existing_tickets = Ticket.objects.filter(
        company__in = user.companies.all()
    )

    statuses = []
    for ticket in existing_tickets:
        status = TicketReadStatus(
            ticket = ticket,
            user = user,
        )
        statuses.append(status)

    TicketReadStatus.objects.bulk_create(statuses, ignore_conflicts=True)


def validate_attachment(file):
    """
    Validate attachment file in ticket creation.
    """
    if not file:
        return file

    ALLOWED_TYPES = {
        'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml',
        'video/mp4', 'video/mpeg', 'video/quicktime', 'video/x-msvideo',
        'audio/mpeg', 'audio/wav', 'audio/ogg',
        'text/csv', 'application/pdf',
        'application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed',
    }

    ALLOWED_EXTENSIONS = [
        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg',
        '.mp4', '.mpeg', '.mov', '.avi',
        '.mp3', '.wav', '.ogg',
        '.csv', '.pdf',
        '.zip', '.rar', '.7z',
    ]

    MAX_FILE_SIZE = 30 * 1024 * 1024

    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise forms.ValidationError(f'Uploaded file extension ({ext}) is not allowed.')

    if file.content_type not in ALLOWED_TYPES:
        raise forms.ValidationError('Uploaded file is not allowed.')

    if file.size > MAX_FILE_SIZE:
        raise forms.ValidationError(f'Uploaded file is too large. Max file size is {MAX_FILE_SIZE}.')

    return file