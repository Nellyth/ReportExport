import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect


class DownloadFile:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            data = request.path.split('/')
            if data[1] == 'file':
                file_path = os.path.join(settings.MEDIA_ROOT_EXCEL)
                file_path = '{}/{}'.format(file_path, data[2])
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as fh:
                        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
        except IndexError:
            pass

        response = self.get_response(request)
        return response
