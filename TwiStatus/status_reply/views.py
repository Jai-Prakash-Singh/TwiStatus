#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: ascii -*-
# -*- coding: utf-42 -*-
# -*- coding: utf-8 -*-


from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_unicode
import requests
from bs4 import BeautifulSoup
import urllib

# Create your views here.

from forms import InputForm
from twitter_status.settings import request_twitter_api, TWITTER_API as api


def my_strip(x):
    try:
        #x = str(x.encode("ascii", "ignore").encode('utf-8')).strip()
        x = smart_unicode(x)

    except:
        x = str(x).strip()

    return x




def get_tweet_id_and_give_status(request,  api, screen_name, tweet_id, html=''):
    reply_list = []
    #link = "https://twitter.com/%s/status/%s" %(screen_name, tweet_id)
    #link = "https://twitter.com/i/iHrithik/conversation/574949073674891265?include_available_features=1&include_entities=1&max_position=574988161111097344"


    
    while  html:
	soup = BeautifulSoup(html, "html.parser")
	
	#reply_div = soup.find("ol", 
	#    attrs={"id":"stream-items-id"}).find_all("li", attrs={"class":"js-simple-tweet"})

        reply_div = soup.find_all("li", attrs={"class":"js-simple-tweet"})

        for reply in reply_div:    
            reply = urllib.unquote(str(reply))
	    soup_reply = BeautifulSoup(reply, "html.parser")
	
	    fullname = soup_reply.find("strong", 
	        attrs={"class":"fullname js-action-profile-name show-popup-with-id"}).text
            #print fullname
	
	    user_name  = soup_reply.find("span", 
	        attrs={"class":"username js-action-profile-name"}).text
	    
	    #print user_name
            try:
	        at_reply  = soup_reply.find("a", 
	            attrs={"class":"twitter-atreply pretty-link"}).text
            except:
                at_reply = None

	    #print at_reply
            try:
	        at_reply_href  = soup_reply.find("a", 
	            attrs={"class":"twitter-atreply pretty-link"})["href"]
            except:
                at_reply_href = "None"
	    
            #print at_reply_href
            
	    at_reply_text  = soup_reply.find("p", 
	        attrs={"class":"js-tweet-text tweet-text"})

            at_reply_text_rtl  = soup_reply.find("p",
                attrs={"class":"js-tweet-text tweet-text tweet-text-rtl"})

            if at_reply_text:
                at_reply_text = at_reply_text.text
            elif at_reply_text_rtl:
                at_reply_text = at_reply_text_rtl.text
            else: 
                at_reply_text = ''

	    #print at_reply_text
	    
	    max_id = soup_reply.find("a", attrs={"class":"details with-icn js-details"})["href"]
            max_id = max_id[max_id.rfind("/")+1:]

	
	    reply_list.append(map(my_strip, [fullname, user_name, at_reply,  at_reply_text ]))


	link = "https://twitter.com/i/%s/conversation/%i?include_available_features=1&include_entities=1&max_position=%i"
	link = link %(screen_name, int(tweet_id), int(max_id ))
        request.session["link"] = link
        request.session["max_id"] = max_id


	r = request_twitter_api.get(link)
	html  =  r.json()["items_html"]

        html = str(html.encode("ascii", "ignore")).strip()

        #print "loop" 

    return {"reply_list" : reply_list}




@csrf_exempt
def get_status_reply(request):
    template_name = "status_reply.html" 

    ci = RequestContext(request) 
    form = InputForm(request.POST or None)
    dict_data  = {"form":form, "error_list": []}

    if request.method == 'POST':
        if form.is_valid():
            tweet_id = form.cleaned_data['twit_id']
            #tweet_id = 571542404156809216
            #tweet_id = 572238536750993408
	    status = api.get_status(id = tweet_id )
            if status.in_reply_to_status_id:
                screen_name = status.in_reply_to_screen_name
                request.session["tweet_id"] = status.in_reply_to_status_id
                request.session["screen_name"] = screen_name
                link = "https://twitter.com/%s/status/%s" %(screen_name, status.in_reply_to_status_id)
            else:
	        screen_name = status._json["user"]["screen_name"]
                request.session["tweet_id"] = tweet_id
	        request.session["screen_name"] = screen_name
		link = "https://twitter.com/%s/status/%s" %(screen_name, tweet_id)
            
            name = status._json["user"]["name"]
            screen_name = status._json["user"]["screen_name"]
            at_reply = status.in_reply_to_screen_name 
            text = status.text
 
            dict_data["status"] = map(my_strip, [name, screen_name, at_reply, text])
            
            r = request_twitter_api.get(link)
            html = r.text
            
             

	    dict_data.update(get_tweet_id_and_give_status(request,  api,  screen_name, tweet_id, html))
            return render_to_response(template_name, dict_data, ci)
	else:
	    dict_data["error_list"].append("twitt id is not valid")
        
        
    return render_to_response(template_name, dict_data, ci)




@csrf_exempt
def ajax_get_reply(request):
    ci = RequestContext(request)
    template_name = "ajax_get_reply.html"

    tweet_id = request.session.get("tweet_id")
    screen_name = request.session.get("screen_name")

    max_id = request.session.get("max_id")

    if max_id:
        link = "https://twitter.com/i/%s/conversation/%i?include_available_features=1&include_entities=1&max_position=%i"
        link = link %(screen_name, int(tweet_id), int(max_id ))
        r = request_twitter_api.get(link)
        html  =  r.json()["items_html"]
        html = str(html.encode("ascii", "ignore")).strip()


    dict_data = get_tweet_id_and_give_status(request,  api, screen_name, tweet_id, html)
    return render_to_response(template_name, dict_data, ci)
