from django.urls import path
from service_desk import views

app_name = 'service_desk'

urlpatterns = [
    path('', views.default_view),  # default_view - redirect to login or dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),  # dashboard_view
    path('tickets/', views.tickets_view, name='tickets'),  # tickets_view
    path('tickets/create/', views.create_ticket_view, name='new_ticket'),  # create_ticket_view
    path('tickets/poll/', views.tickets_poll_view, name='tickets_poll'), #Polling tickets view
    path('tickets/<int:ticket_number>', views.ticket_detail_view, name='ticket_detail'), #ticket_detail_view
    path('tickets/<int:ticket_number>/records/create/', views.record_create_view, name='record_create'), #Create new record
    path('tickets/<int:ticket_number>/records/<int:pk>/edit', views.record_edit_view, name='record_edit'), #Edit record
    path('tickets/<int:ticket_number>/records/<int:pk>/delete', views.record_delete_view, name='record_delete'), #Delete record
    path('api/company/<int:company_id>/requesters/', views.company_requesters_view, name='comapny_requestsers'), #API get company requesters
]