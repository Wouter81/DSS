#-*- coding: utf-8 -*-

import urllib,urllib2,re, cookielib, urlparse, httplib
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,sys,time, os, gzip, socket
import time, datetime
from datetime import date, datetime, timedelta

try:
    import json
except:
    import simplejson as json
    


addon = xbmcaddon.Addon('plugin.video.vi')
addonname = addon.getAddonInfo('name')
addon_id = 'plugin.video.vi'
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


vi_home = 'http://apiv2.voetbalinside.livewallcampaigns.com/home/?page=1'
vi_day ='http://apiv2.voetbalinside.livewallcampaigns.com/top?page=1&type=day'
vi_week ='http://apiv2.voetbalinside.livewallcampaigns.com/top?page=1&type=week'
vi_month ='http://apiv2.voetbalinside.livewallcampaigns.com/top?page=1&type=month'
vi_classics ='http://apiv2.voetbalinside.livewallcampaigns.com/top?page=1&type=classics'
vi_search ='http://apiv2.voetbalinside.livewallcampaigns.com/search/?page=1&searchTerm='
vi_video = 'http://www.rtl.nl/system/s4m/vfd/version=2/d=iphone/fmt=adaptive/fun=abstract/'


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
    addDir('[B][COLOR yellow]Day[/COLOR][/B]' ,'&type=day',1,icon,page=1,channel='top',fanart=fanart)
    addDir('[B][COLOR yellow]Week[/COLOR][/B]' ,'&type=week',1,icon,page=1,channel='top',fanart=fanart)
    addDir('[B][COLOR yellow]month[/COLOR][/B]' ,'&type=month',1,icon,page=1,channel='top',fanart=fanart)
    addDir('[B][COLOR yellow]Classics[/COLOR][/B]' ,'&type=classics',1,icon,page=1,channel='top',fanart=fanart)
    addDir('[B][COLOR yellow]Zoeken[/COLOR][/B]' ,'&searchTerm=',2,icon,page=1,channel='search',fanart=fanart)
    addDir('[B][COLOR orange]---- Uitgelicht ----[/COLOR][/B]' ,'classics',0,icon,page=1,channel='top',fanart=fanart)
    vi_read('&type=',page=1,channel='home')



    xbmcplugin.endOfDirectory(int(sys.argv[1]))




        


def vi_read(url,page=None,channel=None):
    try:
        urldir=url
        livejson = GetHTML('http://apiv2.voetbalinside.livewallcampaigns.com/'+str(channel)+'?page='+str(page)+url)
        livejson = json.loads(livejson, encoding='utf-8')
        for items in livejson:
            name = str(items)
            for items in livejson[name]["items"]:
                title = items["title"]
                title = title.encode('utf-8')
                title = removeNonAscii(title)
                timeDisplay = items["timeDisplay"]
                timeDisplay =    timeDisplay.rstrip(timeDisplay[-6:])
                if "videoUuid" in items:
                    videoUuid = items["videoUuid"]
                    image = items["image"]
                    image = 'http://rtl.lwcdn.nl/imageScaled/?site=voetbalinside&file='+image+'&w=500.000000&h=500.000000&cropped=1'
                    url = get_video('http://www.rtl.nl/system/s4m/vfd/version=2/d=iphone/fmt=adaptive/fun=abstract/uuid='+videoUuid)
                    if url is not None :
                        addLink('[B][COLOR blue]'+title+ '[/COLOR][/B][COLOR red] ('+timeDisplay+')[/COLOR]', url, 20, image,image)
    except:
        pass
    if not "home" in channel:
        try:
            page =page+1
            livejson = GetHTML('http://apiv2.voetbalinside.livewallcampaigns.com/'+str(channel)+'?page='+str(page)+urldir)
            if not '"items":false' in livejson:   
                addDir('Previous Page' ,urldir,1,icon,page,channel,fanart=fanart)
        except:
            pass
            
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
    vi_read('&searchTerm='+query,page=1,channel='search')
    


def get_video(url):
    try:
        livejson = GetHTML(url)
        livejson = json.loads(livejson, encoding='utf-8')
        videohost = livejson["meta"]["videohost"]
        material = livejson["material"]
        for items in material:
            videopath = items["videopath"]
            url = videohost+videopath
            return url
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


def addDir(name, url, mode, iconimage, page,channel, section=None, keyword='', Folder=True, fanart=None):
    if url.startswith("plugin://"):
        u = url
    else:
        u = (sys.argv[0] +
             "?url=" + urllib.quote_plus(url) +
             "&mode=" + str(mode) +
             "&page=" + str(page) +
             "&channel=" + str(channel) +
             "&section=" + str(section) +
             "&keyword=" + urllib.quote_plus(keyword) +
             "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setArt({'thumb': iconimage, 'icon': iconimage})
    if fanart:
        liz.setArt({'fanart': fanart})
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=Folder)
    return ok




    


params = getParams()
url = None
name = None
mode = None
page = None
download = None
channel = None
section=None

try: url = urllib.unquote_plus(params["url"])
except: pass
try: name = urllib.unquote_plus(params["name"])
except: pass
try: mode = int(params["mode"])
except: pass
try: page=int(params["page"])
except: pass
try: channel=str(params["channel"])
except: pass
try: section=str(params["section"])
except: pass


if mode == None: MainDir()
elif mode == 1: vi_read(url,page,channel)
elif mode == 2: search()




elif mode == 20: Play(url,name)





xbmcplugin.endOfDirectory(int(sys.argv[1]))
