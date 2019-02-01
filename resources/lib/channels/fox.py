#-*- coding: utf-8 -*-    
import resources.lib.utils as utils
import resources.lib.item as item
import json

title=['FOX']
img=['fox']
readyForUse=True   

SHOWS = 'http://assets.fox.com/apps/FEA/v1.8/allshows.json'

def getList(param):
    list = []
    channel=utils.getChannel(param)
    params=param.split("|")
    
    if len(params)==1:
        filPrgm=utils.getWebContentSave(SHOWS,'catalog_%s.json' % channel)
        jsonParser     = json.loads(filPrgm) 
        for show in jsonParser['shows']:
            list.append(item.Directory(show['title'],param,show['stub']))
    return list