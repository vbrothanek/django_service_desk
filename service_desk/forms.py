from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from service_desk.models import Ticket, Record

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['company', 'subject', 'description', 'priority', 'due_date', 'attachment']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'company': forms.Select(attrs={'class': 'tom-select-company', 'placeholder': 'Select company...'}),
            'priority': forms.Select(attrs={'class': 'tom-select-priority'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = ''
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('company', css_class='col-6'),
                Column('priority', css_class='col-6'),
            ),
            'subject',
            'description',
            Row(
                Column('due_date', css_class='col-6'),
                Column('attachment', css_class='col-6'),
            ),
        )
