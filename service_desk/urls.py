from django.urls import path
from service_desk import views

app_name = 'service_desk'

urlpatterns = [
    path('', views.default_view),  # default_view - redirect to login or dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),  # dashboard_view
    path('tickets/', views.tickets_view, name='tickets'),  # tickets_view
    path('tickets/create/', views.create_ticket_view, name='new_ticket'),  # create_ticket_view
    path('tickets/<int:ticket_number>', views.ticket_detail_view, name='ticket_detail'), #ticket_detail_view
    # path('settings/', test_view),
    # path('settings/users/', test_view),
    # path('settings/users/add/', test_view),
    # path('settings/users/<int:pk>/edit/', test_view),
    # path('settings/users/<int:pk>/delete/', test_view),
    # path('settings/companies/', test_view),
    # path('settings/companies/add/', test_view),
    # path('settings/companies/<int:pk>/edit/', test_view),
    # path('settings/companies/<int:pk>/delete/', test_view),
]