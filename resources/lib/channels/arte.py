import json

import resources.lib.utils

title=['ARTE']
img=['arte']
readyForUse=True

urlCatalogs='http://www.arte.tv/hbbtvv2/services/web/index.php/EMAC/teasers/categories/v2/fr'
urlCatalog='http://www.arte.tv/hbbtvv2/services/web/index.php/EMAC/teasers/category/v2/%s/fr'
urlVideo='http://www.arte.tv/hbbtvv2/services/web/index.php/OPA/v3/streams/%s/SHOW/fr'

def getList(param):
    list=[]
    params=param.split("|")
    channel=params[0]
    
    if len(params)==1:
        filPrgm= resources.lib.utils.getWebContentSave(urlCatalogs,"catalog_arte_categories.json");
        jsonParser     = json.loads(filPrgm) 
        for prgm in jsonParser['categories']: 
            list.append( [prgm['title'].encode('utf-8'),param + "|" + prgm['code'].encode('utf-8'), '','','list1'] )
    elif len(params)==2:
        cat=params[1]
        filPrgm= resources.lib.utils.getWebContentSave(urlCatalog % cat,"catalog_arte_%s.json" % cat);
        jsonParser     = json.loads(filPrgm) 
        for prgm in jsonParser['category']: 
            if prgm['type']=='category':
                list.append( [prgm['title'].encode('utf-8'),param + "|" + prgm['code'].encode('utf-8'), '','','list2'] )
    elif len(params)==3:
        cat=params[2]
        filPrgm= resources.lib.utils.getWebContentSave(urlCatalog % cat,"catalog_arte_%s.json" % cat);
        jsonParser     = json.loads(filPrgm) 
        for prgm in jsonParser['category']: 
            if prgm['type']=='listing':
                for teaser in prgm['teasers']: 
                    list.append( [teaser['title'].encode('utf-8'),param + "|" + teaser['programId'].encode('utf-8'), '','','list3'] )
    elif len(params)==4: 
        file_name=''
        # get filename
        list=getList(param[:param.rfind('|')])
        for name, url, icon, infoLabels, mode in list:
            if url==param:
                file_name=resources.lib.utils.format_filename(name) + '.mp4'
        
        list=[]
        id=params[3]
        jsonParser     = json.loads(resources.lib.utils.getWebContent(urlVideo % id)) 
        for stream in jsonParser['videoStreams']:
            if stream['quality']:
                list.append([stream['audioLabel'] + " (" + str(stream['width']) + "x" + str(stream['height']) + ")",stream['url'],stream['width'] * stream['height'],[file_name,'mp4'],'video'])
    
    return list