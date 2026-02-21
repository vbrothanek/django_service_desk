from django.contrib.auth.models import AbstractUser
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    ic = models.CharField(max_length=10, blank=True)
    dic = models.CharField(max_length=12, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone = models.CharField(max_length=16, blank=True)
    companies = models.ManyToManyField(Company)


class PriorityType(models.IntegerChoices):
    LOW = 10, 'Low'
    NORMAL = 20, 'Normal'
    HIGH = 30, 'High'
    CRITICAL = 40, 'Critical'


class StatusLevel(models.IntegerChoices):
    NEW = 10,'New'
    ACCEPTED = 20,'Accepted'
    IN_PROGRESS = 30,'In Progress'
    WAITING = 40,'Waiting'
    RESOLVED = 50,'Resolved'
    CLOSED = 60,'Closed'


class Ticket(models.Model):
    ticket_number = models.CharField(max_length=15, unique=True, blank=True, editable=False)
    company = models.ForeignKey(Company, related_name='tickets', on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='created_tickets', on_delete=models.PROTECT)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=5000 ,blank=False)
    status = models.IntegerField(choices=StatusLevel, default=StatusLevel.NEW)
    priority = models.IntegerField(choices=PriorityType, default=PriorityType.NORMAL)
    assigned_to = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    due_date = models.DateField(blank=True, null=True)
    date_of_completion = models.DateField(blank=True, null=True)
    # attachment = models.FileField(upload_to='tickets/attachments/%Y/%m/%d' ,blank=True, null=True)

    def save(self, *args, **kwargs):
        '''
        Custom save method to save ticket with custom ticket number.
        At the end of method we call super() which calls superior class Model to save the ticket.
        '''
        if not self.ticket_number:
            from datetime import date

            current_year = str(date.today().year)[-2:]
            count = Ticket.objects.filter(ticket_number__startswith=current_year).count()
            number_of_next_ticket = count + 1
            self.ticket_number = f'{current_year}{number_of_next_ticket:04d}'

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f"#{self.ticket_number} - {self.subject}"


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_name = models.CharField(max_length=200)
    file = models.FileField(upload_to='tickets/attachments/%Y/%m/%d')

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'

    def __str__(self):
        return self.original_name



class Record(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='records', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ticket_records', on_delete=models.PROTECT)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Record'
        verbose_name_plural = 'Records'

    def __str__(self):
        return f"#{self.ticket.ticket_number} - {self.message}"


class TicketReadStatus(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='read_status', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ticket_reads', on_delete=models.CASCADE)
    last_read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ticket', 'user')

    def __str__(self):
        return f"{self.user} - {self.ticket} ({self.last_read_at})"



