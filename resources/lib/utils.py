import os
import imp
import logging
import urllib2
from urlparse import urlparse
import time

import log
import globalvar
import string

import process.m3u8download


def getChannelsList():
    list=[]
    
    for subdir, dirs, files in os.walk(globalvar.CHANNELS_DIR):
        for file in files:
            filename, extension = os.path.splitext(file)
            extension = extension.upper()
            if extension == '.PY' and file != '__init__.py':
                f, filepath, description = imp.find_module(
                    filename, [globalvar.CHANNELS_DIR])
                try:
                    channelModule = imp.load_module(
                        filename, f, filepath, description)
                except Exception:
                    logging.exception(
                        "Error loading channel module " + filepath)

                if channelModule.readyForUse:
                    for i in range(0, len(channelModule.title)):
                        order = getOrderChannel(channelModule.img[i])
                        list.append( [channelModule.title[i], channelModule.img[i], channelModule.title[i], '','home'] )
                        globalvar.channels[channelModule.img[i]] = [channelModule.title[i], channelModule, order]
    return list
                        
def getOrderChannel(chanName):
    return 1

def getListFromChannel(param):
    params=param.split("|")
    channel=params[0]
    return globalvar.channels[channel][1].getList(param)

def getVideoURL(param):
    params=param.split("|")
    channel=params[0]
    videoLinks=globalvar.channels[channel][1].getVideoURL(param)
    #test()
    return videoLinks

def parse_m3u8s(url):
    req = urllib2.Request(url)
    req.add_header(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
    req.add_header('Referer', url)
    response= urllib2.urlopen(req)
    parsed_uri = urlparse(response.geturl())
    base_URL='{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri)
    base_URL=base_URL[:base_URL.rfind('/')]
    
    list=[]
    item=[]
    webcontent = response.read()
    a=webcontent.splitlines()
    
    i=0
    while i < len(a):
        line=a[i]
        if line.startswith("#EXT-X-STREAM-INF"):
            item=['','','','m3u8_mp4','video']
            line=line.replace('#EXT-X-STREAM-INF:','')
            infos=line.split(',')
            for info in infos:
                if info.startswith('RESOLUTION='):
                    item[0]=info[-len(info)+11:]
                if info.startswith('BANDWIDTH='):
                    item[2]=int(info[-len(info)+10:])
            i+=1
            line=a[i]
            item[1]=base_URL + '/' + line
            list.append(item)
        i+=1
    return list
    
def getWebContent(url):
    req = urllib2.Request(url)
    req.add_header(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
    req.add_header('Referer', url)
    response= urllib2.urlopen(req)
    webcontent = response.read()
    return webcontent
    
def getWebContentSave(url,file_name):
    file_name = format_filename(file_name)
    
    file_path = os.path.join(globalvar.TMP_DIR, file_name)
    iCtlgRefresh=3600
    
    if os.path.exists(file_path):
        mtime = os.stat(file_path).st_mtime
        dl_file = (time.time() - mtime > iCtlgRefresh)
    else:
        dl_file=True
    
    if dl_file:
        file_content = getWebContent(url)
        with open(file_path, 'wb') as f:
            f.write(file_content)
    else:
        file_content=open(file_path).read()
        
            
    return file_content
    
def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename
    
def test():
    file_path = os.path.join(globalvar.TMP_DIR, 'test.mp4')
    process.m3u8download.download_m3u8(getWebContent('http://ios-q1.tf1.fr/2/USP-0x0/13/33/13611333/ssm/13611333.ism/13611333-audio=64000.m3u8?vk=MTM2MTEzMzMubTN1OA==&st=i2OsLrutB0Ds-K9KClAQGw&e=1548380835&t=1548370035&min_bitrate='),file_path,globalvar.TMP_DIR)