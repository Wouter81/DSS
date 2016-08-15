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

wildlink = base64.b64decode('aHR0cDovL3dpbGRoaXR6LnJyLmtwbnN0cmVhbWluZy5ubC9obHMvdm9kL3dpbGRoaXR6L21wNHMv')          
wildqt = base64.b64decode('LzcyMHAyMDAwLm1wNA==')
API = base64.b64decode('aHR0cDovL3dpbGRoaXR6Lm5sL0FQSS9zb25ncy9HZXRTb25ncy5waHA/JnR5cGU9')
    
addon = xbmcaddon.Addon('plugin.video.wildhitz')
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


playlist = 'http://wildhitz.nl/jw/playlist.src.rss.php?plc=&q=jw5&autostart=true&repeat=list'

top3= 'http://wildhitz.nl/jw/playlist.src.rss.php?plc=22465216597e2084839ce5f58681264b&q=jw5&autostart=true&repeat=list'

xml_regex = '<title>(.*?)</title>\s*<jwplayer:file>(.*?)</jwplayer:file>'

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
   addDir('Live On Air' ,playlist,2,icon ,  FANART,'','','','')
   addDir('Recent' ,API+'recent',9,icon ,  FANART,'','','','')
   addDir('Popular' ,API+'popular',9,icon ,  FANART,'','','','')
   addDir('Weekend Mix' ,'http://pastebin.com/raw/C0H0i8f9',5,icon ,  FANART,'','','','')
   addDir('Daily Mix' ,'http://pastebin.com/raw/Sv1vLn0X',5,icon ,  FANART,'','','','')
   #addDir('Top 3' ,'top3',4,icon ,  FANART,'','','','')
   addDir('Playlist' ,'top3',6,icon ,  FANART,'','','','')
   addDir('VideoClips' ,'jukebox',8,icon ,  FANART,'','','','')
   addDir('Search' ,'Search',12,icon ,  FANART,'','','','')
   from resources.lib.modules import cache, control, changelog
   cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')



def Addplaylist():
   i= 1
   while True:
      url = 'http://wildhitz.nl/jw/playlist.'+str(i)+'.jw5.rss'
      title = 'Playlist - '+str(i)
      try:
         read = GetHTML(url)
         addDir(title ,url,2,icon ,  FANART,'','','','')
      except:
         break
      i=i+1
         


def Wildhitz_playlist(url):
   pl=xbmc.PlayList(1)
   pl.clear()
   xml = make_request(url)
   xml = re.compile(xml_regex, re.DOTALL).findall(xml)
   for title, url in xml:
      listitem = xbmcgui.ListItem('WildHitz - '+title,thumbnailImage=icon)
      xbmc.PlayList(1).add(url, listitem)
   xbmc.Player().play(pl)


def Wildhitz_top3():
   pl=xbmc.PlayList(1)
   pl.clear()
   xml = make_request(top3)
   xml = re.compile(xml_regex, re.DOTALL).findall(xml)
   for title, url in xml:
      listitem = xbmcgui.ListItem('WildHitz - '+title,thumbnailImage=icon)
      xbmc.PlayList(1).add(url, listitem)
   xbmc.Player().play(pl)





def CatJukebox():
   addDir('1..9' ,'1',7,icon ,  FANART,'','','','')
   addDir('A' ,'a',7,icon ,  FANART,'','','','')
   addDir('B' ,'b',7,icon ,  FANART,'','','','')
   addDir('C' ,'c',7,icon ,  FANART,'','','','')
   addDir('D' ,'d',7,icon ,  FANART,'','','','')
   addDir('E' ,'e',7,icon ,  FANART,'','','','')
   addDir('F' ,'f',7,icon ,  FANART,'','','','')
   addDir('G' ,'g',7,icon ,  FANART,'','','','')
   addDir('H' ,'h',7,icon ,  FANART,'','','','')
   addDir('I' ,'i',7,icon ,  FANART,'','','','')
   addDir('J' ,'j',7,icon ,  FANART,'','','','')
   addDir('K' ,'k',7,icon ,  FANART,'','','','')
   addDir('L' ,'l',7,icon ,  FANART,'','','','')
   addDir('M' ,'m',7,icon ,  FANART,'','','','')
   addDir('N' ,'n',7,icon ,  FANART,'','','','')
   addDir('O' ,'o',7,icon ,  FANART,'','','','')
   addDir('P' ,'p',7,icon ,  FANART,'','','','')
   addDir('Q' ,'q',7,icon ,  FANART,'','','','')
   addDir('R' ,'r',7,icon ,  FANART,'','','','')
   addDir('S' ,'s',7,icon ,  FANART,'','','','')
   addDir('T' ,'t',7,icon ,  FANART,'','','','')
   addDir('U' ,'u',7,icon ,  FANART,'','','','')
   addDir('V' ,'v',7,icon ,  FANART,'','','','')
   addDir('W' ,'w',7,icon ,  FANART,'','','','')
   addDir('Y' ,'x',7,icon ,  FANART,'','','','')
   addDir('Y' ,'y',7,icon ,  FANART,'','','','')
   addDir('Z' ,'z',7,icon ,  FANART,'','','','')
   
   



def Jukebox(cat):
   url = base64.b64decode('aHR0cDovL3d3dy5kdXRjaHNwb3J0c3RyZWFtcy5jb20veG1sL25ldy1kYXRhLnhtbA==')
   content = make_request(url)
   root = ET.fromstring(content)
   items = root.findall('item')
   for item in items:
      title = item.find('title').text
      link = item.find('url').text
      title = base64.b64decode(title).title()
      link = wildlink+base64.b64decode(link)+wildqt
      title2 = title[:1]
      if title2.lower() == cat:
         addDir(title ,link,10,icon ,  FANART,'','','','')
      else:
         title3 = title[:1]
         if  title3.isdigit():
            title3 = '1'
            if title3 == cat:
               addDir(title ,link,10,icon ,  FANART,'','','','')

def Wildscan(url):
   
   try:
      livejson = GetHTML(url)
      livejson = json.loads(livejson)
      streamlist = livejson["items"]
      for items in streamlist:
         artist = items["artist"]
         title = items["title"]
         link = items["preview"].replace("272p400","720p2000").replace(base64.b64decode('aHR0cDovL3dpbGRoaXRzdmlkZW92b2QuZG93bmxvYWQua3Buc3RyZWFtaW5nLm5sLw=='),base64.b64decode('aHR0cDovL3dpbGRoaXR6LnJyLmtwbnN0cmVhbWluZy5ubC9obHMvdm9kL3dpbGRoaXR6Lw=='))
         song = artist+' - '+title
         song = song.replace("&amp;","and").replace("&","and")
         addDir(song ,link,10,icon ,  FANART,'','','','')

   except:
      pass
   

def Search():
   keyboard = xbmc.Keyboard('', 'Enter Artits/Title:', False)
   keyboard.doModal()
   if keyboard.isConfirmed():
      query = keyboard.getText()
   else:
      return
   Wildscan(API+'search&search='+query)

   



def Wildmix(url):
   content = make_request(url)
   root = ET.fromstring(content)
   items = root.findall('item')
   for item in items:
      title = item.find('title').text
      link = item.find('link').text
      addDir(title ,link,10,icon ,  FANART,'','','','')


def playmix(name,url):
   
   listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )

   xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( url, listitem)


def keyboard(url=None):
    keyboard = xbmc.Keyboard('', 'Search Artist:', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if query == '' :
           return False
        else:
           Playlist(query)
           



def PutRequest(url):
    req_regex = '<title>(.*?)</title>'
    url = 'http://www.paradiseradio.org/sam/web/request.php?songID='+url
    request = GetHTML(url)
    match = re.compile(req_regex).findall(request)
    for dialogtext in match:
        if 'error' in request :
            match = re.compile('<h2 class=\"error\">(.*?)</h2>').findall(request)
            for status in match:
                dialog = xbmcgui.Dialog()
                dialog.ok(dialogtext, status, "Paradise Radio")
        if 'success' in request :
            match = re.compile('<h2 class=\"success\">(.*?)</h2>').findall(request)
            for status in match:
                dialog = xbmcgui.Dialog()
                dialog.ok(dialogtext, status, "Paradise Radio")

                





def Playlist(url):
   xml = '<?xml version="1.0"?>\n'+make_request(playlist)
   #xml = filter(lambda x: not x.isspace(), xml)
   xml = re.compile(xml_regex, re.DOTALL).findall(xml)
   for title, url in xml:
      if title is not "-":
         print title
         print url
         addDir(title ,url,5,icon ,  FANART,'','','','')
    



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
      Wildhitz_playlist(url)
   elif mode==3 :
      Weekendmix()
   elif mode==4 :
      Wildhitz_top3()
   elif mode==5 :
      Wildmix(url)
   elif mode==6 :
      Addplaylist()
   elif mode==7 :
      Jukebox(url)
   elif mode==8 :
      CatJukebox()
   elif mode==9 :
      Wildscan(url)
   elif mode==10 :
      playmix(name,url)

   elif mode==12 :
      Search()



except:
   print 'somethingwrong'
   traceback.print_exc(file=sys.stdout)
	

		
if not ( (mode==2 or mode==4 or mode==19 or mode==10 or mode==15 or mode==21 or mode==22 or mode==27 or mode==33 or mode==35 or mode==37 or mode==40 or mode==42 or mode==0)  )  :
	if mode==144:
		xbmcplugin.endOfDirectory(int(sys.argv[1]),updateListing=True)
	else:
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
