from django import forms
from service_desk.models import Ticket, Record

"""
1. vykresleni formulare
2. uzivatel vyplni data
3. uzivatel odesle formular
4. server dostane data
5. server, kontrola dat
6. Form is valid > ulozi zaznam > vrati uzivateli OK stranku

7. Form is invalid > vykresleni formulare + zobrazeni chyb
"""

class TicketForm(forms.ModelForm):
    class Meta:
         model = Ticket
         fields = ['company', 'subject', 'description', 'priority', 'due_date', 'attachment']
