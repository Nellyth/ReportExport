from django.urls import path
from Apps.Report.views import RegisterCustomer, RegisterFile, index, Search, DownloadReport

urlpatterns = [
    path('', index, name='index'),
    path('customer', RegisterCustomer.as_view(), name='Customer'),
    path('file', RegisterFile.as_view(), name='File'),
    path('search', Search.as_view(), name='Search'),
    path('download', DownloadReport.as_view(), name='Download'),
]
