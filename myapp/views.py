from django.shortcuts import render
from .dbHelper import create_connection, get_all_rows, drop_table_if_exists, migrate_excel_to_sqlite, process_url
from .serializers import WebSerializer
import requests
import time, datetime
from django.http import HttpResponse
from .models import WebResult
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers


def index(request):
    """ home page to load excel file """
    if request.method=='GET':
        return render(request, 'myapp/index.html', {})
    else:
        excel_file = request.FILES['excel_file']

        #  validate xlsx file extension
        if excel_file.split(".")[-1] != 'xlsx' or excel_file.split(".")[-1] != 'xls':
            return render(request, 'myapp/index.html', {})

        conn = create_connection('./db.sqlite3')
        drop_table_if_exists(conn, 'url')

        migrate_excel_to_sqlite(conn, excel_file)
        excel_data = get_all_rows(conn, 'url')

        #perform importing / checking of provided urls
        for url in excel_data:
            if WebResult.objects.all().filter(pk=url[0]).exists():
                continue
            if url is not None:
                process_url(conn, url)

        results = get_all_rows(conn, 'myapp_webresult')

        return render(request, 'myapp/index.html', {'results':results})


def detail(request, url):
    """ show details of a website """
    try:
        website = WebResult.objects.get(url=url)
    except WebResult.DoesNotExist:
        return HttpResponse("<h1>This url was not processed. Make sure you type host:port_number:api/site_check/some_url</h1>")

    website = WebResult.objects.get(url=url)
    data = {
        'url': website.url,
        'http_code': website.http_code,
        'ip': website.ip,
        'datetime': website.datetime,
        'timeout': website.timeout
    }
    return JsonResponse(data)


def result_list(request):
    """ show list of checked websites """
    results = WebResult.objects.all()
    data = list()
    d = list()

    d.append("url")
    d.append("http_code")
    d.append("ip")
    d.append("datetime")
    d.append("timeout")
    data.append(d)

    for r in results:
        d = list()
        d.append(r.url)
        d.append(r.http_code)
        d.append(r.ip)
        d.append(r.datetime)
        d.append(r.timeout)
        data.append(d)

    return render(request, 'myapp/list_view.html', {'results':data})
