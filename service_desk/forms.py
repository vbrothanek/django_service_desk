from crispy_forms.templatetags.crispy_forms_field import css_class
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from service_desk.models import Ticket, Record, TicketAttachment
from service_desk.services import validate_attachment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['company', 'subject', 'description', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'company': forms.Select(attrs={'class': 'tom-select-company', 'placeholder': 'Select company...'}),
            'priority': forms.Select(attrs={'class': 'tom-select-priority'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = ''
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('company', css_class='col-4'),
                Column('priority', css_class='col-2')),
            Row(Column('subject', css_class='col-6')),
            Row(Column('description', css_class='col-6')),
            Row(Column('due_date', css_class='col-2')),
            )



"""
Upload multiple file input by official documentation of Django. 
"""

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class TicketAttachmentForm(forms.Form):
    file = MultipleFileField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('file', css_class='col-3 pb-3'),
            )
        )

    def clean_file(self):
        files = self.cleaned_data.get('file')
        if not files:
            return files
        result = []
        for file in files:
            validated = validate_attachment(file)
            result.append(validated)
        return result