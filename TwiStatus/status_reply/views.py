from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext


# Create your views here.

from forms import InputForm
from twitter_status.settings import TWITTER_API

def get_status_reply(request):
    
    template_name = "status_reply.html" 

    ci = RequestContext(request) 
    form = InputForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data['status_id']
            #date = 571542404156809216
	    api = TWITTER_API

	    main_status = api.GetStatus(id=data) 

	    reply_status_old = api.GetReplies(since_id=data)
            reply_status = []

            for i in reply_status_old:
                reply_status.append(i.AsDict())

            return render_to_response(template_name, {'form':form, "main_status":main_status, "reply_status":reply_status}, ci)

    return render_to_response(template_name, {'form':form}, ci)
