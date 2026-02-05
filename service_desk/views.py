from django.shortcuts import render, redirect
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
    return render(request, 'service_desk/dashboard.html')

def login_view(request):
    return render(request, 'service_desk/login.html')

@login_required
def tickets_view(request):
    all_tickets = Ticket.objects.all()
    latest_tickets = all_tickets.order_by('-last_update').filter()[:5]
    user_tickets = Ticket.objects.filter(user=request.user)

    context = {
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
            print(instance.ticket_number)
            return redirect('service_desk:tickets')


    return render(request, 'service_desk/create_ticket_form.html', {'form': form})