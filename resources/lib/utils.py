# -*- coding: utf-8 -*-
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
import item

def empty_TMP():
    if os.path.exists(globalvar.TMP_DIR) :
        shutil.rmtree(globalvar.TMP_DIR)
    if not os.path.exists(globalvar.TMP_DIR):
        os.makedirs(globalvar.TMP_DIR)
    

def getList(param):
    list=[]
    if param==None:
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
                            list.append(item.Channel(channelModule.title[i],filename + '+' + channelModule.img[i], channelModule.title[i]))
    else:
        channel=getChannel(param)
        module=getModule(param)
        
        f, filepath, description = imp.find_module(module, [globalvar.CHANNELS_DIR])
        channelModule = imp.load_module(channel, f, filepath, description)
        list=channelModule.getList(param)
        
        def getKey(itm):
            return itm.getKey()
        if len(list)>0:
            if list[0].mode=='video':
                list.sort(key=getKey,reverse=True)
    return list



def getChannel(param):
    return param.split("|")[0].split('+')[1]
    
def getModule(param):
    return param.split("|")[0].split('+')[0]
                        
def getOrderChannel(chanName):
    return 1
    
def getListFromChannel(param):
    params=param.split("|")
    channel=params[0]
    list=[]
    f, filepath, description = imp.find_module(channel, [globalvar.CHANNELS_DIR])
    try:
        channelModule = imp.load_module(channel, f, filepath, description)
        list=channelModule.getList(param)
    except Exception: 
        logging.exception("Error loading channel module " + filepath)
    
    return list

def getVideoURL(param):
    params=param.split("|")
    channel=params[0]
    videoLinks=globalvar.channels[channel][1].getVideoURL(param)
    #test()
    return videoLinks
    
def getWebContent(url,headers={}):
    if headers:
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1'}
    req = urllib2.Request(url)
    for h in headers:
        req.add_header(h, headers[h])
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
    
def url_exists(url):
    exists=True
    try:
        urllib2.urlopen(url)
    except :
        exists=False
        
    return exists
    
def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename