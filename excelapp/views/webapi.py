import json

from django.http import HttpResponse
from django.shortcuts import render

from excelapp.models import Tm_Department, Tm_Service
from datetime import datetime as dt


def service_list(request):
    servicelist = []
    if 'term' in request.GET:
        term = request.GET['term']
        tdatetime = dt.now()
        tstr = tdatetime.strftime('%Y/%m/%d %H:%M:%S')
        print(tstr, term)
        queryset = Tm_Service.objects.all()

        queryset = queryset.filter(service_name__contains=term)[:5]
        servicelist = [dict(value=service.service_name) for service in queryset]

        # for service in Tm_Service.objects.all():
        #     servicelist.append(dict(value=service.service_name))



    #json形式の文字列を生成
    json_str = json.dumps(servicelist, ensure_ascii=False, indent=2) 
    return HttpResponse(json_str)


