#-*- coding: utf-8 -*-

import urllib,urllib2,re, cookielib, urlparse, httplib
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,sys,time, os, gzip, socket
import time, datetime
from datetime import date, datetime, timedelta

try:
    import json
except:
    import simplejson as json
    


addon = xbmcaddon.Addon('plugin.video.foxsports.nl')
addonname = addon.getAddonInfo('name')
addon_id = 'plugin.video.foxsports.nl'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8')) 
icon = os.path.join(home, 'icon.png')
fanart = os.path.join(home, 'fanart.jpg')


addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])

class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response


foxicon = 'http://www.foxsports.nl/images/ml/logos/logo.png'
sportsdevil = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='
fox_cat = 'http://mapi.foxsports.nl/api/mobile/v1/articles/category/'


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

def GetHTML(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def MainDir():
    addDir('Uitzending Gemist' ,'',1,icon)
    addDir('Video\'s' ,'',2,icon)
    #addDir('Eredivisie' ,'http://mapi.foxsports.nl/api/mobile/v2/soccer/articles/9',3,icon)
    addDir('Tennis' ,'http://mapi.foxsports.nl/api/mobile/v1/tennis/articles',3,icon)
    addDir('Meer Sports' ,'http://mapi.foxsports.nl/api/mobile/v1/articles/moresports',3,icon)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def Uitzending_Gemist():
    addDir('[B][COLOR gold]Fox Sports DOC[/COLOR][/B]','115', 11, icon)
    addDir('[B][COLOR gold]Club TV[/COLOR][/B]', '116', 11, icon)
    addDir('[B][COLOR gold]De Tafel Van Kees[/COLOR][/B]','117', 11, icon)
    addDir('[B][COLOR gold]Fox Sports Vandaag[/COLOR][/B]','118', 11, icon)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def Video_s():
    addDir('[B][COLOR gold]Samenvattingen[/COLOR][/B]','1', 11, icon)
    addDir('[B][COLOR gold]Doelpunten[/COLOR][/B]','2', 11, icon)
    addDir('[B][COLOR gold]Interviews[/COLOR][/B]','3', 11, icon)
    addDir('[B][COLOR gold]Aanbevolen[/COLOR][/B]','4', 11, icon)
    addDir('[B][COLOR gold]Meest Bekeken[/COLOR][/B]','5', 11, icon)
    addDir('[B][COLOR gold]Meer Video[/COLOR][/B]','6', 11, icon)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))



def foxread(url):
    livejson = GetHTML(fox_cat+url)
    livejson = json.loads(livejson)
    for items in livejson:
        title = items["title"]
        title = title.encode('utf-8')
        #title = title.replace("'","")
        print title
        image = items["image"]
        xdate = items["last_modified"][0:10]
        video_id = items["video"]["diva_settings"]["video_id"]
        image = image.replace('{size}','300x184')
        url = get_video(video_id)
        if url is not None:
            addLink('[COLOR blue]'+title+'[/COLOR]', url, 20, image,image)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
def foxmore(url):
    livejson = GetHTML(url)
    #print livejson
    livejson = json.loads(livejson)
    for items in livejson["other_articles"]:
        try:
            title = items["title"]
            title = safe_unicode(title)
            title = title.encode('utf-8')
            print title
            image = items["image"]
            last_modified = items["last_modified"][0:10]
            try:
                video_id = items["video"]["diva_settings"]["video_id"]
            except:
                video_id = None
            image = image.replace('{size}','300x184')
            if video_id is not None:
                url = get_video(video_id)
                addLink('[COLOR blue]'+title+'[/COLOR]  ('+last_modified+')', url, 20, image,image)
        except:
            pass

    for items in livejson["hero_image_articles"]:
        try:
            title = items["title"]
            title = safe_unicode(title)
            title = title.encode('utf-8')
            image = items["image"]
            last_modified = items["last_modified"][0:10]
            try:
                video_id = items["video"]["diva_settings"]["video_id"]
            except:
                video_id = None
            image = image.replace('{size}','300x184')
            if video_id is not None:
                url = get_video(video_id)
                addLink('[COLOR blue]'+title+'[/COLOR]  ('+last_modified+')', url, 20, image,image)
        except:
            pass


    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_video(id):
    xmlLocation = 'http://www.foxsports.nl/divadata/Output/VideoData/'+id+'.xml'
    xml_regex = '</videoSource>\s*<videoSource format="HLS" offset=".*?">\s*<DVRType>.*?l</DVRType>\s*<uri>(.*?)</uri>'
    content = make_request(xmlLocation)
    #print content
    url = re.compile(xml_regex, re.DOTALL).findall(content)
    for video in url:
        return video



def Play(url,name):
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    dp = xbmcgui.DialogProgress()
    dp.create("foxsports.nl","Please wait")  
    xbmc.Player().play(url, liz, False)

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape') 

def getParams():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def addLink(name,url,mode,iconimage,fanartimage):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    video_streaminfo = {'codec': 'h264'}
    liz.addStreamInfo('video', video_streaminfo)
    liz.setProperty("Fanart_Image", fanartimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def addDir(name,url,mode,iconimage):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    liz.setProperty("Fanart_Image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def _get_keyboard(default="", heading="", hidden=False):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return unicode(keyboard.getText(), "utf-8")
    return default

def cleantext(text):
    text = text.replace('&#8211;','-')
    text = text.replace('&#038;','&')
    text = text.replace('&#8217;','\'')
    text = text.replace('&#8216;','\'')
    text = text.replace('&#8230;','...')
    text = text.replace('&quot;','"')
    text = text.replace('&#039;','`')
    text = text.replace('&amp;','&')
    text = text.replace('&ntilde;','ñ')
    text = text.replace("&#39;","'")
    text = text.replace('&#233;','é')
    text = text.replace('&#252;','ü')
    text = text.replace('&nbsp;',' ')
    text = text.replace('&iacute;','í')
    text = text.replace('&acute;','´')
    text = text.replace('&bull;','-')
    return text


params = getParams()
url = None
name = None
mode = None
download = None

try: url = urllib.unquote_plus(params["url"])
except: pass
try: name = urllib.unquote_plus(params["name"])
except: pass
try: mode = int(params["mode"])
except: pass



if mode == None: MainDir()
elif mode == 1: Uitzending_Gemist()
elif mode == 2: Video_s()
elif mode == 3: foxmore(url)
elif mode == 4: SEBN()
elif mode == 5: PlaySEBN(url)
elif mode == 6: tipweeknumbers(url)
elif mode == 7: tiplist(url)

elif mode == 11: foxread(url)
elif mode == 20: Play(url,name)
elif mode == 15: Search(url)
elif mode == 16: Playvid(url, name)


elif mode == 227: MainFox()
elif mode == 228: ListFox(url)
elif mode == 229: SearchListFox(url)
elif mode == 230: SearchFox(url)
elif mode == 231: PlayvidFox(url, name)
elif mode == 237: MainSamenvattingen()
elif mode == 238: MainDoelpunten()
elif mode == 239: MainInterviews()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
