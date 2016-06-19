import urllib2, re

_url_ = 'https://www.whatismyip.com/'
_reg_pattern_ = '<td>Country:</td><td>([A-Z]*)</td>'

def returnCountyCode() :
    match = re.findall(_reg_pattern_,_GEO_getUrl(_url_))
    try :
        return match[0]
    except :
        return ""
    
def _GEO_getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):

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