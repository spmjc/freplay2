#-*- coding: utf-8 -*-    
import resources.lib.utils as utils
import resources.lib.item as item
import json

title=['ABC']
img=['abc']
readyForUse=True          
BRANDID = "001"

SHOWS = 'http://api.watchabc.go.com/vp2/ws/s/contents/2015/shows/jsonp/%s/001/-1'
VIDEOLIST = 'http://api.watchabc.go.com/vp2/ws/s/contents/2015/videos/jsonp/%s/001/-1/%s/-1/-1/-1/-1'
VIDEOURL = 'http://api.watchabc.go.com/vp2/ws/s/contents/2015/videos/jsonp/%s'
PLAYLISTMOV = 'http://www.kaltura.com/p/%s/sp/%s00/playManifest/format/rtmp/entryId/'
PLAYLISTMP4 = 'http://www.kaltura.com/p/%s/sp/%s00/playManifest/format/applehttp/entryId/'
PLAYLISTM3U = 'http://cdnapi.kaltura.com/p/%s/sp/%s00/playManifest/format/url/protocol/http/entryId/'
CLOSEDCAPTIONHOST = 'http://cdn.video.abc.com'
GETAUTHORIZATION = 'http://api.watchabc.go.com/vp2/ws-secure/entitlement/2015/authorize/json'
SWFURL = 'http://livepassdl.conviva.com/ver/2.61.0.65970/LivePassModuleMain.swf'

def getList(param):
    list = []
    channel=utils.getChannel(param)
    params=param.split("|")
    
    if len(params)==1:
        filPrgm=utils.getWebContentSave(SHOWS % BRANDID,'catalog_%s.json' % channel)
        jsonParser     = json.loads(filPrgm) 
        uniqueItem = dict()  
        for show in jsonParser['shows']['show'] :
            if show['genre'] not in uniqueItem:
                list.append(item.Directory(show['genre'],param,show['genre']))
                uniqueItem[show['genre']] = show['genre']
                
    if len(params)==2:
        filPrgm=utils.getWebContentSave(SHOWS % BRANDID,'catalog_%s.json' % channel)
        jsonParser     = json.loads(filPrgm) 
        uniqueItem = dict()  
        for show in jsonParser['shows']['show'] :
            imgURL=''
            if show['genre']==params[1]:
                if 'thumbnails' in show:
                    if show['thumbnails']!='':
                        for img in show['thumbnails']['thumbnail'] :
                            if img['@type']=='main':
                                imgURL=img['$']
                list.append(item.Directory(show['title'],param,show['@id'],imgURL))
    if len(params)==3:
        filPrgm=utils.getWebContentSave(VIDEOLIST % (BRANDID,params[2]),'catalog_%s.json' % params[2])
        jsonParser     = json.loads(filPrgm) 
        uniqueItem = dict()  
        for show in jsonParser['videos']['video'] :
                list.append(item.Directory(show['title'],param,show['url']))
    return list