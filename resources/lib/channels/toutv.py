#-*- coding: utf-8 -*-    
import resources.lib.utils as utils
import resources.lib.item as item
import json

title=['Tou.tv']
img=['toutv']
readyForUse=True          

urlCatalog='http://ici.tou.tv/presentation/section/rattrapage?v=2&d=ipad&includePartnerTeaser=false'

def canPlay(item):
  if item['IsFree'] and item['IsActive']:
    return True
    
def getList(param):
    list = []
    params=param.split("|")
    
    filPrgm=utils.getWebContentSave(urlCatalog,'TouTV.json')
    jsonParser     = json.loads(filPrgm) 
    uniqueItem = dict()  
    
    if len(params)==1:
        
        for lineup in jsonParser['Lineups'] :
            for lineupitem in lineup['LineupItems'] :
                if canPlay(lineupitem):
                    if lineupitem['Title'] is not None: 
                        if lineupitem['Title'] not in uniqueItem: 
                            list.append(item.Directory(lineupitem['Title'],param,lineupitem['Title'],lineupitem['ImageUrl']))
                            uniqueItem[lineupitem['Title']] = lineupitem['Title']
    
    elif len(params)==2:
        
        for lineup in jsonParser['Lineups'] :
            for lineupitem in lineup['LineupItems'] :
                if canPlay(lineupitem):
                    if lineupitem['Title'] is not None: 
                        if lineupitem['Title'] == params[1]: 
                            details=lineupitem['Details']
                            
                            titre          = params[1]
                            if lineupitem['PromoDescription'] is not None:
                              titre+='-' + lineupitem['PromoDescription']  
                            image      = details['ImageUrl']
                            url= lineupitem['Url']
                            i=item.Directory(titre,param,url,image)
                            i.plot=details['Description']
                            i.duration=details['Length']/60
                            list.append(i)
    
    elif len(params)==3:
        filPrgm=utils.getWebContent('http://ici.tou.tv/presentation%s?v=2&d=ipad&includePartnerTeaser=false' % (params[2]))
        jsonParser     = json.loads(filPrgm)
        IdMedia=jsonParser['IdMedia']
        filPrgm=utils.getWebContent('http://api.radio-canada.ca/ValidationMedia/v1/Validation.html?appCode=toutv&idMedia=%s&deviceType=ipad&output=json'% (IdMedia))
        print 'http://api.radio-canada.ca/ValidationMedia/v1/Validation.html?appCode=toutv&idMedia=%s&deviceType=ipad&output=json'% (IdMedia)
        jsonParser     = json.loads(filPrgm)
        print jsonParser['url'] 
        
    return list