# -*- coding: utf-8 -*-
import json

import urllib2
import urllib
import urlparse
import base64
import hashlib

import resources.lib.utils as utils
import resources.lib.item as item
import resources.lib.m3u8 as m3u8

title=['TF1','TMC','TFX','TF1 Series Films']
img=['tf1','tmc','tfx','tf1-series-films']
readyForUse=True

urlCatalog='http://api.mytf1.tf1.fr/mobile/2/init?device=ios-tablet'

def getList(param):
    list=[]
    params=param.split("|")
    channel=utils.getChannel(param)
    
    if(len(params)<4):
        filPrgm= utils.getWebContentSave(urlCatalog,"catalog_tf1.json");
        jsonParser     = json.loads(filPrgm) 
        uniqueItem = dict()  
    
    if len(params)==1:
        for prgm in jsonParser['programs'] :
            if channel in prgm['channels']:
                if prgm['category'] not in uniqueItem: 
                    list.append(item.Directory(prgm['category'],param, prgm['categorySlug']))
                    #list.append( [prgm['category'].encode('utf-8'),param + "|" + prgm['categorySlug'].encode('utf-8'), '','','list1'] )
                    uniqueItem[prgm['category']] = prgm['category']
    elif len(params)==2:
        for prgm in jsonParser['programs'] : 
            if channel in prgm['channels']:
                if prgm['categorySlug']==params[1]: 
                    list.append(item.Directory(prgm['title'],param, prgm['id']))
                    #list.append( [prgm['title'].encode('utf-8'),param+ "|" + prgm['id'].encode('utf-8'), "",'','list2'] )
    elif len(params)==3:
        for vid in jsonParser['videos'] :
            if vid['programId'] ==params[2]:
                if vid['videoType']['type']=='replay' or vid['videoType']['type']=='video' or vid['videoType']['type']=='extract':
                    #title=vid['title'].encode('utf-8')         
                    #plot, duration = '', ''
                    #if 'summary' in vid : plot=vid['summary'].encode('utf-8')       
                    #if 'length' in vid  :duration=vid['length']/60
                    i=item.Directory(vid['title'],param, vid['streamId'])
                    if 'summary' in vid : i.plot=vid['summary']       
                    if 'length' in vid  : i.duration=vid['length']/60
                    list.append(i)
                    #list.append( [title,param + "|" + vid['streamId'].encode('utf-8'), '',infoLabels,'list3'] )
    elif len(params)==4:
        params=param.split("|")
        id=params[3]
        VideoURL= 'http://wat.tv/get/ipad/' + id
        
        content= utils.getWebContent(VideoURL)
        if content=='':
            jsonParser= json.loads(utils.getWebContent('http://www.wat.tv/get/webhtml/' + id))
            VideoURL= jsonParser['hls']
        
        list=m3u8.parse_m3u8s('TBD',VideoURL)
    
    return list