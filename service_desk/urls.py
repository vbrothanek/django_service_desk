'''
URLs:

Login page
/login/


User site part
Dahsboard page
/dashboard/

All tickets
/tickets/

Detail about ticket
/tickets/{ticket_number}/

Create new ticket
/tickets/create/

User settings page
/settings/

Companies - statistics
/statistics/


Admin site part
Add User, edit, list, delete
/settings/users/
/settings/users/add/
/settings/users/pk/edit/
/settings/users/pk/delete/

Add company, edit, list, delete
/settings/companies/
/settings/companies/add/
/settings/companies/pk/edit/
/settings/companies/pk/delete/
'''

from django.urls import path
from service_desk import views

def test_view(request):
    from django.shortcuts import HttpResponse
    return HttpResponse('Test page: ' + request.path)

app_name = 'service_desk'

urlpatterns = [
    path('ticket-list/', views.ticket_list, name='ticket-list'),
    path('', views.default_view),  # default_view - redirect to login or dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),  # dashboard_view
    path('tickets/', views.tickets_view, name='tickets'),  # tickets_view
    path('tickets/create/', views.create_ticket_view, name='new_ticket'),  # create_ticket_view
    path('tickets/<int:ticket_number>', views.ticket_detail_view, name='ticket_detail'), #ticket_detail_view
    path('settings/', test_view),
    path('settings/users/', test_view),
    path('settings/users/add/', test_view),
    path('settings/users/<int:pk>/edit/', test_view),
    path('settings/users/<int:pk>/delete/', test_view),
    path('settings/companies/', test_view),
    path('settings/companies/add/', test_view),
    path('settings/companies/<int:pk>/edit/', test_view),
    path('settings/companies/<int:pk>/delete/', test_view),
]