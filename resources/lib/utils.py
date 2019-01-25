import os
import imp
import logging
import urllib2
from urlparse import urlparse
import time
import shutil

import log
import globalvar
import string

def empty_TMP():
    if os.path.exists(globalvar.TMP_DIR) :
        shutil.rmtree(globalvar.TMP_DIR)
    

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