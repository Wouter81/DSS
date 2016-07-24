import urllib2,urllib,cgi, re, urlresolver  
import urlparse
import HTMLParser
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import random
from operator import itemgetter
import traceback,cookielib
import base64,os,  binascii
import CustomPlayer,uuid
from time import time
from datetime import datetime
import base64
import xml.etree.ElementTree as ET
import random
import live365
import time
import datetime
import _strptime
from resources.lib.modules import control
from resources.lib.modules.log_utils import log

from addon.common.addon import Addon
          
try:
    import json
except:
    import simplejson as json
    
addon = xbmcaddon.Addon('plugin.video.dss')
addonname = addon.getAddonInfo('name')
#icon = addon.getAddonInfo('icon')
addon_id = 'plugin.video.dss'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8')) 
icon = os.path.join(home, 'icon.png')
FANART = os.path.join(home, 'fanart.jpg')

addonDir = addon.getAddonInfo('path').decode("utf-8")
libDir = os.path.join(addonDir, 'resources', 'lib')
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
favorites = os.path.join(profile, 'favorites')
history = os.path.join(profile, 'history')
 
if not os.path.exists(profile):
    os.makedirs(profile)


addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])

S365COOKIEFILE='s365CookieFile.lwp'
S365COOKIEFILE=os.path.join(profile, S365COOKIEFILE)



class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response

def ShowSettings(Fromurl):
	selfAddon.openSettings()


def get365CookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(S365COOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar

def Privacy_Policy():
    dialog = xbmcgui.Dialog()
    dialog.ok("OFFLINE", "DutchSportStreams is voor onbepaalde tijd offline.", "alternatieven zijn : ZemTV, SportDevil en Castaway")




def addLink(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok

def addDir(name,url,mode,iconimage,fanart,description,genre,date,credits,isItFolder=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date, "credits": credits })
        liz.setProperty("Fanart_Image", fanart)

        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
        return ok



def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Kodi/14.0 (Macintosh; Intel Mac OS X 10_10_3) App_Bitness/64 Version/14.0-Git:2014-12-23-ad747d9-dirty')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link;

def get_Url(url, cookieJar=None,post=None, timeout=20, headers=None):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link;

def GetHTML(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
				
	return param




def Addtypes():
        import geo
        addDir('Club Channels' ,'sss',30,icon ,  FANART,'','','','')
        #if geo.returnCountyCode() == "NL":
        addDir('Sport365.live' ,'Sport365',12,icon ,  FANART,'','','','')
        addDir('Bvls2016.sc' ,'Bvls',13,icon ,  FANART,'','','','')
        addDir('Thefeed2all.eu' ,'sss',2,icon ,  FANART,'','','','')
        #addDir('Wiz1.net' ,'sss',20,icon ,  FANART,'','','','')
        #addDir('Goatd.net' ,'sss',22,icon ,  FANART,'','','','')
	return




def total_seconds(dt):
    import datetime
    if hasattr(datetime, 'total_seconds'):
        return dt.total_seconds()
    else:
        return (dt.microseconds + (dt.seconds + dt.days * 24 * 3600) * 10**6) / 10**6
        
def getutfoffset():
    import time
    from datetime import datetime

    ts = time.time()
    utc_offset = total_seconds((   datetime.fromtimestamp(ts)-datetime.utcfromtimestamp(ts)))/60
              
    return int(utc_offset)







def AddBvls(url=None):
    i=0
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Scanning Bvls2016.sc')
    sourceSite = 'http://www.bvls2016.sc/'
    xmlurl = 'http://dutchsportstreams.com/xml/ds.xml'
    req = urllib2.Request(xmlurl,None)
    response = urllib2.urlopen(req)
    xml = response.read()
    response.close()
    root = ET.fromstring(xml)
    items = root.findall('item')
    for item in items:
        cname = item.find('title').text
        lnk = item.find('url').text
        print cname
        print lnk
        try :
            frameHtml = getPage(lnk,'http://www.bvls2016.sc/', getUserAgent())
            b64coded = getBaseEncodedString(frameHtml)
            streamUrl = getStreamUrl(b64coded)
            i+=1
            progress.update( 15+ (i*15), "BVLS2016.SC", "Finding links.. stream%d"%i, "" )
        except :
            streamUrl = ''
        if (getResponse(streamUrl)) :
            color = 'green'
        else :
            #streamUrl = ''
            color = 'red'
        if streamUrl.startswith('rtmp'):
            
            color = 'blue'
        if streamUrl[-4:] == '.flv' :
            streamUrl=VeetleId(streamUrl)
        #else :
            #print('M3U')
        #if 'youtube' in streamUrl:
            #streamUrl=streamUrl.replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/play/?video_id=').strip()
        addDir('[COLOR '+color+']Bvls2016.sc - '+cname.capitalize()+'[/COLOR]',streamUrl,14,icon ,  FANART,'','','','',isItFolder=False)
        
    progress.close()

def getResponse(url):
    try:
        response = urllib2.urlopen(url, timeout=200)
        if response and response.getcode() == 200:
            return response
        else :
            return False
    except:
        return False
    
def AddSports365Channels(url=None):
    errored=True
    import live365
    #addDir(Colored("All times in local timezone.",'red') ,"" ,0 ,"","","","","","")		#name,url,mode,icon
    videos=live365.getLinks()
    for nm,link,active in videos:
        if active:
           
            addDir(Colored(nm  ,'ZM') ,link,11 ,"","","","","","")
        else:
            addDir("[N/A]"+Colored(nm ,'blue') ,"",0 ,"","","","","","")
        errored=False
    #if errored:
       #if RefreshResources([('live365.py','https:#')]):
            #dialog = xbmcgui.Dialog()
            #ok = dialog.ok('XBMC', 'No Links, so updated files dyamically, try again, just in case!')           
            #print 'Updated files'

def CatClubchannels():
    import plugintools
    plugintools.add_item(title="AFC Ajax",url="plugin://plugin.video.youtube/user/ajax/",thumbnail='https://yt3.ggpht.com/-jqrIEltgE1U/AAAAAAAAAAI/AAAAAAAAAAA/AhkDhss9X4w/s100-c-k-no/photo.jpg',folder=True )
    plugintools.add_item(title="Feyenoord",url="plugin://plugin.video.youtube/user/FeyenoordRotterdamTV/",thumbnail="https://yt3.ggpht.com/-sfO41QeVlw4/AAAAAAAAAAI/AAAAAAAAAAA/hDDl3jwRL1k/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="PSV",url="plugin://plugin.video.youtube/user/psveindhoven/",thumbnail="https://i.ytimg.com/i/_2ynsXrRrKP8zYrU7Hc06A/mq1.jpg?v=53302bc9",folder=True )
    plugintools.add_item(title="Pec Zwolle",url="plugin://plugin.video.youtube/user/peczwolletv/",thumbnail="https://yt3.ggpht.com/-ShDWQyu69vk/AAAAAAAAAAI/AAAAAAAAAAA/klALDUBVkFs/s100-c-k-no-rj-c0xffffff/photo.jpg",folder=True )
    plugintools.add_item(title="Heracles Almelo",url="plugin://plugin.video.youtube/user/HeraclesAlmeloTV/",thumbnail="https://yt3.ggpht.com/-4syNFL3i7WA/AAAAAAAAAAI/AAAAAAAAAAA/9uxdYzc6z-8/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="Roda JC Kerkrade",url="plugin://plugin.video.youtube/user/RodaJCKerkradeTV/",thumbnail="https://yt3.ggpht.com/-LhF3zdjpng4/AAAAAAAAAAI/AAAAAAAAAAA/peTKp7TXFYQ/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="ADO Den Haag",url="plugin://plugin.video.youtube/user/ADODenHaagTV/",thumbnail="https://yt3.ggpht.com/-6RvgIEV9WhI/AAAAAAAAAAI/AAAAAAAAAAA/eYEVcEyJTHU/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="Vitesse",url="plugin://plugin.video.youtube/user/VitesseTV/",thumbnail="https://yt3.ggpht.com/-ewXQBcFk6ZE/AAAAAAAAAAI/AAAAAAAAAAA/1_nJq7G_iqo/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="FC Groningen",url="plugin://plugin.video.youtube/user/FCGroningenTV/",thumbnail="https://yt3.ggpht.com/-vatxowB6e2o/AAAAAAAAAAI/AAAAAAAAAAA/PySf0KkU7ZM/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="N.E.C.",url="plugin://plugin.video.youtube/user/NECTVkanaal/",thumbnail="https://yt3.ggpht.com/-KpZ8RDTeTfQ/AAAAAAAAAAI/AAAAAAAAAAA/pVeT-DTm5kk/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="FC Utrecht",url="plugin://plugin.video.youtube/user/fcutrecht/",thumbnail="https://yt3.ggpht.com/-3RaZ5yClYxg/AAAAAAAAAAI/AAAAAAAAAAA/R4o-6Jk6x8M/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="AZ",url="plugin://plugin.video.youtube/user/AZTV/",thumbnail="https://yt3.ggpht.com/-yyhnHNLCPp8/AAAAAAAAAAI/AAAAAAAAAAA/xlm_pFvukqI/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="Willem II",url="plugin://plugin.video.youtube/user/WillemII/",thumbnail="https://yt3.ggpht.com/-738-M5uYXlg/AAAAAAAAAAI/AAAAAAAAAAA/0k0wAIqPq30/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="Excelsior",url="plugin://plugin.video.youtube/user/sbvexcelsior/",thumbnail="https://yt3.ggpht.com/-32h9c3Rz-ao/AAAAAAAAAAI/AAAAAAAAAAA/1ANEn8xjySU/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="FC Twente",url="plugin://plugin.video.youtube/user/FCTwenteTV/",thumbnail="https://yt3.ggpht.com/-TKHbRZL1kb4/AAAAAAAAAAI/AAAAAAAAAAA/cyqeyk8i8RM/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="SC Cambuur",url="plugin://plugin.video.youtube/user/SCCambuurTV/",thumbnail="https://yt3.ggpht.com/-Fb4cKM1YAto/AAAAAAAAAAI/AAAAAAAAAAA/uBPlhE7gn7E/s100-c-k-no/photo.jpg",folder=True )
    plugintools.add_item(title="De Graafschap",url="plugin://plugin.video.youtube/user/degraafschapvideo/",thumbnail="https://yt3.ggpht.com/--eXA14VMeVU/AAAAAAAAAAI/AAAAAAAAAAA/ju7WtvhOsg0/s100-c-k-no/photo.jpg",folder=True )
    #plugintools.add_item(title="",url="plugin://plugin.video.youtube/user//",thumbnail="",folder=True )




def Catfeed2all():
        addDir('Football' ,'football.html',18,icon ,  FANART,'','','','')
        addDir('AM. Football' ,'american-football.html',18,icon ,  FANART,'','','','')
        addDir('Basketball' ,'basketball.html',18,icon ,  FANART,'','','','')
        addDir('Boxing/WWE/UFC' ,'boxing-wwe-ufc.html',18,icon ,  FANART,'','','','')
        addDir('Rugby' ,'rugby.html',18,icon ,  FANART,'','','','')
        addDir('Ice Hockey' ,'ice-hockey.html',18,icon ,  FANART,'','','','')
        addDir('Tennis' ,'tennis.html',18,icon ,  FANART,'','','','')
        addDir('Motorsport' ,'motosport.html',18,icon ,  FANART,'','','','')
        addDir('Golf' ,'golf.html',18,icon ,  FANART,'','','','')
        addDir('Baseball' ,'baseball.html',18,icon ,  FANART,'','','','')
        addDir('Darts' ,'darts.html',18,icon ,  FANART,'','','','')
        addDir('Snooker' ,'snooker.html',18,icon ,  FANART,'','','','')
        addDir('Handball' ,'handball.html',18,icon ,  FANART,'','','','')
        addDir('Cricket' ,'cricket.html',18,icon ,  FANART,'','','','')
        addDir('Aussie Rules' ,'aussie-rules.html',18,icon ,  FANART,'','','','')
        addDir('Others' ,'others.html',18,icon ,  FANART,'','','','')
	return



def Addthefeed2all(url):
    try:
        pagecontent=getPage('http://www.feed2allnow.eu/type/'+url,'http://www.feed2allnow.eu/',getUserAgent())
        match1=re.compile('<span>\s*([^<]+)</span>\s*([^<]+) </a> </h3>.+?\s*.+?href=\'(.*?)\'',re.DOTALL).findall(pagecontent)
        for dsstime,dssgame,dsslink in match1:
            dsslink = 'http://www.feed2allnow.eu' + dsslink
            addDir('[B][COLOR yellow3]'+ dssgame+ '[/COLOR][/B]',dsslink,3,icon ,  FANART,'','','','',isItFolder=False)
    except:
        pass
    try:
        pagecontent=getPage('http://www.feed2allnow.eu/type/'+url,'http://www.feed2allnow.eu/',getUserAgent())
        match1=re.compile('<span class="matchtime">([^<]+)</span> </span>\s*([^<]+)</a> </h3>.+?\s*.+?href=\'([^<]+)\'',re.DOTALL).findall(pagecontent)
        for dsstime,dssgame,dsslink in match1:
            try:
                dt = datetime.strptime(dsstime, "%H:%M")
                dsstime = str(dt.hour+1).rjust(2,'0') + ':' + str(dt.minute).rjust(2,'0')
            except :
                pass        
            dsslink = 'http://www.feed2allnow.eu' + dsslink
            addDir('[B][COLOR yellow3]''('+dsstime+') '+ dssgame+ '[/COLOR][/B]',dsslink,3,icon ,  FANART,'','','','',isItFolder=False)
    except:
        pass
    


def Addwiz(url=None):
    pagecontent = getPage('http://www.wiz1.net/lag10_home.php','http://www.wiz1.net/',getUserAgent())
    match = re.compile(r'(\d{2}:\d{2}) <font color="#5185C9"><b>([^<]+)</b></font> ([^<]+)<a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(pagecontent)
    for dsstime, sport, game, dsslink in match:
        try:
            dt = datetime.strptime(dsstime, "%H:%M")
            dsstime = str(dt.hour+0).rjust(2,'0') + ':' + str(dt.minute).rjust(2,'0')
        except :
            pass
        #if 'Eredivisie' in sport or 'Belgium' in sport:
            #addDir('[B][COLOR yellow3]''('+dsstime+') '+ game+ '[/COLOR][/B]',dsslink,21,icon ,  FANART,'','','','',isItFolder=False)
        #if 'Netherlands' in game or 'Belgium' in game:
        addDir('[B][COLOR yellow3]''('+sport+') '+'('+dsstime+') '+ game+ '[/COLOR][/B]',dsslink,3,icon ,  FANART,'','','','',isItFolder=False)
        



def Addgoatd(url=None):
    dssport=''
    goatpage = getPage('http://goatd.net/','http://goatd.net/',getUserAgent())
    match = re.compile(r'<b>ET</b></td>\s+<td[^<]+><img src="([^"]+)".*?href="([^"]+)"[^>]+>([^<]+)<.*?<b>([^<]+)<.*?<b>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(goatpage)
    for img, dsslink, dssgame, dsstime, dsszone in match:
        try:
            sport = re.compile('http://.*?/.*?/.*?/.*?/.*?/.*?/(.*?).gif', re.DOTALL | re.IGNORECASE).findall(img)
            if sport > 0 :
                for dssport in sport:
                    dssport = re.sub("[^A-Za-z]", "", dssport) 
        except:
            pass
        dsslink = 'http://goatd.net/' + dsslink
        addDir('[B][COLOR yellow3]''('+dssport+') '+'('+dsstime+') '+dsszone+' '+ dssgame+ '[/COLOR][/B]',dsslink,3,icon ,  FANART,'','','','',isItFolder=False)
        





def AddCricFree(url):
    pat='<li.*?><a href="(.*?)".*?channels-icon (.*?)"'
    res=get_Url("http://cricfree.sx/")
    channels=re.findall(pat,res)
    
    pat='<li><a href="(.*?)".*?\<span class="chclass3"\>(.*?)<'
    channels+=re.findall(pat,res)    
#    channels=sorted(channels,key=lambda s: s[1].lower()   )
    channels=sorted_nicely(channels)
    for u,n in channels:
        addDir(n.capitalize(),u,17,icon ,  FANART,'','','','',isItFolder=False)





def playSports365(url):
    #print ('playSports365')
    import live365
    urlToPlay=live365.selectMatch(url)
    if urlToPlay and len(urlToPlay)>0:
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    #    print   "playing stream name: " + str(name)
        xbmc.executebuiltin('XBMC.Notification(Visit sport365.live , And keep Streams Alive !! ,10000,'+icon+')')
        xbmc.Player(  ).play( urlToPlay, listitem)  
    #else:
       #if RefreshResources([('live365.py','https://')]):
            #dialog = xbmcgui.Dialog()
            #ok = dialog.ok('XBMC', 'No Links, so updated files dyamically, try again, just in case!')           
            #print 'Updated files'
    return	 


def PlayCricFree(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    res=getUrl(url)
    patt='<iframe frameborder="0" marginheight="0".*?src="(.*?)" id="iframe"'
    url2=re.findall(patt,res)[0]
    referer=[('Referer',url)]
    res=get_Url(url2,headers=referer)
    urlToPlay=None
    supported=False
    if 'theactionlive.com/' in res:
        supported=True
        progress.update( 30, "", "Finding links..stage2", "" )
        patt="id='(.*?)'.*?width='(.*)'.*?height='(.*?)'"
        gid,wd,ht=re.findall(patt,res)[0]
        referer=[('Referer',url2)]
        url3='http://theactionlive.com/livegamecr2.php?id=%s&width=%s&height=%s&stretching='%(gid,wd,ht)
        res=get_Url(url3,headers=referer)    
        if 'biggestplayer.me' in res:
            progress.update( 50, "", "Finding links..stage3", "" )
            patt="id='(.*?)'.*?width='(.*)'.*?height='(.*?)'"
            gid,wd,ht=re.findall(patt,res)[0]
            referer=[('Referer',url3)]
            
            patt="src='(.*?)'"
            jsUrl=re.findall(patt,res)[0]
            jsData=getUrl(jsUrl)
            patt="\.me\/(.*?)\?"
            phpURL=re.findall(patt,jsData)[0]
            url4='http://biggestplayer.me/%s?id=%s&width=%s&height=%s'%(phpURL,gid,wd,ht)
            progress.update( 80, "", "Finding links..last stage", "" )
            res=get_Url(url4,headers=referer)    
            patt='file: "(.*?)"'
            urlToPlay=re.findall(patt,res)[0];
            referer=[('Referer',url4)]
            urlToPlay+='|Referer='+url4
    if 'www.reytv.co' in res:
        supported=True
        progress.update( 30, "", "Finding links..stage2", "" )
        patt="fid='(.*?)'.*?v_width=(.*?);.*?v_height=(.*?);"
        gid,wd,ht=re.findall(patt,res)[0]
        referer=[('Referer',url2)]
        url3='http://reytv.co/embedo.php?live=%s&width=%s&height=%s'%(gid,wd,ht)
        progress.update( 50, "", "Finding links..stage3", "" )
        res=get_Url(url3,headers=referer)
        
        patt='file: "(.*?)"'
        rtmp=re.findall(patt,res)[0]
        patt='securetoken: "(.*?)"'
        token=re.findall(patt,res)[0]           
        urlToPlay=rtmp + ' token=' + token + ' pageUrl='+url3+ ' swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf'+' timeout=20'
    
    if urlToPlay and len(urlToPlay)>0:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        playlist.add(urlToPlay,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist) 
    else:
        dialog = xbmcgui.Dialog()
        if not supported:
            ok = dialog.ok('Not Supported','This channel is not supported yet')
   
    
   

		

def Colored(text = '', colorid = '', isBold = False):
    if colorid == 'ZM':
        color = 'FF11b500'
    elif colorid == 'EB':
        color = 'FFe37101'
    elif colorid == 'bold':
        return '[B]' + text + '[/B]'
    else:
        color = colorid
        
    if isBold == True:
        text = '[B]' + text + '[/B]'
    return '[COLOR ' + color + ']' + text + '[/COLOR]'	

def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)
        



    
        


def playBvls(name,url):
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
#    print "playing stream name: " + str(name)
    xbmc.executebuiltin('XBMC.Notification(Visit www.bvls2016.sc , And keep Streams Alive !! ,10000,'+icon+')')
    xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( url, listitem)
	

def playVeetle(url):
     xbmc.executebuiltin('XBMC.RunPlugin('+url+')') 





def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key[1]) ] 
    return sorted(l, key = alphanum_key)




def getPage(page, referer=None, ua=None, cookieJar=None,post=None,timeout=5):
    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    url = page                                                           
    try:                                                                 
        req = urllib2.Request(url ,None)                                                                          
        if(referer is not None):                                                                                  
            req.add_header('Referer', referer)                                                                    
                                                                                                                  
        if(ua is not None):                                                                                       
            req.add_header('User-Agent', ua)                                                                      
                                                                                                                  
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')               
        req.add_header('Accept-Language', 'nl,en-US;q=0.7,en;q=0.3')                                              
        req.add_header('Accept-Encoding', 'deflate')                                                        
        req.add_header('Connection', 'keep-alive')
        response = opener.open(req,post,timeout=timeout)
        #response = urllib2.urlopen(req,post,timeout)                                            
        data = response.read()                                                                                    
        response.close()                                                                                          
        if(ua is None) :                                                                                          
            print(data)                                                                            
        return str(data)                                                                           
    except :                                                                                       
        return ''                                                                                  
        print('We failed to open '+url)

def getUserAgent():
    return getUa()

def getUa():
    foo = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0", "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0", "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0", "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0", "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0", "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1", "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21.0", "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130331 Firefox/21.0", "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0", "Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0", "Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0", "Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0", "Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1", "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1", "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1", "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.16) Gecko/20120427 Firefox/15.0a1", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1", "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2", "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1", "Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:15.0) Gecko/20121011 Firefox/15.0.1"]
    return(random.choice(foo))

def getBaseEncodedString(streamPage):
    try:
        _regex_encodedstring = re.compile("file\s*\:\s*window\.atob\(\'(.*?)\'\)" , re.DOTALL)
        baseEncoded = _regex_encodedstring.search(streamPage).group(1)
        return baseEncoded
    except:
        return ''

def getStreamUrl(baseEncoded):
    return base64.b64decode(baseEncoded)

def VeetleId(streamUrl):
    veetleId = getIdByUrl(streamUrl)
    veetleUrl = 'plugin://plugin.video.veetle/?channel='+veetleId
    return veetleUrl

def getIdByUrl(url):
    try :
        _regex_getM3u = re.compile("http://(.*?)/flv/(.*?)/1.flv", re.DOTALL)
        streamId = _regex_getM3u.search(url).group(2)
        return streamId
    except :
        return url


def resolver(url, name):
    import liveresolver
    resolved = liveresolver.resolve(url) 
    if resolved:
        xbmc.Player().play(resolved)
    else:
        xbmc.executebuiltin("XBMC.Notification(DutchSportStreams,No playable link found. - ,5000)")
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage="DefaultVideo.png")
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    xbmc.Player().play(resolved, liz)



params=get_params()
url=None
name=None
mode=None
linkType=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass


args = cgi.parse_qs(sys.argv[2][1:])
linkType=''
try:
	linkType=args.get('linkType', '')[0]
except:
	pass


print 	mode,url,linkType

try:
	if mode==None or url==None or len(url)<1:
		print "InAddTypes"
		Addtypes()


        elif mode==2:
                Catfeed2all()
        elif mode==3:
                resolver(url,name)
        elif mode==11 :

                url=base64.b64decode(url)
                playSports365(url.split('Sports365:')[1])

    
	elif mode==12 :
		print "Play url is 12"+url
		AddSports365Channels(url)

	elif mode==13 :
		print "Play url is 12"+url
		AddBvls(url)
		
        elif mode==14 :
		print "Play url is 13"+url
		playBvls(name,url)

	elif mode==16 :
		print "Play url is "+url
		AddCricFree(url)
	elif mode==17 :
		print "Play url is "+url
		PlayCricFree(url)
	elif mode==18 :
		print "Play url is "+url
		Addthefeed2all(url)
	elif mode==19 :
		print "Play url is "+url
		playthefeed2all(url)
	elif mode==20 :
		print "Play url is "+url
		Addwiz(url)
	elif mode==21 :
		print "Play url is "+url
		playwiz(url)
	elif mode==22 :
		print "Play url is "+url
		Addgoatd(url)
	elif mode==23 :
		print "Play url is "+url
		playgoatd(url)

        elif mode==30 :
		CatClubchannels()
	

except:
	print 'somethingwrong'
	traceback.print_exc(file=sys.stdout)
	

if not ( (mode==3 or mode==4 or mode==9 or mode==11 or mode==15 or mode==25 or mode==26 or mode==27 or mode==29 or mode==32 or mode==37 or mode==40 or mode==42 or mode==0)  )  :
	if mode==144:
		xbmcplugin.endOfDirectory(int(sys.argv[1]),updateListing=True)
	else:
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

from resources.lib.modules import cache, control, changelog
cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')
