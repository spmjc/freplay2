# -*- coding: utf-8 -*-
import json

import resources.lib.utils as utils
import resources.lib.item as item

title=['ARTE']
img=['arte']
readyForUse=True

urlCatalogs='http://www.arte.tv/hbbtvv2/services/web/index.php/EMAC/teasers/categories/v2/fr'
urlCatalog='http://www.arte.tv/hbbtvv2/services/web/index.php/EMAC/teasers/category/v2/%s/fr'
urlVideo='http://www.arte.tv/hbbtvv2/services/web/index.php/OPA/v3/streams/%s/%s/fr'

def getList(param):
    list=[]
    params=param.split("|")
    channel=utils.getChannel(param)
    
    if len(params)==1:
        filPrgm= utils.getWebContentSave(urlCatalogs,"catalog_arte_categories.json");
        jsonParser     = json.loads(filPrgm) 
        for prgm in jsonParser['categories']: 
            list.append(item.Directory(prgm['title'],param,prgm['code']))
    elif len(params)==2:
        cat=params[1]
        filPrgm= utils.getWebContentSave(urlCatalog % cat,"catalog_arte_%s.json" % cat);
        jsonParser     = json.loads(filPrgm) 
        for prgm in jsonParser['category']: 
            if prgm['type']=='category':
                list.append(item.Directory(prgm['title'],param,prgm['code']))
    elif len(params)==3:
        cat=params[2]
        filPrgm= utils.getWebContentSave(urlCatalog % cat,"catalog_arte_%s.json" % cat);
        jsonParser     = json.loads(filPrgm) 
        for prgm in jsonParser['category']: 
            if prgm['type']=='listing':
                for teaser in prgm['teasers']: 
                    list.append(item.Directory(teaser['title'],param,teaser['programId'] + '+' + teaser['kind']))
    elif len(params)==4: 
        
        list=[]
        p=params[3]
        a=p.split('+')
        id=a[0]
        kind=a[1]
        jsonParser     = json.loads(utils.getWebContent(urlVideo % (id, kind))) 
        for stream in jsonParser['videoStreams']:
            list.append(item.Video(stream['url'],stream['audioLabel'] + " (" + str(stream['width']) + "x" + str(stream['height']) + ")",stream['width'] * stream['height'],'mp4'))
    
    return list