from .models import Ticket, TicketReadStatus

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