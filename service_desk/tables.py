from django_tables2 import Table
from .models import Ticket
from django.utils.html import format_html

class TicketTable(Table):
    class Meta:
        model = Ticket
        template_name = "django_tables2/bootstrap5.html"
        fields = ('ticket_number', 'subject', 'status', 'priority', 'assigned_to', 'last_update')
        attrs = {"class": "table table-sm table-hover"}
        """
        lambda record - for each row if record.us_unread set bold, else nothing.
        """
        row_attrs = {
            'class': lambda record: 'fw-bold' if getattr(record, 'is_unread', False) else ''
        }

    def render_status(self, value, record):
        status_classes = {
            10: 'badge bg-primary-subtle border border-primary-subtle text-primary-emphasis rounded-pill',  # New
            20: 'badge bg-light-subtle border border-light-subtle text-light-emphasis rounded-pill',  # Accepted
            30: 'badge bg-warning-subtle border border-warning-subtle text-warning-emphasis rounded-pill',  # In Progress
            40: 'badge bg-secondary-subtle border border-secondary-subtle text-secondary-emphasis rounded-pill',  # Waiting
            50: 'badge bg-success-subtle border border-success-subtle text-success-emphasis rounded-pill',  # Resolved
            60: 'badge bg-dark-subtle border border-dark-subtle text-dark-emphasis rounded-pill',  # Closed
        }
        css_class = status_classes.get(record.status, 'bg-secondary')
        return format_html('<span class="badge {}">{}</span>', css_class, value)

    def render_priority(self, value, record):
        priority_classes = {
            10: 'badge bg-success-subtle border border-success-subtle text-success-emphasis rounded-pill',  # Low
            20: 'badge bg-info-subtle border border-info-subtle text-info-emphasis rounded-pill',  # Normal
            30: 'badge bg-warning-subtle border border-warning-subtle text-warning-emphasis rounded-pill',  # High
            40: 'badge bg-danger-subtle border border-danger-subtle text-danger-emphasis rounded-pill',  # Critical
        }
        css_class = priority_classes.get(record.priority, 'bg-secondary')
        return format_html('<span class="badge {}">{}</span>', css_class, value)