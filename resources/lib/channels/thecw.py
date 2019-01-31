# -*- coding: utf-8 -*-
import json
import re

import resources.lib.utils as utils
import resources.lib.item as item
import resources.lib.globalvar as globalvar
import resources.lib.m3u8 as m3u8

title = ['The CW']
img = ['thecw']
readyForUse = True

listShow='http://www.cwtv.com/feed/mobileapp/shows?pagesize=100&api_version=4'
listEpisodes='http://www.cwtv.com/feed/mobileapp/videos?show=%s&api_version=4'
listVideos='http://metaframe.digitalsmiths.tv/v4/CWtv/assets/%s/partner/132?format=json'

def getList(param):
    list = []
    params=param.split("|")
    channel=utils.getChannel(param)
    uniqueItem = dict()
    
    if len(params)==1:
        filPrgm = utils.getWebContentSave(listShow ,'catalog_%s.json' % (channel))
        jsonParser = json.loads(filPrgm)
        for show in jsonParser['items']:
            list.append(item.Directory(show['title'],param, show['slug'], show['showlogo_image']))
    elif len(params)==2:
        filPrgm = utils.getWebContentSave(listEpisodes % params[1] ,'catalog_%s.json' % (channel+params[1]))
        jsonParser = json.loads(filPrgm)
        for video in jsonParser['videos']:
            if video['season'] not in uniqueItem:
                list.append(item.Directory('Season ' + video['season'] ,param, video['season']))
                uniqueItem[video['season']]=video['season']
    elif len(params)==3:
        filPrgm = utils.getWebContentSave(listEpisodes % params[1] ,'catalog_%s.json' % (channel+params[1]))
        jsonParser = json.loads(filPrgm)
        for video in jsonParser['videos']:
            if video['season'] == params[2]:
                i=item.Directory(video['episode'] + ' - ' + video['title'] ,param, video['mpx_url'], video['medium_thumbnail'])
                i.duration=video['duration_secs']
                i.plot=video['description_long']
                i.date=video['airdate']
                list.append(i)
    elif len(params)==4:
        print params[3]
        
        m3u8_url = re.compile('video src="(.+?)" ').findall(str(utils.getWebContent(params[3])))[0]
        list=m3u8.parse_m3u8s('TBD',m3u8_url)
        
    return list