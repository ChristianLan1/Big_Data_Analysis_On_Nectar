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
    context = {}
    
    
    if error == "no":
        docs = SERVER['tweet_results']
        #print(docs)
        #print(docs.view('city/city-view',key = "melbourne"))


        #GET /tweet_resutls/_design/city/_view/city-view HTTP/1.1

        cityInfo = []
        cityTotal = []
        cityPercentage = {}
        for doc in docs.view('results/result-view',group = True):

            print(doc.key, doc.value)
            cityInfo.append(doc)
        print("space")
        for doc in docs.view('results/cityTweet-view',group = True):

            #print(doc.key,doc.value)
            #cityTotal.append(doc)
            for data in cityInfo:
                if data.key == doc.key:
                    number = (data.value/doc.value)*100
                    percentage = str(round(number,2))+"%"
                    #print(percentage)
                    cityPercentage[data.key] = percentage
        cityTotal.append(cityPercentage)
        

        #print(cityTotal)

        #print(cityInfo)

        context['cityTotal'] = cityTotal
        context['cityInfo'] = cityInfo
        

        docsNsw = SERVER['aurin_nsw']
        #print(docs)
        #print(docs.view('city/city-view',key = "melbourne"))
        countId = []
        countDomesitc = 0
        #print(docs['f6376ce946ac201c045408615e00d502'])
        for doc in docsNsw:
            features = docsNsw[doc]['features']
            for feature in features:
                countId.append(feature["id"])
            #print(len(countId))
        docsNswDomestic = SERVER['aurin_nsw_domestic']
        for doc in docsNswDomestic.view('domesitc/new-view'):
            for element in doc.value:
                #print(doc.value[element])
                countDomesitc += doc.value[element]
        countDomesitc += len(countId)
        countDomestic = (countDomestic/7410000)*100
        print(countDomesitc)
        
        context['NswCount'] = countDomesitc
            
            #print(docs[doc]['features'])
        #GET /tweet_resutls/_design/city/_view/city-view HTTP/1.1
        docsVic = SERVER['aurin_vic']
        att = ['a10','a20','a50','a80']
        count = 0
        for doc in docsVic.view('vic/new-view'):

            #print(doc.key, doc.value)
            for properties in doc.value:
                #print(properties)
                for element in properties:
                    if element in att:
                    
                        if properties[element] == 'lga_code_2011':
                            continue
                        elif properties[element] == None:
                            continue
                        else:
                            count += properties[element]
            print(count)
            cout = (cout/5740000)*100
            context['VicCount'] = count
        docsSa = SERVER['aurin_sa']
        countForSa = 0
        for doc in docsSa.view('sa/new-view'):
            for properties in doc.value:
                for element in properties:
                    if element == 'month' or element == "id":
                        continue
                    else:
                        if not properties[element] == None:
                            #print(countForSa)
                            countForSa += properties[element]
        countForSa = (countForSa/1677000)*100
        print(countForSa)
        context['SaCount'] = countForSa





        docs = SERVER['tweet_2014_results']
        cityInfoOld = []
        cityTotalOld = []
        cityPercentageOld = {}
        for doc in docs.view('results/result-view',group = True):
            cityInfoOld.append(doc)
            print(doc.key, doc.value)
        print("total")
        for doc in docs.view('results/cityTweet-view',group = True):
            for data in cityInfoOld:
                if data.key == doc.key:
                    number = (data.value/doc.value)*100
                    percentage = round(number,2)
                    #print(percentage)
                    cityPercentageOld[data.key] = percentage
        cityTotalOld.append(cityPercentageOld)
        context['cityTotalOld'] = cityTotalOld
        print(cityTotalOld)


        #context = {'file':2}
    else:
        context = {'file':error}

    return render(request,'index.html',context = context)
    
        

