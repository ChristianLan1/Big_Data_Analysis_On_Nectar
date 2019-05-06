from django.shortcuts import render
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from couchdb import Server
try:
    SERVER = Server('http://172.18.0.1:5984')
    if (len(SERVER) == 0):
        SERVER.create('tweet_results')
    error = "no"
except:
    error = "socket error. Unable to connect to couchdb"
# Create your views here.

def index(request):
    
    
    if error == "no":
        docs = SERVER['tweet_results']
        print(docs)
        print(docs['0f664afca04e2b25008526baf10008ed'])
        

   

        context = {'file':docs['0f664afca04e2b25008526baf10008ed']}
    else:
        context = {'file':error}

    return render(request,'index.html',context = context)
    
        

