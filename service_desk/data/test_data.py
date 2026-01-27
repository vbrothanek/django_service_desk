from service_desk.models import Ticket, Company
from django.contrib.auth.models import User


def create_ticket():
    try:
        company = Company.objects.get(name='Treti spolecnost v HD')
    except Company.DoesNotExist:
        print(f'Company does not exist')

    try:
        user = User.objects.get(username='duser')
    except User.DoesNotExist:
        print(f'User does not exist')

    for n in range(100, 120):
        print(n)

        Ticket.objects.create(
            subject=f'Ticket #99{n}',
            description=f'Ticket #99{n} - some description that is provided.',
            status=10,
            priority=20,
            company=company,
            user=user
        )
        print(f'created ticket {n}')

    print(f': {Ticket.objects.count()} tickets')