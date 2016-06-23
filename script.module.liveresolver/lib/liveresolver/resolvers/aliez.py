# -*- coding: utf-8 -*-


import re,urllib,urlparse
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log
def resolve(url):
    try:
    	page = url
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
    	except: referer = url
        result = client.request(url, referer=referer)

        url = urllib.unquote(re.findall('.*file["]*\s*:\s*["\']([^"\']+)',result)[0])
        url += ' live=true swfVfy=1 swfUrl=http://i.aliez.me/swf/playernew.swf flashver=%s pageUrl='%constants.flash_ver() + page
        return url
    except:
        return

