# -*- coding: utf-8 -*-
import os
import urllib

import globalvar

class Item:
    
    def __init__(self):
        self.name=None
        self.mode=None
        self.date=None
        self.duration=None
        self.plot=None
        self.icon=None
        self.url=None
        self.parent=None
        self.qualityName=None
        self.resolution=None
        self.fileType=None
        
    def getDisplayTitle(self):
        if self.mode=='channel':
            return self.name
        if self.mode=='folder':
            return self.name.title()
        else:
            return self.qualityName.title()
    
    def getInfoLabels(self):
        infoLabels = {
            "Title": self.name,
            "Plot": self.plot,
            "Duration": self.duration}
        return infoLabels
        
    def getKey(self):
        if self.mode=='video':
            return self.resolution
    
    def getEncodedURL(self):
        return urllib.quote(self.url, safe='')
        
class Channel(Item):
    
    def __init__(self, name, url, icon=''):
        self.name=name
        self.url=url
        self.icon=os.path.join(globalvar.MEDIA_DIR,url.split('+')[1] + '.png')
        self.mode='channel'
        
class Directory(Item):
    
    def __init__(self, name, parent, url, icon=''):
        self.name=name
        self.parent=parent
        self.url=parent + '|' + url
        self.icon=icon
        self.mode='folder'

class PrevPage(Item):
    
    def  __init__(self, parent):
        self.name='<< Page Precedente'
        self.icon=os.path.join(globalvar.MEDIA_DIR,'prev.png')
        self.parent=parent
        self.mode='folder'
        
        path=parent[:parent.rfind('+')]
        page=int(parent[-(len(parent)-parent.rfind('+')-1):])-1
        self.url=path + '+' + str(page)

class NextPage(Item):
    
    def  __init__(self, parent):
        self.name='Page Suivante >>'
        self.icon=os.path.join(globalvar.MEDIA_DIR,'next.png')
        self.parent=parent
        self.mode='folder'
        
        path=parent[:parent.rfind('+')]
        page=int(parent[-(len(parent)-parent.rfind('+')-1):])+1
        self.url=path + '+' + str(page)
        
class Video(Item):
    
    def  __init__(self, url, qualityName, resolution, fileType):
        self.name='TBD'
        self.url=url
        self.mode='video'
        self.qualityName=qualityName
        self.resolution=resolution
        self.fileType=fileType
        self.icon=''