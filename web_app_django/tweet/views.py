from django.shortcuts import render
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from couchdb import Server

SERVER = Server('http://127.0.0.1:5984')
if (len(SERVER) == 0):
    SERVER.create('tweet_results')
# Create your views here.

def index(request):
    docs = SERVER['tweet_results']
    if request.method == "POST":
        title = request.POST['title'].replace(' ','')
        docs[title] = {'title':title,'text':""}
        return HttpResponseRedirect(u"/doc/%s/" % title)
    context = {'rows':docs}
    return render(request,'index.html',context = context)

def detail(request,id):
    docs = SERVER['docs']
    doc = docs[id]
            
    if request.method =="POST":
        doc['title'] = request.POST['title'].replace(' ','')
        doc['text'] = request.POST['text']
        docs[id] = doc
    return render_to_response('tweet/detail.html',{'row':doc})