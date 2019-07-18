from django.db import models
from datetime import datetime
from Apps.Report.choices import select_parser_customers, select_options_file_parser


def movie_directory_path(instance, filename):
    return f'{datetime.now().strftime("%m|%d|%Y-%H:%M:%S")}/{filename}'


class Customers(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    parser = models.CharField(max_length=15, choices=select_parser_customers)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{0}'.format(self.name)


class FileParser(models.Model):
    emailID = models.IntegerField(null=True)
    email_date = models.DateField(null=True)
    parser = models.CharField(max_length=15, null=True)
    options = models.CharField(max_length=15, choices=select_options_file_parser, null=False)
    sent = models.BooleanField(null=False)
    file = models.FileField(upload_to=movie_directory_path, null=False)
    createAdd = models.DateField(null=True, blank=True, default=datetime.now)
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['createAdd']

    def __str__(self):
        return '{0}'.format(self.emailID)