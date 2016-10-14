#-*- coding: utf-8 -*-

import urllib,urllib2,re, cookielib, urlparse, httplib
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,sys,time, os, gzip, socket
import time, datetime
from datetime import date, datetime, timedelta

try:
    import json
except:
    import simplejson as json
    

addon = xbmcaddon.Addon('plugin.video.dss')
addonname = addon.getAddonInfo('name')
addon_id = 'plugin.video.dss'
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


def MainDir():
    addDir('Club Channels' ,'',1,icon)
    addDir('SEBN' ,'',4,icon)
    addDir('Ziggo Sport Totaal Replays and Clips' ,'',2,icon)
    addDir('FOX Sports Videos' ,'',3,icon)
    
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def SEBN():
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]1[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-1.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]2[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-2.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]3[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-3.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]4[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-4.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]5[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-5.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]6[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-6.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]7[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-7.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]8[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-8.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]9[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-9.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]10[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-10.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]11[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-11.php', 5, 'http://sebn.sc/images/logo.png',fanart)
    addLink('[B][COLOR green]•[/COLOR][COLOR yellow]SEBN [/COLOR][COLOR red]12[/COLOR][/B]', sportsdevil+'http://sebn.sc/sebn-12.php', 5, 'http://sebn.sc/images/logo.png',fanart)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlaySEBN(url,name=None):
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    dp = xbmcgui.DialogProgress()
    dp.create("DutchSportStreams","Please wait")  
    xbmc.Player().play(url, liz, False)

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
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def MainZigo():
    addDir('Zoeken','http://www.ziggosporttotaal.nl/zoeken.html?s=',15,'https://pbs.twimg.com/profile_images/666249780998311936/dK_1dIYE.jpg') 
    addDir('Laatste video','http://www.ziggosporttotaal.nl/video/?sort=recent',13,'https://pbs.twimg.com/profile_images/666249780998311936/dK_1dIYE.jpg') 
    addDir('Meest bekeken','http://www.ziggosporttotaal.nl/video/?sort=most',13,'https://pbs.twimg.com/profile_images/666249780998311936/dK_1dIYE.jpg') 
    addDir('Voetbal','http://www.ziggosporttotaal.nl/video/1-voetbal/',13,'https://pbs.twimg.com/profile_images/666249780998311936/dK_1dIYE.jpg') 
    addDir('Racing','http://www.ziggosporttotaal.nl/video/22-racing/',13,'https://pbs.twimg.com/profile_images/666249780998311936/dK_1dIYE.jpg')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def List(url):
    listhtml = make_request(url)
    match = re.compile(r'<div class="video-list-item">.*?<a href="(.*?)">.*?img src="(.*?)".*?<span class="title">(.*?)</span>.*?<small class="date">(.*?)</small>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name, datum in match:
        name = cleantext(name) + ' - ' + datum
        videopage = "http://www.ziggosporttotaal.nl" + videopage
        img = "http://www.ziggosporttotaal.nl" + img
        addLink(name, videopage, 16, img,'https://static-ontdek.ziggo.nl/images/1920/topvisuals/3840x2880-highlights-race-campaign-new.jpg')
    try:
        nextp=re.compile('href="([^"]+)" class="nav-link icon-chevron-right"', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        next = "http://www.ziggosporttotaal.nl" + nextp.replace("&amp;","&")
        utils.addDir('Volgende Pagina', next, 13,'')
    except: pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def SearchList(url):
    listhtml = make_request(url)
    match = re.compile(r'<li class="video-list-item">.*?<a href="(.*?)" class="imgLink">.*?srcset="(.*?) 2x.*?<span class="video-title">(.*?)</span>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = cleantext(name)
        videopage = "http://www.ziggosporttotaal.nl" + videopage
        img = "http://www.ziggosporttotaal.nl" + img
        addLink(name, videopage, 16, img, 'https://static-ontdek.ziggo.nl/images/1920/topvisuals/3840x2880-highlights-race-campaign-new.jpg')
    try:
        nextp=re.compile(r'nav-link active">\d+<.*?href="([^"]+)" class="nav-link', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        next = "http://www.ziggosporttotaal.nl/zoeken.html" + nextp.replace("&amp;","&").replace(" ","+")
        addDir('Volgende Pagina', next, 14,'')
    except: pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Playvid(url, name):
    listhtml = make_request(url)
    match = re.compile(r"file: '(.*?)'").findall(listhtml)
    if match:
        videourl = match[0]
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Music'})
        listitem.setProperty("IsPlayable","true")
        if int(sys.argv[1]) == -1:
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            pl.clear()
            pl.add(videourl, listitem)
            xbmc.Player().play(pl)
        else:
            listitem.setPath(str(videourl))
            xbmcplugin.setResolvedUrl(utils.addon_handle, True, listitem)
    #else:
        #utils.notify('Oh oh','Couldn\'t find a playable video link')



def MainFox():
    addDir('Zoeken','http://www.foxsports.nl/search/videos/?q=',230,foxicon)
    addDir('Laatste Video','http://www.foxsports.nl/video/filter/fragments/1/',228,foxicon) 
    addDir('Samenvattingen','',237,foxicon)
    addDir('Doelpunten','',238,foxicon)
    addDir('Interviews','',239,foxicon)
    addDir('Analyses','http://www.foxsports.nl/video/filter/fragments/1/analyses/',228,foxicon)
    addDir('Voetbal','http://www.foxsports.nl/video/filter/fragments/1/alle/voetbal/',228,foxicon) 
    addDir('Tennis','http://www.foxsports.nl/video/filter/fragments/1/alle/tennis/',228,foxicon) 
    addDir('Overige','http://www.foxsports.nl/video/filter/fragments/1/alle/overige/',228,foxicon) 
    addDir('Aanbevolen','http://www.foxsports.nl/video/filter/fragments/1/aanbevolen/',228,foxicon) 
    addDir('Meest bekeken','http://www.foxsports.nl/video/meest_bekeken/',228,foxicon) 
    addDir('Videoklasiekers','http://www.foxsports.nl/video/filter/fragments/1/videoklassiekers/',228,foxicon) 
    addDir('Meer','http://www.foxsports.nl/video/filter/fragments/1/meer_video/',228,foxicon)  
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def MainSamenvattingen():
    addDir('Alle Samenvattingen','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/',228,foxicon)
    addDir('Voetbal Samenvattingen','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/',228,foxicon)
    addDir('Eredivisie','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/eredivisie/',228,foxicon)  
    addDir('Jupiler League','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/jupiler-league/',228,foxicon) 
    addDir('KNVB Beker','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/knvb-beker/',228,foxicon)
    addDir('UEFA Europa League','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/uefa-europa-league/',228,foxicon)
    addDir('Barclays Premier League','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/barclays-premier-league/',228,foxicon)
    addDir('Bundesliga','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/bundesliga/',228,foxicon)  
    addDir('FA Cup','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/fa-cup/',228,foxicon) 
    addDir('DFB Pokal','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/dfb-pokal/',228,foxicon)
    addDir('UEFA Europa League Kwalificatie','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/uefa-europa-league-kwalificatie/',228,foxicon)
    addDir('EK Kwalificatie','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/ek-kwalificatie/',228,foxicon)
    addDir('Tweede Bundesliga','http://www.foxsports.nl/video/filter/fragments/1/samenvattingen/voetbal/tweede-bundesliga/',228,foxicon) 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def MainDoelpunten():
    addDir('Alle Doelpunten','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/',228,foxicon)
    addDir('Eredivisie','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/eredivisie/',228,foxicon)  
    addDir('Jupiler League','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/jupiler-league/',228,foxicon) 
    addDir('KNVB Beker','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/knvb-beker/',228,foxicon)
    addDir('UEFA Europa League','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/uefa-europa-league/',228,foxicon)
    addDir('Barclays Premier League','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/barclays-premier-league/',228,foxicon)
    addDir('Bundesliga','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/bundesliga/',228,foxicon)  
    addDir('FA Cup','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/fa-cup/',228,foxicon) 
    addDir('DFB Pokal','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/dfb-pokal/',228,foxicon)
    addDir('UEFA Europa League Kwalificatie','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/uefa-europa-league-kwalificatie/',228,foxicon)
    addDir('EK Kwalificatie','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/ek-kwalificatie/',228,foxicon)
    addDir('Tweede Bundesliga','http://www.foxsports.nl/video/filter/fragments/1/doelpunten/voetbal/tweede-bundesliga/',228,foxicon) 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def MainInterviews():
    addDir('Alle Doelpunten','http://www.foxsports.nl/video/filter/fragments/1/interviews/',228,foxicon)
    addDir('Eredivisie','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/eredivisie/',228,foxicon)  
    addDir('Jupiler League','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/jupiler-league/',228,foxicon) 
    addDir('KNVB Beker','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/knvb-beker/',228,foxicon)
    addDir('UEFA Europa League','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/uefa-europa-league/',228,foxicon)
    addDir('Barclays Premier League','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/barclays-premier-league/',228,foxicon)
    addDir('Bundesliga','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/bundesliga/',228,foxicon)  
    addDir('FA Cup','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/fa-cup/',228,foxicon) 
    addDir('DFB Pokal','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/dfb-pokal/',228,foxicon)
    addDir('UEFA Europa League Kwalificatie','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/uefa-europa-league-kwalificatie/',228,foxicon)
    addDir('EK Kwalificatie','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/ek-kwalificatie/',228,foxicon)
    addDir('Tweede Bundesliga','http://www.foxsports.nl/video/filter/fragments/1/interviews/voetbal/tweede-bundesliga/',228,foxicon) 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

def ListFox(url):
    try:
        page = get_num(url)
    except:
        page = 1
    listhtml = make_request(url)
    match = re.compile("""src='([^']+)' alt='([^<]+)'>.*?href="([^"]+)""", re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, name, videopage in match:
        name = cleantext(name)
        videopage = "http://www.foxsports.nl" + videopage
        addLink(name, videopage, 231, img,img)
    if len(match) == 12:
        npage = page + 1        
        url = url.replace('/'+str(page)+'/','/'+str(npage)+'/')
        addDir('Volgende Pagina ', url, 228, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def SearchListFox(url, page=None):
    listhtml = make_request(url)
    match = re.compile(r'<article class="dcm-article">.*?<a href="(.*?)">.+?src="(.*?)".*?<a href=".*?">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = cleantext(name)
        addLink(name, videopage, 231, img,img)
    try:
        nextp=re.compile(r'dcm-active">\d+<.*?href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        next = "http://www.foxsports.nl/video/search/" + nextp.replace("&amp;","&").replace(" ","%20")
        addDir('Volgende Pagina', next, 229,'')
    except: pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayvidFox(url, name):
    listhtml = make_request(url)
    videoid = re.compile('data-videoid="(.*?)"', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    videoid = 'http://www.foxsports.nl/divadata/Output/VideoData/' + videoid + '.xml'
    videoxml = make_request(videoid)
    videourl = re.compile(r'<uri>([^<]+m3u8)</uri>', re.DOTALL | re.IGNORECASE).findall(videoxml)[0]
    if videourl:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Music'})
        listitem.setProperty("IsPlayable","true")
        if int(sys.argv[1]) == -1:
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            pl.clear()
            pl.add(videourl, listitem)
            xbmc.Player().play(pl)
        else:
            listitem.setPath(str(videourl))
            xbmcplugin.setResolvedUrl(utils.addon_handle, True, listitem)


#sportsdevil = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +i.string
#referer = item('referer')[0].string
#if referer:
#print 'referer found'
#sportsdevil = sportsdevil + '%26referer=' +referer


def Search(url):
    searchUrl = url
    vq = _get_keyboard(heading="Zoeken naar...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    SearchList(searchUrl)    


def SearchFox(url):
    searchUrl = url
    vq = _get_keyboard(heading="Zoeken naar...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    SearchListFox(searchUrl)  


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
elif mode == 1: CatClubchannels()
elif mode == 2: MainZigo()
elif mode == 3: MainFox()
elif mode == 4: SEBN()
elif mode == 5: PlaySEBN(url)
elif mode == 6: tipweeknumbers(url)
elif mode == 7: tiplist(url)

elif mode == 13: List(url)
elif mode == 14: SearchList(url)
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
