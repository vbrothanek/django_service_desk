from django.shortcuts import render
from .models import Ticket, Company, Record

def ticket_list(request):
    tickets = Ticket.objects.all()
    context = {'tickets': tickets}

    return render(request, 'service_desk/ticket_list.html')
