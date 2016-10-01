import urllib2,urllib,cgi, re, os
import urlparse
import HTMLParser
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import xml.etree.ElementTree as ET
import random
import base64
from operator import itemgetter
import traceback,cookielib
from resources.lib.modules import control
from resources.lib.modules.log_utils import log

try:
    import json
except:
    import simplejson as json

   
addon = xbmcaddon.Addon('plugin.video.xite')
addonname = addon.getAddonInfo('name')
#icon = addon.getAddonInfo('icon')
addon_id = 'plugin.video.wildhitz'
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
 


addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])





class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response





def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)	  
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
		link = 'index.html'
		return link


def addLink(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=5"
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







def GetHTML(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key[1]) ] 
    return sorted(l, key = alphanum_key) 


def Addtypes():
   addDir('Live On Air' ,'xite',2,icon ,  FANART,'','','','')
   addDir('Week Mix' ,'http://xite.nl/videos/categorie/xite-week-mix/1?ajax=1',3,icon ,  FANART,'','','','')
   import plugintools
   plugintools.add_item(title="Xite Youtube",url="plugin://plugin.video.youtube/user/XITEONLINE/",thumbnail=icon,folder=True )
   
   from resources.lib.modules import cache, control, changelog
   cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')





def Xitelive():
    name = 'Xite Live Stream'
    url='http://xite.nl/live'
    html=make_request(url)
    html = re.compile(' <source type="application/x-mpegurl" src="(.*?)">', re.DOTALL).findall(html)
    for url in html:
        pl=xbmc.PlayList(1)
        pl.clear()
        listitem = xbmcgui.ListItem(name,thumbnailImage=icon)
        xbmc.PlayList(1).add(url, listitem)
        xbmc.Player().play(pl)


def Xitemix(url):
    name = ''
    i=0
    nexti=re.compile('http://xite.nl/videos/categorie/xite-week-mix/(.*?)\?ajax=1', re.DOTALL).findall(url)
    for i in nexti:
        i=int(i)
        i=i+1

    html=make_request(url)
    match = re.compile(r'<img src="(.*?)" />.*?<h3>(.*?)</h3>.*?<a href="(.*?)"><span>Bekijk video</span></a>', re.DOTALL).findall(html)
    for img, name, url in match:
        url = 'http://xite.nl'+url
        addDir(name ,url,4,img ,  img,'','','','')
    if name != 'XITE Year Mix - 2013':
            
        url2='http://xite.nl/videos/categorie/xite-week-mix/'+str(i)+'?ajax=1'
        addDir('Next page' ,url2,3,icon ,  FANART,'','','','')
        
 

       

def Playmix(url,name):
    html = make_request(url)
    match = re.compile('<source type="video/mp4"  src="(.*?)">', re.DOTALL).findall(html)
    for url in match:
        pl=xbmc.PlayList(1)
        pl.clear()
        listitem = xbmcgui.ListItem(name,thumbnailImage=icon)
        xbmc.PlayList(1).add(url, listitem)
        xbmc.Player().play(pl)






def getResponse(url):
    try:
        response = urllib2.urlopen(url, timeout=200)
        if response and response.getcode() == 200:
            return response
        else :
            return False
    except:
        return False
    









    
        





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
   elif mode==2 :
      Xitelive()
   elif mode==3 :
      Xitemix(url)
   elif mode==4 :
      Playmix(url,name)


except:
   print 'somethingwrong'
   traceback.print_exc(file=sys.stdout)
	

		
if not ( (mode==2 or mode==4 or mode==19 or mode==10 or mode==15 or mode==21 or mode==22 or mode==27 or mode==33 or mode==35 or mode==37 or mode==40 or mode==42 or mode==0)  )  :
	if mode==144:
		xbmcplugin.endOfDirectory(int(sys.argv[1]),updateListing=True)
	else:
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
