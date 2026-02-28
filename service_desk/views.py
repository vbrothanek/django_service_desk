from django.db.models import OuterRef, Subquery, DateTimeField
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import RequestConfig
from .models import Ticket, Company, Record, TicketReadStatus, TicketAttachment
from django.contrib.auth.decorators import login_required
from service_desk.forms import TicketForm, TicketAttachmentForm, TicketDetailForm, TicketDetailFollowersForm
from django.core.paginator import Paginator
from .tables import TicketTable


@login_required
def default_view(request):
    return redirect('service_desk:dashboard')


@login_required
def dashboard_view(request):
    context = {'active_page': 'dashboard'}
    return render(request, 'service_desk/dashboard.html', context)


@login_required
def tickets_view(request):
    user_groups = request.user.groups.values_list('name', flat=True)

    if 'Agents' in user_groups:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(
            company__in=request.user.companies.all()
        )

    # Sorting before pagination
    sort = request.GET.get('sort', '-last_update')
    tickets = tickets.order_by(sort)

    # Pagination
    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 20)
    paginator = Paginator(tickets, per_page=per_page)
    page = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)

    tickets_page = list(page.object_list)

    user_followed_ids = set(request.user.followed_tickets.values_list('id', flat=True))

    read_statuses = dict(
        TicketReadStatus.objects.filter(
            user=request.user).values_list('ticket_id', 'last_read_at'))

    for ticket in tickets_page:
        is_participant = (
                ticket.user.id == request.user.id or
                (ticket.assigned_to and ticket.assigned_to.id == request.user.id) or
                ticket.id in user_followed_ids
        )

        if is_participant and (ticket.pk not in read_statuses or ticket.last_update > read_statuses[ticket.pk]):
            ticket.is_unread = True
        else:
            ticket.is_unread = False

    table = TicketTable(tickets_page, order_by=sort)
    RequestConfig(request, paginate=False).configure(table)

    context = {
        'active_page': 'tickets',
        'table': table,
        'page': page,
        'page_range': page_range,
    }

    return render(request, 'service_desk/tickets.html', context)



@login_required
def create_ticket_view(request):
    user_groups = request.user.groups.values_list('name', flat=True)

    # Specify the queryset of company by the role of the user.
    if 'Agents' in user_groups:
        companies = Company.objects.filter(is_active=True)
    else:
        companies = request.user.companies.filter(is_active=True)


    if request.method == 'GET':
        form = TicketForm()
        form.fields['company'].queryset = companies

        # If user only have access to one company, automatically fill the filed
        if companies.count() == 1:
            form.fields['company'].initial = companies.first()

        attachment_form = TicketAttachmentForm()
    else:
        form = TicketForm(request.POST)
        form.fields['company'].queryset = companies
        attachment_form = TicketAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            for file in request.FILES.getlist('file'):
                TicketAttachment.objects.create(
                    ticket = instance,
                    file = file,
                    original_name = file.name,
                    uploaded_by = request.user,
                )

            if request.POST.get('action') == 'save_and_another':
                return redirect('service_desk:new_ticket')
            return redirect('service_desk:ticket_detail', ticket_number=instance.ticket_number)

    context = {
        'active_page': 'tickets_create',
        'form': form,
        'attachment_form': attachment_form,
    }

    return render(request, 'service_desk/create_ticket_form.html', context)


@login_required
def ticket_detail_view(request, ticket_number):
    ticket = get_object_or_404(Ticket, ticket_number=ticket_number)

    #Update Read Status when user involved in ticket opened the ticket.
    TicketReadStatus.objects.update_or_create(
        ticket = ticket,
        user = request.user,
        defaults = {
            'last_read_at': timezone.now(),
        }
    )

    form = TicketDetailForm(instance=ticket)
    form_followers = TicketDetailFollowersForm(instance=ticket)

    context = {'ticket': ticket,
               'ticket_entry': form,
               'followers': form_followers,
               'active_page': 'tickets'}

    return render(request, 'service_desk/ticket_detail.html', context)
