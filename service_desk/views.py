from django.db.models import OuterRef, Subquery, DateTimeField
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import RequestConfig
from .models import Ticket, Company, Record, TicketReadStatus, TicketAttachment, StatusLevel
from django.contrib.auth.decorators import login_required
from service_desk.forms import TicketForm, TicketAttachmentForm, TicketDetailForm, TicketDetailFollowersForm, \
    NewRecordForm
from django.core.paginator import Paginator
from .tables import TicketTable, RecordTable


@login_required
def default_view(request):
    return redirect('service_desk:dashboard')


@login_required
def dashboard_view(request):
    per_fetch = 5
    data = Ticket.objects.values('company', 'company__name', 'ticket_number', 'assigned_to', 'user')
    data = list(data[:per_fetch])

    next_url = f'/api-htmx/?startFrom={per_fetch}' if len(data) == per_fetch else None

    context = {
        'active_page': 'dashboard',
        'data': data,
        'next': next_url
    }
    return render(request, 'service_desk/dashboard.html', context)


@login_required
def api_json(request):
    per_fetch = 5

    start_from = int(request.GET.get('startFrom') or 0)
    until = start_from + per_fetch

    data = Ticket.objects.values('company', 'company__name', 'ticket_number', 'assigned_to', 'user')
    data = list(data[start_from:until])

    if len(data) < per_fetch:
        next_url = None
    else:
        next_url = f'/api/?startFrom={str(until)}'

    return JsonResponse({
        'data': data,
        'next': next_url
    })

@login_required
def api_htmx(request):
    per_fetch = 5

    start_from = int(request.GET.get('startFrom') or 0)
    until = start_from + per_fetch

    data = Ticket.objects.values('company', 'company__name', 'ticket_number', 'assigned_to', 'user')
    data = list(data[start_from:until])

    if len(data) < per_fetch:
        next_url = None
    else:
        next_url = f'/api-htmx/?startFrom={str(until)}'


    return render(request, 'service_desk/include/dashboard_htmx.html', {
        'data': data,
        'next': next_url
    })


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
                ticket.user.id == request.user.id or                                    # Check if user is the ticket creator
                (ticket.assigned_to and ticket.assigned_to.id == request.user.id) or    # Check if ticket is assigned to user (assigned_to can be None)
                ticket.id in user_followed_ids                                          # Check if user is following the ticket
        )

        if (is_participant and (ticket.pk not in read_statuses or ticket.last_update > read_statuses[ticket.pk])) \
                or (ticket.status == StatusLevel.NEW and ticket.assigned_to is None):
            ticket.is_unread = True
        else:
            ticket.is_unread = False

    tickets_table = TicketTable(tickets_page, order_by=sort)
    RequestConfig(request, paginate=False).configure(tickets_table)

    context = {
        'active_page': 'tickets',
        'tickets_table': tickets_table,
        'page': page, # tickets
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
    ticket = get_object_or_404(Ticket.objects.select_related('assigned_to', 'user', 'company'),
                               ticket_number=ticket_number)

    form = TicketDetailForm(instance=ticket)
    form_followers = TicketDetailFollowersForm(instance=ticket)
    attachment_form = TicketAttachmentForm()
    record_form = NewRecordForm(initial={'user': request.user})

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # Initialize all forms with instance defaults to ensure context is always complete,
        # regardless of which form was submitted or whether validation failed.
        form = TicketDetailForm(instance=ticket)
        form_followers = TicketDetailFollowersForm(instance=ticket)
        attachment_form = TicketAttachmentForm()

        if form_type == 'ticket':
            form = TicketDetailForm(request.POST, instance=ticket)
            form_followers = TicketDetailFollowersForm(request.POST, instance=ticket)

            if form.is_valid() and form_followers.is_valid():
                ticket = form.save(commit=False)

                if 'status' in form.changed_data and form.cleaned_data['assigned_to'] is None:
                    ticket.assigned_to = request.user

                ticket.save()
                form_followers.save()

                return redirect('service_desk:ticket_detail', ticket_number=ticket_number)

        elif form_type == 'attachments':
            attachment_form = TicketAttachmentForm(request.POST, request.FILES)

            if attachment_form.is_valid():
                for file in attachment_form.cleaned_data['file']:
                    TicketAttachment.objects.create(
                        ticket=ticket,
                        file=file,
                        original_name=file.name,
                        uploaded_by=request.user
                    )

                return redirect('service_desk:ticket_detail', ticket_number=ticket_number)


    #Update Read Status when user involved in ticket opened the ticket.
    TicketReadStatus.objects.update_or_create(
        ticket = ticket,
        user = request.user,
        defaults = {
            'last_read_at': timezone.now(),
        }
    )

    records_sorting = request.GET.get('sort', '-created_at')
    records = Record.objects.filter(ticket_id=ticket.pk).select_related('user').order_by(records_sorting)

    # Pagination
    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 15)
    paginator = Paginator(records, per_page=per_page)
    page = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)

    records_page = list(page.object_list)

    records_table = RecordTable(records_page, order_by=records_sorting)
    RequestConfig(request, paginate=False).configure(records_table)

    context = {'ticket': ticket,
               'ticket_entry': form,
               'followers': form_followers,
               'attachment_form': attachment_form,
               'record_form': record_form,
               'records_table': records_table,
               'page': page,  # records
               'page_range': page_range,
               'per_page': per_page,
               'active_page': 'tickets'}

    if request.headers.get('HX-Request'):
        return render(request, 'service_desk/include/records_table.html', context)

    return render(request, 'service_desk/ticket_detail.html', context)


@login_required
def record_create_view(request, ticket_number):
    ticket = get_object_or_404(Ticket, ticket_number=ticket_number)

    if request.method == 'POST':
        form = NewRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            print(record.ticket_id, record.user, record.message)
            record.ticket = ticket
            record.user = request.user
            record.save()

            return redirect('service_desk:ticket_detail', ticket_number=ticket_number)

    return redirect('service_desk:ticket_detail', ticket_number=ticket_number)

