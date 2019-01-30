# -*- coding: utf-8 -*-

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
        return self.name.title()
    
    def getInfoLabels(self):
        infoLabels = {
            "Title": self.name,
            "Plot": self.plot,
            "Duration": self.duration}
        return infoLabels
        
class Channel(Item):
    
    def __init__(self, name, url, icon=''):
        self.name=name
        self.url=url
        self.icon=icon
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
        self.icon=''
        self.parent=parent
        self.mode='folder'
        
        path=parent[:parent.rfind('+')]
        page=int(parent[-(len(parent)-parent.rfind('+')-1):])-1
        self.url=path + '+' + str(page)

class NextPage(Item):
    
    def  __init__(self, parent):
        self.name='Page Suivante >>'
        self.icon=''
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
        