from django.shortcuts import render
from pybooru import Moebooru
import random
from django.http import Http404

# Create your views here.
siteurl='https://www.sakugabooru.com/post/show/'
header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
client = Moebooru(site_url='https://www.sakugabooru.com')

def boorurandom():
    try:
        files = client.post_list(tags="order:random") #Random Post 
        choice = random.choice(files) #Select 1 Random Post from Query
        boorurl=choice['file_url'] #File URL
        tags = choice['tags'] #Post Tags

        verdict=filetypechecker(boorurl) #Checker if .mp4 file or not
        if(verdict):
            posturl = siteurl+"{0}".format(choice['id']) #POST URL from 

            params = {'tags': tags, 'post_url': posturl}
            return {'context': params, 'url': boorurl}

    except Exception as e:
            params = {'tags': 'not found', 'post_url': 'not found please refresh'}
            return {'context': params, 'url': 'url not found please refresh'}

def filetypechecker(boorurl):
    if boorurl.find('/'):
            if ".mp4" in (boorurl.rsplit('/',1)[1]):
                return True
            else:
                return False

def index(request):
    try:
        data = boorurandom()
        return render(request, 'vids/index.html', context={
            'videoUrl': data['url'],
            'postUrl': data['context']['post_url'],
            'tags': data['context']['tags']
        })
    except Exception as e:
        return Http404()