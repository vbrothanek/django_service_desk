from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from .models import User, Record, Ticket
from .services import mark_existing_tickets_as_read, create_notification_receiver_list
from django.utils import timezone
from .notifications import send_new_ticket_notification, send_update_ticket_notification, send_record_notification

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
        # print('created', instance.message)
        if instance.is_internal:
            # print('internal', instance.message)
            Ticket.objects.filter(pk=instance.ticket_id).update(
                last_update_internal = timezone.now(),
                last_updated_by_internal = instance.user
            )
        else:
            # print('normal', instance.message)
            Ticket.objects.filter(pk=instance.ticket_id).update(
                last_update = timezone.now(),
                last_update_internal = timezone.now(),
                last_updated_by = instance.user,
                last_updated_by_internal = instance.user
            )


"""
send_new_ticket_notification
Signal when ticket is created send email notification to customers or agents.
"""
@receiver(post_save, sender=Ticket)
def send_ticket_mail_notification(sender, instance, created, **kwargs):
    if created:
        receivers = create_notification_receiver_list()
        send_new_ticket_notification(instance, receivers)


"""
store_old_ticket_values
Helper for send_update_mail_notification to compare statuses and assigned to before and after the save. 
"""
@receiver(pre_save, sender=Ticket)
def store_old_ticket_values(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Ticket.objects.get(pk=instance.pk)
            instance._old_status = old.status
            instance._old_assigned_to = old.assigned_to
        except Ticket.DoesNotExist:
            pass

"""
send_update_mail_notification
send email notification to customer if status or assigned to is changed.
"""
@receiver(post_save, sender=Ticket)
def send_update_mail_notification(sender, instance, created, **kwargs):
    if not created:
        status_changed = getattr(instance, '_old_status', None) != instance.status
        assigned_to = getattr(instance, '_old_assigned_to', None) != instance.assigned_to

        if status_changed or assigned_to:
            send_update_ticket_notification(instance)


@receiver(post_save, sender=Record)
def send_new_record_mail_notification(sender, instance, created, **kwargs):
    if created:
        receivers = create_notification_receiver_list()
        send_record_notification(instance, receivers)