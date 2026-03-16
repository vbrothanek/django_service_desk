from django.db.models import OuterRef, Subquery, DateTimeField
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import RequestConfig
from .filters import TicketFilter, RecordFilter
from .models import Ticket, Company, Record, TicketReadStatus, TicketAttachment, StatusLevel
from django.contrib.auth.decorators import login_required
from service_desk.forms import TicketForm, TicketAttachmentForm, TicketDetailForm, TicketDetailFollowersForm, \
    NewRecordForm, RecordEditForm
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
        tickets = Ticket.objects.select_related('assigned_to', 'company', 'user')
    else:
        tickets = Ticket.objects.filter(
            company__in=request.user.companies.all()
        ).select_related('assigned_to', 'company', 'user')


    # ticket filters
    filter_data = request.GET.copy()

    if 'Agents' in user_groups and 'status' not in request.GET:
        filter_data.setlist('status', ['10', '20', '30', '40'])

    ticket_filter = TicketFilter(filter_data, queryset=tickets)
    tickets = ticket_filter.qs

    # Sorting before pagination
    if 'Agents' in user_groups:
        sort = request.GET.get('sort', '-last_update_internal')
    else:
        sort = request.GET.get('sort', '-last_update')
    tickets = tickets.order_by(sort)

    # Pagination
    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 20)
    paginator = Paginator(tickets, per_page=per_page)
    page = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)

    # Convert QuerySet to list
    tickets_page = list(page.object_list)

    # Load IDs of all tickets the user is following into a set
    user_followed_ids = set(request.user.followed_tickets.values_list('id', flat=True))

    # Load all read statuses for the user as a dictionary {ticket_id: last_read_at}
    read_statuses = dict(
        TicketReadStatus.objects.filter(
            user=request.user).values_list('ticket_id', 'last_read_at'))

    for ticket in tickets_page:
        # Check if the user is a participant of the ticket
        is_participant = (
                ticket.user.id == request.user.id or  # User is the ticket creator
                (
                            ticket.assigned_to and ticket.assigned_to.id == request.user.id) or  # Ticket is assigned to the user (assigned_to can be None)
                ticket.id in user_followed_ids  # User is following the ticket
        )

        if 'Agents' in user_groups:
            # Agents can see both public and internal records
            # Compare against the most recent of both timestamps
            # filter(None, ...) removes None values, max() returns the newer timestamp
            last_relevant_update = max(
                filter(None, [ticket.last_update, ticket.last_update_internal]),
                default=None
            )
        else:
            # Managers and Customers only see public records
            # Compare only against last_update
            last_relevant_update = ticket.last_update

        if (is_participant and (
                ticket.pk not in read_statuses or  # User has never read the ticket
                (last_relevant_update and last_relevant_update > read_statuses[ticket.pk]))) \
                or (ticket.status == StatusLevel.NEW and ticket.assigned_to is None):  # New ticket not yet assigned
            ticket.is_unread = True
        else:
            ticket.is_unread = False

    if 'Agents' in user_groups:
        tickets_table = TicketTable(tickets_page, order_by=sort, exclude=('last_update',))
    else:
        tickets_table = TicketTable(tickets_page, order_by=sort, exclude=('last_update_internal',))

    RequestConfig(request, paginate=False).configure(tickets_table)

    context = {
        'active_page': 'tickets',
        'tickets_table': tickets_table,
        'filter': ticket_filter,
        'page': page, # tickets
        'page_range': page_range,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'service_desk/include/tickets_table.html', context)

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
            instance.last_update = timezone.now()
            instance.last_update_internal = timezone.now()
            instance.last_updated_by = request.user
            instance.last_updated_by_internal = instance.user
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
    user_groups = request.user.groups.values_list('name', flat=True)
    is_agent = "Agents" in user_groups
    ticket = get_object_or_404(Ticket.objects.select_related('assigned_to', 'user', 'company', 'last_updated_by', 'last_updated_by_internal'),
                               ticket_number=ticket_number)

    form = TicketDetailForm(instance=ticket, is_agent=is_agent)
    form_followers = TicketDetailFollowersForm(instance=ticket)
    attachment_form = TicketAttachmentForm()
    record_form = NewRecordForm(initial={'user': request.user}, is_agent=is_agent)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # Initialize all forms with instance defaults to ensure context is always complete,
        # regardless of which form was submitted or whether validation failed.
        form = TicketDetailForm(instance=ticket, is_agent=is_agent)
        form_followers = TicketDetailFollowersForm(instance=ticket)
        attachment_form = TicketAttachmentForm()

        if form_type == 'ticket':
            form = TicketDetailForm(request.POST, instance=ticket,  is_agent=is_agent)

            if is_agent:
                form_followers = TicketDetailFollowersForm(request.POST, instance=ticket)

            form_valid = form.is_valid()
            followers_valid = form_followers.is_valid() if is_agent else True

            if form_valid and followers_valid:
                ticket = form.save(commit=False)

                if 'status' in form.changed_data and form.cleaned_data['assigned_to'] is None:
                    ticket.assigned_to = request.user

                ticket.last_update = timezone.now()
                ticket.last_update_internal = timezone.now()
                ticket.last_updated_by = request.user
                ticket.last_updated_by_internal = request.user
                ticket.save()

                if is_agent:
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
    records = Record.objects.filter(ticket_id=ticket.pk).select_related('user', 'ticket')
    records_filter = RecordFilter(request.GET, queryset=records, is_agent=is_agent)
    records = records_filter.qs.order_by(records_sorting)

    if 'Customers' in user_groups or 'Managers' in user_groups:
        records = records.filter(is_internal=False)

    # Pagination
    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 15)
    paginator = Paginator(records, per_page=per_page)
    page = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)

    records_page = list(page.object_list)

    if 'Customers' in user_groups or 'Managers' in user_groups:
        records_table = RecordTable(records_page, order_by=records_sorting,
                                    exclude=('is_internal',), current_user=request.user, is_agent=is_agent)
    else:
        records_table = RecordTable(records_page, order_by=records_sorting,
                                    current_user=request.user, is_agent=is_agent)

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
               'is_agent': is_agent,
               'records_filter': records_filter,
               'active_page': 'tickets'}

    if request.headers.get('HX-Request'):
        return render(request, 'service_desk/include/records_table.html', context)

    return render(request, 'service_desk/ticket_detail.html', context)


@login_required
def record_create_view(request, ticket_number):
    ticket = get_object_or_404(Ticket, ticket_number=ticket_number)

    if request.method == 'POST':
        is_agent = 'Agents' in request.user.groups.values_list('name', flat=True)
        form = NewRecordForm(request.POST, is_agent=is_agent)

        if form.is_valid():
            record = form.save(commit=False)
            record.ticket = ticket
            record.user = request.user
            record.save()

            return redirect('service_desk:ticket_detail', ticket_number=ticket_number)

    return redirect('service_desk:ticket_detail', ticket_number=ticket_number)

@login_required
def record_edit_view(request, ticket_number, pk):
    record = get_object_or_404(Record, pk=pk)
    is_agent = 'Agents' in request.user.groups.values_list('name', flat=True)

    if not is_agent and record.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = RecordEditForm(request.POST, instance=record, is_agent=is_agent)

        if form.is_valid():
            form.save()
            return redirect('service_desk:ticket_detail', ticket_number=ticket_number)

    else:
        form = RecordEditForm(instance=record, is_agent=is_agent)

    context = {'form': form,
               'record': record,
               'ticket_number': ticket_number,
               'is_agent': is_agent
               }

    return render(request, 'service_desk/include/record_edit_modal.html', context)


@login_required
def record_delete_view(request, ticket_number, pk):
    record = get_object_or_404(Record, pk=pk)
    is_agent = 'Agents' in request.user.groups.values_list('name', flat=True)

    if not is_agent:
      return HttpResponseForbidden()

    if request.method == 'POST':
      record.delete()
      return redirect('service_desk:ticket_detail', ticket_number=ticket_number)

    return HttpResponseForbidden()