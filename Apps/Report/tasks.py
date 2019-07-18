from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from Apps.Report.models import FileParser
from ReportExporter.celery import app as celery_app
import pandas as pd
import uuid


@celery_app.task
def excel_report(**kwargs) -> str:
    data = kwargs.get('data')
    queryset = FileParser.objects.filter()
    if data.get('filter_by') == 'email_date':
        if data.get('start_date'):
            queryset = queryset.filter(createAdd__gte=data.get('start_date'))
        if data.get('final_date'):
            queryset = queryset.filter(createAdd__lte=data.get('start_date'))
    elif data.get('filter_by') == 'custom_date':
        if data.get('start_date'):
            queryset = queryset.filter(email_date__gte=data.get('start_date'))
        if data.get('final_date'):
            queryset = queryset.filter(email_date__lte=data.get('start_date'))
    if data.get('email_id'):
        queryset = queryset.filter(emailID=data.get('email_id'))
    if data.get('customer'):
        queryset = queryset.filter(customer=data.get('customer'))
    if data.get('sent'):
        queryset = queryset.filter(sent=data.get('sent'))
    if queryset:
        data = {'emailID': [], 'email_date': [], 'parser': [], 'options': [], 'sent': [], 'file': [],
                'createAdd': [], 'customer': []}
        for query in queryset:
            data['emailID'] += [query.emailID]
            data['email_date'] += [query.email_date]
            data['parser'] += [query.parser]
            data['options'] += [query.options]
            data['sent'] += [query.sent]
            data['file'] += [query.file]
            data['createAdd'] += [query.createAdd]
            data['customer'] += [query.customer]
        df = pd.DataFrame(data, columns=list(data.keys()))
        key = uuid.uuid4()
        key = str(key).replace('-', '_')
        df.to_excel('media/Excel/{}.xlsx'.format(key))
        return key
    return 'Query without data'


@celery_app.task
def send_email(data) -> str:
    print(data)
    subject, from_email, to = 'Finished Report', settings.EMAIL_HOST_USER, 'nellith25@gmail.com'
    text_content = 'Finished Report <br>'
    html_content = 'Result of the Report <br>' \
                   'Key, to download the file manually: {} <br>' \
                   '<a href="http://{}:8000/file/{}.xlsx">Click to download the report</a>'.format(data[0],
                                                                                                   settings.IP_LOCAL,
                                                                                                   data[0])
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return 'The mail was sent correctly to the user: {}'.format('admin')
