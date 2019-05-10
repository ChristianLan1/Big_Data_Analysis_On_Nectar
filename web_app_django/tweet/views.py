from django.shortcuts import render
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from couchdb import Server
try:
    SERVER = Server('http://172.26.38.157:5984')
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
        for doc in docs:

            print(docs[doc])
            
            context = {'file':docs[doc]}
    else:
        context = {'file':error}

    return render(request,'index.html',context = context)
    
        

