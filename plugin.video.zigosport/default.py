#-*- coding: utf-8 -*-

import urllib,urllib2,re, cookielib, urlparse, httplib
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,sys,time, os, gzip, socket
import time, datetime
from datetime import date, datetime, timedelta

try:
    import json
except:
    import simplejson as json
    


addon = xbmcaddon.Addon('plugin.video.zigosport')
addonname = addon.getAddonInfo('name')
addon_id = 'plugin.video.zigosport'
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


ziggosearch = 'http://go.ziggosporttotaal.nl/apiv2/video?appVersion=2.2.0&device=iphone&search='
autosport ='http://go.ziggosporttotaal.nl/apiv2/video?appVersion=2.2.0&category=autosport&device=iphone&order=recent'
golf ='http://go.ziggosporttotaal.nl/apiv2/video?appVersion=2.2.0&category=golf&device=iphone&order=recent'
other ='http://go.ziggosporttotaal.nl/apiv2/video?appVersion=2.2.0&category=other&device=iphone&order=recent'
soccer ='http://go.ziggosporttotaal.nl/apiv2/video?appVersion=2.2.0&category=soccer&device=iphone&order=recent'
tennis ='http://go.ziggosporttotaal.nl/apiv2/video?appVersion=2.2.0&category=tennis&device=iphone&order=recent'


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
    addDir('Voebal' ,soccer,1,icon)
    addDir('Racing' ,autosport,1,icon)
    addDir('Golf' ,golf,1,icon)
    addDir('Tennis' ,tennis,1,icon)
    addDir('Meer Sport' ,other,1,icon)
    addDir('Zoeken' ,'',2,icon)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))



def ziggoread(url):
    livejson = GetHTML(url)
    livejson = json.loads(livejson, encoding='utf-8')
    for items in livejson["responseObject"]["mediaItems"]:
        imported = items["imported"]
        imported = str(datetime.fromtimestamp(imported))[0:10]
        title = items["title"]
        title = title.encode('utf-8')
        title = removeNonAscii(title)
        print title
        image = items["imageUrl"]
        print image
        url = items["ipadHigh"]
        if url == None:
            url = items["iphoneHigh"]
            if url == None:
                url = items["iphoneLow"]
        print url
        duration = items["duration"]
        duration = str(timedelta(seconds=duration))
        if duration.startswith("0:"):
            duration =  duration[3:10]
        duration=  '['+duration+']'
        if url is not None : 
            addLink('[COLOR red]'+duration+'[/COLOR][B][COLOR blue]'+title+'[/COLOR][/B] ('+imported+')', url, 20, image,image)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        





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



def search():
    keyboard = xbmc.Keyboard('', 'Enter Zoek Naam:', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
    else:
        return
    query = query.encode('utf-8')
    query = removeNonAscii(query)
    url = ziggosearch+query
    try:
        ziggoread(url)
    except:
        return
    


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
elif mode == 1: ziggoread(url)
elif mode == 2: search()




elif mode == 20: Play(url,name)





xbmcplugin.endOfDirectory(int(sys.argv[1]))
