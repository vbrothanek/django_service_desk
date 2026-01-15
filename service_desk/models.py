from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Firm(models.Model):
    name = models.CharField(max_length=200)
    IC = models.CharField(max_length=10, blank=True)
    DIC = models.CharField(max_length=12, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Firm'
        verbose_name_plural = 'Firms'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=16, blank=True)
    agent_id = models.CharField(max_length=100, blank=True)
    firms = models.ManyToManyField(Firm)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.username


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('waiting', 'Waiting for customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    ticket_number = models.CharField(max_length=15, unique=True, blank=True, editable=False)
    firm = models.ForeignKey(Firm, related_name='tickets', on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='tickets', on_delete=models.PROTECT)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=5000 ,blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    assigned_to = models.ForeignKey(User, related_name='assigned_agent', on_delete=models.PROTECT, blank=True, null=True)
    supervisor = models.ForeignKey(User, related_name='supervisor', on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    due_date = models.DateField(blank=True, null=True)
    date_of_completion = models.DateField(blank=True, null=True)

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


class Record(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='records', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='records', on_delete=models.PROTECT)
    description = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Record'
        verbose_name_plural = 'Records'

    def __str__(self):
        return f"#{self.ticket.ticket_number} - {self.description}"

