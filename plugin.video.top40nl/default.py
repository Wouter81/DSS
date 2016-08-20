#-*- coding: utf-8 -*-

import urllib,urllib2,re, cookielib, urlparse, httplib
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,sys,time, os, gzip, socket
import time, datetime
from datetime import date, datetime, timedelta

try:
    import json
except:
    import simplejson as json
    

addon = xbmcaddon.Addon('plugin.video.top40nl')
addonname = addon.getAddonInfo('name')
addon_id = 'plugin.video.top40nl'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8')) 
icon = os.path.join(home, 'icon.png')
fanart = os.path.join(home, 'fanart.jpg')


addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])




def MainDir():
    addDir('Top 40 Overzicht' ,'',4,icon)
    addDir('Tipparade Overzicht' ,'',5,icon)
    addLink('Top 40 Radio' ,'http://vip-icecast.538.lw.triple-it.nl/WEB02_MP3',3,icon,fanart)
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def Top40():
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y')
    
    st = int(st)
    while st != 1964:
        addDir('Top40 '+str(st) ,str(st),1,icon)
        st = st - 1
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Tipparade():
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y')
    
    st = int(st)
    while st != 1966:
        addDir('Tipparade '+str(st) ,str(st),6,icon)
        st = st - 1
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def weeknumbers(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Scanning Top40.nl Year '+url)
    year = url
    maxweek =int(lastweek(year))
    b= 0
    xweek = 0 
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    rdate = firstweek(year) 
    try:
        while str(url) == str(year) and b < maxweek:
            data = GetHTML('http://www.top40.nl/app_api/top40_json/1?date='+rdate)
            data = json.loads(data)
            for i in data:
                
                year =i['year']
                week =i['week']
                xdate = i['date']
                if str(url) == str(year) :
                    progress.update( 1+ (int(week)*2), "Scanning Top40.nl Year %d"%year, "Finding week %d"%week, "" )
                    if xweek != week: 
                        addDir('Top40.nl '+str(year)+' week '+str(week) ,xdate,2,icon)   
                try:
                    xdate = datetime.strptime(xdate, '%Y-%m-%d')
                except TypeError:
                    xdate = datetime(*(time.strptime(xdate, '%Y-%m-%d')[0:6]))
                xdate = xdate + timedelta(days=7)
                xdate = xdate.strftime('%Y-%m-%d')
                rdate = xdate
                b = b+1
                xweek = week        
    except:
        pass
    progress.close()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def hitlist(url):
    try:
        data = GetHTML('http://www.top40.nl/app_api/top40_json/1?date='+url)
        data = json.loads(data)
        for i in data:
            positions = i['positions']
            for x in positions:
                position = x['position']
                title = x['title']
                title = title.encode('utf-8')
                credit = x['credit']
                credit = credit.encode('utf-8')
                prev_position = x['prev_position']
                cover_img_url_medium = x['cover_img_url_medium']
                if cover_img_url_medium == None:
                    cover_img_url_medium = ''
                else:
                    cover_img_url_medium = x['cover_img_url_medium']
                cover_img_url_large = x['cover_img_url_large']
                if cover_img_url_large == None :
                    cover_img_url_large = ''
                else:
                    cover_img_url_large = x['cover_img_url_large']
                youtube_url = x['youtube_url']
                if youtube_url == None :
                    Noclip = ' [Geen Video Clip]'
                    youtube_url = 'http://'   
                else:
                    Noclip = ''
                    youtube_url = x['youtube_url']
                trackid = '[COLOR green]['+str(position)+'][/COLOR]<-[COLOR yellow]['+str(prev_position)+'][/COLOR][COLOR orange] '+credit+' - '+title+'[/COLOR] '+Noclip
                addLink(trackid ,youtube_url,3,cover_img_url_medium,cover_img_url_large)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
        pass



def firstweek(_year):
    year = 0
    _date = _year+'-01-02'
    _year = int(_year)
    try:
        while year != _year:     
            data = GetHTML('http://www.top40.nl/app_api/top40_json/1?date='+_date)
            data = json.loads(data)
            for i in data:
                year =i['year']
                week =i['week']
                xdate = i['date']
                xdate = xdate.encode('utf-8')
                try:
                    _date = datetime.strptime(_date, '%Y-%m-%d')
                except TypeError:
                    _date = datetime(*(time.strptime(_date, '%Y-%m-%d')[0:6]))
                _date = _date + timedelta(days=1)
                _date = _date.strftime('%Y-%m-%d')
        return xdate
    except:
        return _date
    
def tipfirstweek(_year):
    year = 0
    _date = _year+'-01-02'
    _year = int(_year)
    try:
        while year != _year:     
            data = GetHTML('http://www.top40.nl/app_api/top40_json/3?date='+_date)
            data = json.loads(data)
            for i in data:
                year =i['year']
                week =i['week']
                xdate = i['date']
                try:
                    _date = datetime.strptime(_date, '%Y-%m-%d')
                except TypeError:
                    _date = datetime(*(time.strptime(_date, '%Y-%m-%d')[0:6]))
                _date = _date + timedelta(days=1)
                _date = _date.strftime('%Y-%m-%d')
        return xdate
    except:
        return _date

def lastweek(_year):
    _date = str(_year)+'-12-31'
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    try:
        data = GetHTML('http://www.top40.nl/app_api/top40_json/1?date='+_date)
        data = json.loads(data)
        for i in data:
            week =i['week']
            if week == 0 :
                st = st + datetime.timedelta(days=2)
                data = GetHTML('http://www.top40.nl/app_api/top40_json/1?date='+st)
                data = json.loads(data)
                for i in data:
                    week =i['week']
                    return week
            else :
                return week
    except:
        week = 52
        return week

def tiplastweek(_year):
    _date = str(_year)+'-12-31'
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    try:
        data = GetHTML('http://www.top40.nl/app_api/top40_json/3?date='+_date)
        data = json.loads(data)
        for i in data:
            week =i['week']
            if week == 0 :
                st = st + datetime.timedelta(days=2)
                data = GetHTML('http://www.top40.nl/app_api/top40_json/1?date='+st)
                data = json.loads(data)
                for i in data:
                    week =i['week']
                    return week
            else :
                return week
    except:
        week = 52
        return week

def tipweeknumbers(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Scanning Top40.nl Tipparade Year '+url)
    year = url
    maxweek =int(tiplastweek(year))
    b= 0
    xweek = 0 
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    rdate = tipfirstweek(year) 
    try:
        while str(url) == str(year) and b < maxweek:
            data = GetHTML('http://www.top40.nl/app_api/top40_json/3?date='+rdate)
            data = json.loads(data)
            for i in data:                
                year =i['year']
                week =i['week']
                xdate = i['date']
                if str(url) == str(year) :
                    progress.update( 1+ (int(week)*2), "Scanning Top40.nl Tipparade Year %d"%year, "Finding week %d"%week, "" )
                    if xweek != week: 
                        addDir('Top40.nl Tipparade '+str(year)+' week '+str(week) ,xdate,7,icon) 
                try:
                    xdate = datetime.strptime(xdate, '%Y-%m-%d')
                except TypeError:
                    xdate = datetime(*(time.strptime(xdate, '%Y-%m-%d')[0:6]))
                xdate = xdate + timedelta(days=7)
                xdate = xdate.strftime('%Y-%m-%d')
                rdate = xdate
                b = b+1
                xweek = week        
    except:
        pass
    progress.close()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def tiplist(url):
    try:
        data = GetHTML('http://www.top40.nl/app_api/top40_json/3?date='+url)
        data = json.loads(data)
        for i in data:
            positions = i['positions']
            for x in positions:
                position = x['position']
                title = x['title']
                title = title.encode('utf-8')
                credit = x['credit']
                credit = credit.encode('utf-8')
                prev_position = x['prev_position']
                cover_img_url_medium = x['cover_img_url_medium']
                if cover_img_url_medium == None:
                    cover_img_url_medium = ''
                else:
                    cover_img_url_medium = x['cover_img_url_medium']
                cover_img_url_large = x['cover_img_url_large']
                if cover_img_url_large == None :
                    cover_img_url_large = ''
                else:
                    cover_img_url_large = x['cover_img_url_large']
                youtube_url = x['youtube_url']
                if youtube_url == None :
                    Noclip = ' [Geen Video Clip]'
                    youtube_url = 'http://'   
                else:
                    Noclip = ''
                    youtube_url = x['youtube_url']
                trackid = '[COLOR green]['+str(position)+'][/COLOR]<-[COLOR yellow]['+str(prev_position)+'][/COLOR][COLOR orange] '+credit+' - '+title+'[/COLOR] '+Noclip
                addLink(trackid ,youtube_url,3,cover_img_url_medium,cover_img_url_large)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
        pass

def PlayVideo(name,url):
    streamUrl =  url
    streamUrl=streamUrl.replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/play/?video_id=').strip()
    xbmc.log(streamUrl)
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    listitem.setInfo('video', {'Title': name})
    xbmc.Player().play(streamUrl, listitem)

  



def GetHTML(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

    


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
elif mode == 1: weeknumbers(url)
elif mode == 2: hitlist(url)
elif mode == 3: PlayVideo(name,url)
elif mode == 4: Top40()
elif mode == 5: Tipparade()
elif mode == 6: tipweeknumbers(url)
elif mode == 7: tiplist(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
