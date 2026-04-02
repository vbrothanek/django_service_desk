from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

def _send_email(subject, context, template, recipients):
    html_message = render_to_string(template, context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=context['ticket'].description,
        from_email=None,
        to=recipients,
    )

    email.attach_alternative(html_message, 'text/html')
    email.send(fail_silently=True)


def send_new_ticket_notification(instance, receivers):
    ticket_url = f"{settings.SITE_URL}{reverse('service_desk:ticket_detail', args=[instance.ticket_number])}"
    subject = f"[#{instance.ticket_number}] {instance.subject}"
    context = {
        'ticket': instance,
        'ticket_url': ticket_url
    }

    if instance.user.groups.filter(name__in=['Managers' ,'Customers']).exists():

        if instance.requester and instance.requester.email_notifications:
            # Email to customer
            _send_email(subject, context, 'service_desk/email/ticket_created_customer.html', [instance.requester.email])

        # Email to agent or central email
        _send_email(subject, context, 'service_desk/email/ticket_created_agent.html', receivers)

    elif instance.user.groups.filter(name__in=['Agents', 'Admins']).exists():
        if instance.requester and instance.requester.email_notifications:
            # Email to customer
            _send_email(subject, context, 'service_desk/email/ticket_created_customer.html', [instance.requester.email])


def send_update_ticket_notification(instance):
    ticket_url = f"{settings.SITE_URL}{reverse('service_desk:ticket_detail', args=[instance.ticket_number])}"
    subject = f"[#{instance.ticket_number}] {instance.subject}"
    context = {
        'ticket': instance,
        'ticket_url': ticket_url
    }

    if instance.requester and instance.requester.email_notifications:
        _send_email(subject, context, 'service_desk/email/ticket_updated_customer.html', [instance.requester.email])


def send_record_notification(instance, receivers):
    ticket_url = f"{settings.SITE_URL}{reverse('service_desk:ticket_detail', args=[instance.ticket.ticket_number])}"
    subject = f"[#{instance.ticket.ticket_number}] {instance.ticket.subject}"
    context = {
        'ticket': instance.ticket,
        'ticket_url': ticket_url,
        'record': instance
    }

    if instance.user.groups.filter(name__in=['Managers', 'Customers']).exists():
        _send_email(subject, context, 'service_desk/email/record_created_agent.html', receivers)

    elif instance.user.groups.filter(name__in=['Agents', 'Admins']).exists():
        if instance.ticket.requester and instance.ticket.requester.email_notifications:
            _send_email(subject, context, 'service_desk/email/record_created_customer.html', [instance.ticket.requester.email])