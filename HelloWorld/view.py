
from django.http import HttpResponse,Http404
from django.template import Template,Context
from django.template.loader import get_template
import time,datetime
from django.shortcuts import render
 
def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)
 
# def hello(request):
#     return HttpResponse("Hello world ! ")
# import time
# def current_time(request):
#     return HttpResponse('Current time is :%s'%time.ctime())
# def hours_ahead(request,offest):
#     try:
#         offest=int(offest)
        
#     except ValueError:
#         raise Http404()
#     else:
#         dt=datetime.datetime.now()+datetime.timedelta(hours=offest)
#         html='<html><body>In %s hour(s),it will be %s.</body></html>'%(offest,dt)
#         return HttpResponse(html)
# def current_datetime(request):
#     now = datetime.datetime.now()
#     t = get_template('current_datetime.html')
#     html = t.render(Context({'current_date': now}))
#     return HttpResponse(html)

from django.shortcuts import render_to_response
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})

def hours_ahead(request,offest):
    try:
      hour_offset=int(offest)
        
    except ValueError:
         raise Http404()
    else:
        next_time=datetime.datetime.now()+datetime.timedelta(hours=hour_offset)
        return render_to_response('hoursahead.html', {'hour_offset':hour_offset,'next_time':next_time})#locals()
       