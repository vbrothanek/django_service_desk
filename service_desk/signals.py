from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import User, Record, Ticket
from .services import mark_existing_tickets_as_read
from django.utils import timezone

"""
user_added_to_company
Signal to automatically mark all existing tickets as read for a user
when they are added to a company.

@receiver listens to m2m_changed signal on User.companies relationship.
'post_add' means the function runs after the company is added to the user.
"""

@receiver(m2m_changed, sender=User.companies.through)
def user_added_to_company(sender, instance, action, **kwargs):
    # print(f"Signal fired! Action: {action}, User: {instance}")
    if action == 'post_add':
        # print("post_add - marking tickets as read")
        mark_existing_tickets_as_read(instance)


"""
update_ticket_last_update
Signal when record is created update timestamp to ticket last update.
"""
@receiver(post_save, sender=Record)
def update_ticket_last_update(sender, instance, created, **kwargs):
    if created:
        Ticket.objects.filter(pk=instance.ticket_id).update(last_update=timezone.now())