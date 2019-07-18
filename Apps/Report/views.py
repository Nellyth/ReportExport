import os
from celery import chord
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView, FormView
from Apps.Report.models import Customers, FileParser
from Apps.Report.forms import CustomerForm, FileForm, SearchForm, DownloadForm
from django.urls import reverse_lazy
from django.shortcuts import render
from Apps.Report.tasks import excel_report, send_email
from ReportExporter import settings


def index(request):
    return render(request, 'index.html')


class RegisterCustomer(CreateView):
    model = Customers
    template_name = 'Tp_customer.html'
    form_class = CustomerForm
    success_url = reverse_lazy('File')


class RegisterFile(CreateView):
    model = FileParser
    template_name = 'File.html'
    form_class = FileForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            customer = Customers.objects.get(pk=request.POST.get('customer'))
            file.customer = customer
            file.parser = customer.parser
            file.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class Search(FormView):
    template_name = 'SearchReport.html'
    form_class = SearchForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        data = form.cleaned_data
        if data.get('customer'):
            data['customer'] = data.get('customer').id
        chord(excel_report.s(data=data))(send_email.s())
        return super().form_valid(form)


class DownloadReport(FormView):
    template_name = 'DownloadRepoter.html'
    form_class = DownloadForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        data = form.cleaned_data
        if data:
            file_path = os.path.join(settings.MEDIA_ROOT_EXCEL)
            file_path = '{}/{}.{}'.format(file_path, self.request.POST['key'], 'xlsx')
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
            return super().form_valid(form)
