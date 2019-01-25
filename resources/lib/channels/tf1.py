import json

import resources.lib.utils
import resources.lib.m3u8

title=['TF1','TMC','TFX','TF1 Series Films']
img=['tf1','tmc','tfx','tf1-series-films']
readyForUse=True

urlCatalog='http://api.mytf1.tf1.fr/mobile/2/init?device=ios-tablet'

def getList(param):
    list=[]
    params=param.split("|")
    channel=params[0]
    
    if(len(params)<4):
        filPrgm= resources.lib.utils.getWebContentSave(urlCatalog,"catalog_tf1.json");
        jsonParser     = json.loads(filPrgm) 
        uniqueItem = dict()  
    
    if len(params)==1:
        for prgm in jsonParser['programs'] :
            if channel in prgm['channels']:
                if prgm['category'] not in uniqueItem: 
                    list.append( [prgm['category'].encode('utf-8'),param + "|" + prgm['categorySlug'].encode('utf-8'), '','','list1'] )
                    uniqueItem[prgm['category']] = prgm['category']
    elif len(params)==2:
        for prgm in jsonParser['programs'] : 
            if channel in prgm['channels']:
                if prgm['categorySlug']==params[1]: 
                    list.append( [prgm['title'].encode('utf-8'),param+ "|" + prgm['id'].encode('utf-8'), "",'','list2'] )
    elif len(params)==3:
        for vid in jsonParser['videos'] :
            if vid['programId'] ==params[2]:
                if vid['videoType']['type']=='replay' or vid['videoType']['type']=='video' or vid['videoType']['type']=='extract':
                    title=vid['title'].encode('utf-8')         
                    plot, duration = '', ''
                    if 'summary' in vid : plot=vid['summary'].encode('utf-8')       
                    if 'length' in vid  :duration=vid['length']/60 
                    infoLabels = { "Title": title,"Plot":plot,"Duration": duration}
                    list.append( [title,param + "|" + vid['streamId'].encode('utf-8'), '',infoLabels,'list3'] )
    elif len(params)==4:
        file_name=''
        # get filename
        list=getList(param[:param.rfind('|')])
        for name, url, icon, infoLabels, mode in list:
            print url + param
            if url==param:
                file_name=resources.lib.utils.format_filename(name) + '.mp4'
                
        params=param.split("|")
        id=params[3]
        VideoURL= 'http://wat.tv/get/ipad/' + id
        return resources.lib.m3u8.parse_m3u8s(file_name,VideoURL)
    
    return list