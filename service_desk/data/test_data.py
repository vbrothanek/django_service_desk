from service_desk.models import Ticket, Company, User


def create_ticket():
    try:
        company = Company.objects.get(name='Spolecnost 03 a.s.')
    except Company.DoesNotExist:
        print('Company does not exist')
        return

    try:
        user = User.objects.get(username='duser')
    except User.DoesNotExist:
        print('User does not exist')
        return

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

    print(f'Total: {Ticket.objects.count()} tickets')