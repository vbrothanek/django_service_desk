from django.urls import path
from . import views

app_name = 'service_desk'

urlpatterns = [
    path('ticket-list/',views.ticket_list,name='ticket_list'),
]