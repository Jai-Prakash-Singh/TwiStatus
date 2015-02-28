from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.

from forms import InputForm
import twitter

def get_status_reply(request):
    
    template_name = "status_reply.html" 

    ci = RequestContext(request) 
    form = InputForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data['status_id']
            print data
            #date = 571542404156809216
            consumer_key = 'bsjANsQfkTDfLQqyAPEdQb5tE'
	    consumer_secret = 'VKGAWEiQXvgqA8kqjG5w7bEVAWTSZd2MjevV2wilsNzBmm76R8'
	    access_token = '519973818-WwH5f7XfUSlIftoHkLpoj7F8j8AgYnRc9BPCd4cR'
	    access_token_secret = 'dpKnEDbMg2Wxhsue1sdJJZkvHQDlsXtxZ50JvHGlcUQij'

	    api = twitter.Api(consumer_key=consumer_key,
		consumer_secret=consumer_secret,
		access_token_key=access_token,
		access_token_secret=access_token_secret)

	    main_status = api.GetStatus(id=data) 
	    print main_status

	    reply_status_old = api.GetReplies(since_id=data)
            reply_status = []
            for i in reply_status_old:
                reply_status.append(i.AsDict())
	    print reply_status

            #return HttpResponse((main_status, reply_status))
            return render_to_response(template_name, {'form':form, "main_status":main_status, "reply_status":reply_status}, ci)
        return render_to_response(template_name, {'form':form}, ci)
    else:
        return render_to_response(template_name, {'form':form}, ci)
