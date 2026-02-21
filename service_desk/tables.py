from django_tables2 import Table
from .models import Ticket
from django.utils.html import format_html
from django.urls import reverse

class TicketTable(Table):
    """
    Rendering methods for TicketTable columns.
    Django Tables2 automatically calls render_<column_name>() for each column defined in Meta.fields.

    Parameters available in each render method:
        value  - the raw value of the specific field for the current column (e.g. subject text, status integer)
        record - the entire Ticket model instance for the current row, provides access to all fields (e.g. record.ticket_number, record.status)

    Available render methods:
        render_ticket_number - renders ticket number as a link to ticket detail page
        render_subject       - renders subject as a link with truncated text (max 40 chars) and full text in tooltip
        render_status        - renders status as a Bootstrap badge with color based on status value
        render_priority      - renders priority as a Bootstrap badge with color based on priority value
    """
    class Meta:
        model = Ticket
        template_name = "django_tables2/bootstrap5.html"
        fields = ('ticket_number', 'subject', 'status', 'priority', 'assigned_to', 'created_at','last_update')
        attrs = {
            "class": "table table-sm table-hover tickets-table",
            "thead": {"class": "pt-4"},
        }
        """
        lambda record - for each row if record.us_unread set bold, else nothing.
        """
        row_attrs = {
            'class': lambda record: 'fw-bold' if getattr(record, 'is_unread', False) else ''
        }

    def render_status(self, value, record):
        status_classes = {
            10: 'bg-primary-subtle border border-primary-subtle text-primary-emphasis rounded-pill',  # New
            20: 'bg-light-subtle border border-light-subtle text-light-emphasis rounded-pill',  # Accepted
            30: 'bg-warning-subtle border border-warning-subtle text-warning-emphasis rounded-pill',  # In Progress
            40: 'bg-secondary-subtle border border-secondary-subtle text-secondary-emphasis rounded-pill',  # Waiting
            50: 'bg-success-subtle border border-success-subtle text-success-emphasis rounded-pill',  # Resolved
            60: 'bg-dark-subtle border border-dark-subtle text-dark-emphasis rounded-pill',  # Closed
        }
        css_class = status_classes.get(record.status, 'bg-secondary')
        return format_html('<span class="badge {}">{}</span>', css_class, value)

    def render_priority(self, value, record):
        priority_classes = {
            10: 'bg-success-subtle border border-success-subtle text-success-emphasis rounded-pill',  # Low
            20: 'bg-info-subtle border border-info-subtle text-info-emphasis rounded-pill',  # Normal
            30: 'bg-warning-subtle border border-warning-subtle text-warning-emphasis rounded-pill',  # High
            40: 'bg-danger-subtle border border-danger-subtle text-danger-emphasis rounded-pill',  # Critical
        }
        css_class = priority_classes.get(record.priority, 'bg-secondary')
        return format_html('<span class="badge {}">{}</span>', css_class, value)


    def render_subject(self, value, record):
        """
        Renders the subject column with truncated text.
        If the subject exceeds 40 characters, it is truncated and an ellipsis (…) is appended.
        The full text is preserved in the tooltip (title attribute) for hover visibility.
        """
        short_subject = str(value)[:40] + '...' if len(str(value)) > 40 else str(value)
        url = reverse('service_desk:ticket_detail', args=[record.ticket_number])
        return format_html('<a href="{}" class="ticket-row-link text-decoration-none" title="{}">{}</a>', url, value, short_subject)

    def render_ticket_number(self,value, record):
        url = reverse('service_desk:ticket_detail', args=[record.ticket_number])
        return format_html('<a href="{}" class="ticket-row-link text-decoration-none">{}</a>', url, value)

    def render_last_update(self, value, record):
        return value.strftime('%d.%m.%Y %H:%M')

    def render_created_at(self, value, record):
        return value.strftime('%d.%m.%Y %H:%M')