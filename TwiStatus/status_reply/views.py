from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from forms import InputForm
from twitter_status.settings import TWITTER_API as api

def get_status_reply(request):
    template_name = "status_reply.html" 

    ci = RequestContext(request) 
    form = InputForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data['status_id']
            #date = 571542404156809216
            request.session["tweet_id"] = data

            try:
                main_status = api.GetStatus(id=data) 
                reply_status_old = api.GetReplies(since_id=data)
                reply_status = [] 
         

                for i in reply_status_old:
                    reply_status.append(i.AsDict())

                return render_to_response(template_name, {'form':form, "main_status":main_status, "reply_status":reply_status}, ci)
            except:
                msg = "Given post id is not aval on twitter"
                return render_to_response(template_name, {'form':form, "msg":msg}, ci)
            
    return render_to_response(template_name, {'form':form}, ci)




@csrf_exempt
def ajax_get_reply(request):
    ci = RequestContext(request)
    template_name = "ajax_get_reply.html"
    tweet_id = request.session.get("tweet_id")
    try:
        reply_status_old = api.GetReplies(since_id=tweet_id)
        reply_status = []

        for i in reply_status_old:
            reply_status.append(i.AsDict())

            print reply_status

        return render_to_response(template_name, {"reply_status":reply_status}, ci)

    except:
        msg = "Given post id is not aval on twitter"
        return render_to_response(template_name, {"msg":msg}, ci)

    # return HttpResponse(tweet_id)
