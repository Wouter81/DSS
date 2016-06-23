# -*- coding: utf-8 -*-

'''
    Liveresolver Add-on
    Copyright (C) 2016 natko1412

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urlparse,base64, urllib
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log

def resolve(url):
    #try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = 'http://zerocast.tv/channels'
        if 'chan=' in url:
            result = client.request(url, referer=referer)
            log(result)
            log('banana')
            url = re.findall('<script\stype=[\'"]text/javascript[\'"]\ssrc=[\'"](.+?)[\'"]>', result)[0]

        log('bina2')
        r = re.findall('.+?a=([0-9]+)', url)[0]

        url = 'http://zerocast.tv/embed.php?a=%s&id=&width=640&height=480&autostart=true&strech=exactfit' % r

        result = client.request(url, referer=referer)
        unpacked = ''
        packed = result.split('\n')
        for i in packed:
            try:
                unpacked += jsunpack.unpack(i)
            except:
                pass
        result += unpacked
        r = re.findall('curl\s*=\s*[\'"](.+?)[\'"]', result)
        r += re.findall('file\s*:\s*["\'](.+?)["\']', result)
        r = r[0].decode('base64', 'strict')

        #if r.startswith('rtmp'):
        #    return '%s pageUrl=%s live=1 swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf flashver=' % (r, url) + constants.flash_ver() + ' swfVfy=1 timeout=10'

        if '.m3u8' in r:
            chunk = client.request(r)
            chunk = re.compile('(chunklist_.+)').findall(chunk)[0]
            url = r.split('.m3u8')[0].rsplit('/', 1)[0] + '/' + chunk
            url += '|%s' % urllib.urlencode({'User-Agent': client.agent()})
            return url
    #except:
    #    return


