from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Company, Record
from django.contrib.auth.decorators import login_required
from service_desk.forms import TicketForm

def ticket_list(request):
    all_tickets = Ticket.objects.all()
    context = {'tickets': all_tickets}

    return render(request, 'service_desk/ticket_list.html', context)

def default_view(request):
    return redirect('service_desk:tickets')

# @login_required
def dashboard_view(request):
    context = {'active_page': 'dashboard'}
    return render(request, 'service_desk/dashboard.html', context)

def login_view(request):
    return render(request, 'service_desk/login.html')

@login_required
def tickets_view(request):
    all_tickets = Ticket.objects.all()
    latest_tickets = all_tickets.order_by('-last_update').filter()[:5]
    user_tickets = Ticket.objects.filter(user=request.user)

    context = {
        'active_page': 'tickets',
        'latest_tickets': latest_tickets,
        'user_tickets': user_tickets,
        'all_tickets': all_tickets
    }

    return render(request, 'service_desk/tickets.html', context)

@login_required
def create_ticket_view(request):

    if request.method == 'GET':
        form = TicketForm()
    else:
        form = TicketForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            if request.POST.get('action') == 'save_and_another':
                return redirect('service_desk:new_ticket')
            # print(instance.ticket_number)
            return redirect('service_desk:tickets')

    context = {
        'active_page': 'tickets_create',
        'form': form,
    }

    return render(request, 'service_desk/create_ticket_form.html', context)

@login_required
def ticket_detail_view(request, ticket_number):
    ticket = get_object_or_404(Ticket, ticket_number=ticket_number)
    context = {'ticket': ticket}
    return render(request, 'service_desk/ticket_detail.html', context)
