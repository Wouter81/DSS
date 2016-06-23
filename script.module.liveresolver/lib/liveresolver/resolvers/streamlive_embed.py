# -*- coding: utf-8 -*-


import re,urlparse,json,requests,cookielib
from liveresolver.modules import client
from liveresolver.modules import control
from liveresolver.modules import constants,liveresolver_utils
from liveresolver.modules.log_utils import log
import urllib,sys,os



def resolve(url):
    
    try:
        
        try: 
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
            url = url.replace(referer,'').replace('?referer=','').replace('&referer=','')
        except:
            referer = url

        id = re.findall('embed/(\d+)',url)[0]
        page = 'http://www.streamlive.to/embedplayer_new2.php?width=620&height=470&channel=%s&autoplay=true'%id
        


        result = client.request(page,headers={'referer':'http://www.streamlive.to', 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to', 'User-agent':client.agent()})
        log(result)

        token_url = re.compile('getJSON\("(.+?)"').findall(result)[0]
        if 'http' not in token_url:
            token_url = 'http:' + token_url
        r2 = client.request(token_url,referer=referer)
        token = json.loads(r2)["token"]

        file = re.compile('(?:[\"\'])?file(?:[\"\'])?\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
        rtmp = re.compile('streamer\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace(r'\\','\\').replace(r'\/','/')
        app = re.compile('.*.*rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
        url=rtmp + ' app=' + app + ' playpath=' + file + ' swfUrl=http://www.streamlive.to/ads/streamlive.swf flashver=' + constants.flash_ver() + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl='+page

        
        return url
    except:
        return



