import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from service_desk.models import Ticket, Company, PriorityType, StatusLevel, Record
from django import forms


class TicketFilter(django_filters.FilterSet):
    subject = django_filters.CharFilter(field_name='subject', lookup_expr='icontains', label='Subject')
    ticket_number = django_filters.CharFilter(field_name='ticket_number', lookup_expr='icontains', label='Ticket Number')
    company = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains', label='Company')
    assigned_to = django_filters.CharFilter(field_name='assigned_to__username', lookup_expr='icontains', label='Assigned To')
    created_at_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='Created from', widget=forms.DateInput(attrs={'type': 'date'}))
    created_at_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='Created to', widget=forms.DateInput(attrs={'type': 'date'}))
    last_update_from = django_filters.DateFilter(field_name='last_update', lookup_expr='gte', label='Last Update from', widget=forms.DateInput(attrs={'type': 'date'}))
    last_update_to = django_filters.DateFilter(field_name='last_update', lookup_expr='lte', label='Last Update to', widget=forms.DateInput(attrs={'type': 'date'}))
    status = django_filters.MultipleChoiceFilter(choices=StatusLevel.choices, label='Status', widget=forms.SelectMultiple(attrs={'class': 'tom-select-filter-status'}))
    priority = django_filters.MultipleChoiceFilter(choices=PriorityType.choices, label='Priority', widget=forms.SelectMultiple(attrs={'class': 'tom-select-filter-priority'}))

    class Meta:
        model = Ticket
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_tag = False
        self.form.helper.form_method = 'get'
        self.form.helper.disable_csrf = True
        self.form.helper.layout = Layout(
            Row(
                Column('ticket_number', css_class='col-12 col-md-6 col-lg-3'),
                Column('subject', css_class='col-12 col-md-6 col-lg-4'),
                Column('company', css_class='col-12 col-md-6 col-lg-4'),
            ),
            Row(
                Column('status', css_class='col-12 col-md-6 col-lg-3'),
                Column('priority', css_class='col-12 col-md-6 col-lg-3'),
                Column('assigned_to', css_class='col-12 col-md-6 col-lg-3'),
            ),
            Row(
                Column('created_at_from', css_class='col-12 col-md-6 col-lg-3'),
                Column('created_at_to', css_class='col-12 col-md-6 col-lg-3'),
                Column('last_update_from', css_class='col-12 col-md-6 col-lg-3'),
                Column('last_update_to', css_class='col-12 col-md-6 col-lg-3'),
            ))


class RecordFilter(django_filters.FilterSet):
    message = django_filters.CharFilter(field_name='message', lookup_expr='icontains', label='Message')
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains', label='User')
    created_at_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='Created from', widget=forms.DateInput(attrs={'type': 'date'}))
    created_at_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='Created to', widget=forms.DateInput(attrs={'type': 'date'}))
    is_internal = django_filters.BooleanFilter(field_name='is_internal', label='Is internal', widget=forms.Select(choices=[('', 'All'), (True, 'Yes'), (False, 'No')]))

    class Meta:
      model = Record
      exclude = []

    def __init__(self, *args, **kwargs):
      is_agent = kwargs.pop('is_agent', False)

      super().__init__(*args, **kwargs)
      self.form.helper = FormHelper()
      self.form.helper.form_tag = False
      self.form.helper.form_method = 'get'
      self.form.helper.disable_csrf = True

      if not is_agent:
          del self.form.fields['is_internal']

      if is_agent:
          self.form.helper.layout = Layout(
              Row(
                  Column('message', css_class='col-12 col-md-6 col-lg-4'),
                  Column('user', css_class='col-12 col-md-6 col-lg-3'),
                  Column('is_internal', css_class='col-12 col-md-6 col-lg-2'),
              ),
              Row(
                  Column('created_at_from', css_class='col-12 col-md-6 col-lg-3'),
                  Column('created_at_to', css_class='col-12 col-md-6 col-lg-3'),
              )
          )
      else:
          self.form.helper.layout = Layout(
              Row(
                  Column('message', css_class='col-12 col-md-6 col-lg-4'),
                  Column('user', css_class='col-12 col-md-6 col-lg-3'),
              ),
              Row(
                  Column('created_at_from', css_class='col-12 col-md-6 col-lg-3'),
                  Column('created_at_to', css_class='col-12 col-md-6 col-lg-3'),
              )
          )