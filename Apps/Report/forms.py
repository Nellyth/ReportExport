import os

from django import forms
from django.conf import settings

from Apps.Report.models import Customers, FileParser
from Apps.Report.choices import select_parser_customers, select_options_file_parser, select_options_filter_by
from datetime import datetime


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = [
            'name',
            'parser'
        ]
        labels = {
            'name': 'Name',
            'parser': 'Parser',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parser': forms.Select(choices=select_parser_customers, attrs={'class': 'form-control'}),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = FileParser
        fields = [
            'customer',
            'emailID',
            'email_date',
            'options',
            'sent',
            'file',
        ]
        labels = {
            'customer': 'Customer',
            'emailID': 'Email ID',
            'email_date': 'Email Date',
            'options': 'Options',
            'sent': 'Sent',
            'file': 'File',
        }
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'emailID': forms.NumberInput(attrs={'class': 'form-control'}),
            'email_date': forms.DateTimeInput(
                attrs={'type': 'date', 'class': 'form-control', 'min': datetime.now().strftime('%Y-%m-%d')}),
            'options': forms.Select(choices=select_options_file_parser, attrs={'class': 'form-control'}),
            'sent': forms.CheckboxInput(attrs={'class': 'form-check', 'style': 'width: 20px; height: 20px;'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class SearchForm(forms.Form):
    filter_by = forms.CharField(label='Filter By', required=False, max_length=20,
                                widget=forms.Select(choices=select_options_filter_by, attrs={'class': 'form-control'}))
    start_date = forms.DateField(label='Start date', required=False,
                                 widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    final_date = forms.DateField(label='Final date', required=False,
                                 widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    email_id = forms.IntegerField(label='Email ID', required=False,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    customer = forms.ModelChoiceField(label='Customer', queryset=Customers.objects.all(), required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    sent = forms.BooleanField(label='Sent', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check', 'style': 'width: 20px; height: 20px;'}))

    def clean(self):
        start_date = self.cleaned_data['start_date']
        final_date = self.cleaned_data['final_date']
        email_id = self.cleaned_data['email_id']
        customer = self.cleaned_data['customer']

        if not email_id and not customer and not start_date and not final_date:
            raise forms.ValidationError("Must fill out a field to do the search")


class DownloadForm(forms.Form):
    key = forms.CharField(max_length=50, label='Key',
                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_key(self):
        key = self.cleaned_data['key']

        if not key:
            raise forms.ValidationError("The key field can not be empty")
        else:
            file_path = os.path.join(settings.MEDIA_ROOT_EXCEL)
            file_path = '{}/{}.{}'.format(file_path, key, 'xlsx')
            if not os.path.exists(file_path):
                raise forms.ValidationError("The file you want to download does not exist")
