from django.shortcuts import render, redirect
from .models import Ticket, Company, Record
from django.contrib.auth.decorators import login_required

def ticket_list(request):
    all_tickets = Ticket.objects.all()
    context = {'tickets': all_tickets}

    return render(request, 'service_desk/ticket_list.html', context)

def default_view(request):
    return redirect('/')

# @login_required
def dashboard_view(request):
    return render(request, 'service_desk/dashboard.html')

def login_view(request):
    return render(request, 'service_desk/login.html')

def tickets_view(request):
    all_tickets = Ticket.objects.all()
    latest_tickets = all_tickets.order_by('-last_update').filter()[:5]
    return render(request, 'service_desk/tickets.html', {'all_tickets': all_tickets,'latest_tickets': latest_tickets})

def create_ticket_view(request):
    return render(request, 'service_desk/create_ticket.html')