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
    addDir('Kompetitie' ,'',6,icon)
    addDir('Voetbal' ,'http://mapi.foxsports.nl/api/mobile/v2/soccer/articles',3,icon)
    addDir('Tennis' ,'http://mapi.foxsports.nl/api/mobile/v1/tennis/articles',3,icon)
    addDir('Meer Sports' ,'http://mapi.foxsports.nl/api/mobile/v1/articles/moresports',3,icon)
    import plugintools
    plugintools.add_item(title="Fox Sports Youtube",url="plugin://plugin.video.youtube/user/EredivisieLive/",thumbnail='https://yt3.ggpht.com/-UB8-sc_B1Kg/AAAAAAAAAAI/AAAAAAAAAAA/vxlLGekBYxU/s100-c-k-no-mo-rj-c0xffffff/photo.jpg',folder=True )
    addDir('Zoeken' ,'',15,icon)

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

def Competition_Main():
    livejson = GetHTML('http://mapi.foxsports.nl/api/mobile/v1/soccer/competitions')
    livejson = json.loads(livejson)
    for items in livejson["national"]:
        ID = items["id"]
        url = 'http://mapi.foxsports.nl/api/mobile/v2/soccer/articles/'+str(ID)
        title = items["name"]
        title = title.encode('utf-8')
        title = removeNonAscii(title)
        print title
        icon = items["icon"]
        addDir('[B][COLOR gold]'+title+'[/COLOR][/B]',url, 3, icon)
    for items in livejson["international"]:
        ID = items["id"]
        url = 'http://mapi.foxsports.nl/api/mobile/v2/soccer/articles/'+str(ID)
        title = items["name"]
        title = title.encode('utf-8')
        title = removeNonAscii(title)
        print title
        icon = items["icon"]
        addDir('[B][COLOR gold]'+title+'[/COLOR][/B]',url, 3, icon)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

def foxread(url):
    livejson = GetHTML(fox_cat+url)
    livejson = json.loads(livejson)
    for items in livejson:
        title = items["title"]
        title = title.encode('utf-8')
        title = removeNonAscii(title)
        print title
        image = items["image"]
        last_modified = items["last_modified"][0:10]
        video_id = items["video"]["diva_settings"]["video_id"]
        image = image.replace('{size}','300x184')
        url = get_video(video_id)
        if url is not None:
            addLink('[COLOR blue]'+title+'[/COLOR]  ('+last_modified+')', url, 20, image,image)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
def foxmore(url):
    livejson = GetHTML(url)
    livejson = json.loads(livejson, encoding='utf-8')
    for items in livejson["other_articles"]:
        title = items["title"]
        title = title.encode('utf-8')
        title = removeNonAscii(title)
        image = items["image"]
        image = image.replace('{size}','300x184')
        last_modified = items["last_modified"][0:10]
        if "video" in items:
            video_id = items["video"]["diva_settings"]["video_id"]
            url = get_video(video_id)
            if url is not None :
                addLink('[COLOR blue]'+title+'[/COLOR]  ('+last_modified+')', url, 20, image,image)

    for items in livejson["hero_image_articles"]:
        title = items["title"]
        title = title.encode('utf-8')
        title = removeNonAscii(title)
        image = items["image"]
        image = image.replace('{size}','300x184')
        last_modified = items["last_modified"][0:10]
        if "video" in items:
            video_id = items["video"]["diva_settings"]["video_id"]
            url = get_video(video_id)
            if url is not None :
                addLink('[COLOR blue]'+title+'[/COLOR]  ('+last_modified+')', url, 20, image,image)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def search():
    keyboard = xbmc.Keyboard('', 'Enter Zoek Naam:', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
    else:
        return
    query = query.encode('utf-8')
    query = removeNonAscii(query)
    livejson = GetHTML('http://mapi.foxsports.nl/api/mobile/v1/search/'+query)
    livejson = json.loads(livejson)
    for items in livejson:
        items = items["object"]
        title = items["title"]
        title = title.encode('utf-8')
        title = removeNonAscii(title)
        image = items["image"]
        image = image.replace('{size}','300x184')
        imported = items["date"]
        imported = str(datetime.fromtimestamp(imported))
        imported = imported[0:10]
        if "video" in items:
            video_id = items["video"]["diva_settings"]["video_id"]
            url = get_video(video_id)
            if url is not None :
                addLink('[COLOR blue]'+title+'[/COLOR]  ('+imported+')', url, 20, image,image)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_video(id):
    try:
        xmlLocation = 'http://www.foxsports.nl/divadata/Output/VideoData/'+id+'.xml'
        xml_regex = '<videoSource format="HLS" offset=".*?">\s*<DVRType>.*?</DVRType>\s*<uri>(.*?)</uri>'
        content = GetHTML(xmlLocation)
        url = re.compile(xml_regex, re.DOTALL).findall(content)
        for video in url:
            return video
    except:
        url = None
        return url



def Play(url,name):
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    dp = xbmcgui.DialogProgress()
    dp.create("foxsports.nl","Please wait")  
    xbmc.Player().play(url, liz, False)

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

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
elif mode == 6: Competition_Main()
elif mode == 7: tiplist(url)

elif mode == 11: foxread(url)
elif mode == 20: Play(url,name)
elif mode == 15: search()
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
