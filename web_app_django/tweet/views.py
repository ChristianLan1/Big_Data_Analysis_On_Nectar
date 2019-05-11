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
        #print(docs)
        #print(docs.view('city/city-view',key = "melbourne"))


        #GET /tweet_resutls/_design/city/_view/city-view HTTP/1.1

        cityInfo = []
        for doc in docs.view('city/city-view',group = True):

            print(doc.key, doc.value)
            cityInfo.append(doc)
        print(cityInfo)
            
        context = {'cityInfo':cityInfo}

        #context = {'file':2}
    else:
        context = {'file':error}

    return render(request,'index.html',context = context)
    
        

