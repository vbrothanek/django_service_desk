# from django import forms
# from service_desk.models import Ticket, Record
#
# """
# 1. vykresleni formulare
# 2. uzivatel vyplni data
# 3. uzivatel odesle formular
# 4. server dostane data
# 5. server, kontrola dat
# 6. Form is valid > ulozi zaznam > vrati uzivateli OK stranku
#
# 7. Form is invalid > vykresleni formulare + zobrazeni chyb
# """
#
# class TicketForm(forms.ModelForm):
#     class Meta:
#          model = Ticket
#          fields = ['company', 'subject', 'description', 'priority', 'due_date', 'attachment']

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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
