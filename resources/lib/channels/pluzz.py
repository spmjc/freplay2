# -*- coding: utf-8 -*-
import json
import resources.lib.utils as utils
import resources.lib.item as item
import resources.lib.globalvar as globalvar
import resources.lib.m3u8 as m3u8

title = ['La 1ère', 'France 2', 'France 3', 'France 4', 'France 5', 'France Ô']
img = ['la_1ere', 'france2', 'france3', 'france4', 'france5', 'franceo']
readyForUse = True

channelCatalog = 'http://pluzz.webservices.francetelevisions.fr/' \
                 'pluzz/liste/type/replay/nb/10000/chaine/%s'

showInfo = 'http://webservices.francetelevisions.fr/tools/getInfosOeuvre/v2/' \
           '?idDiffusion=%s&catalogue=Pluzz'

imgURL = 'http://refonte.webservices.francetelevisions.fr%s'

categories = {"france2": "France 2",
              "france3": "France 3",
              "france4": "France 4",
              "france5": "France 5",
              "franceo": "France Ô",
              "guadeloupe": "Guadeloupe 1ère",
              "guyane": "Guyane 1ère",
              "martinique": "Martinique 1ère",
              "mayotte": "Mayotte 1ère",
              "nouvellecaledonie": "Nouvelle Calédonie 1ère",
              "polynesie": "Polynésie 1ère",
              "reunion": "Réunion 1ère",
              "saintpierreetmiquelon": "St-Pierre et Miquelon 1ère",
              "wallisetfutuna": "Wallis et Futuna 1ère",
              "sport": "Sport",
              "info": "Info",
              "documentaire": "Documentaire",
              "seriefiction": "Série & fiction",
              "magazine": "Magazine",
              "jeunesse": "Jeunesse",
              "divertissement": "Divertissement",
              "jeu": "Jeu",
              "culture": "Culture"}


def getList(param):
    list = []
    params=param.split("|")
    channel=utils.getChannel(param)
    uniqueItem = dict()

    realChannel = channel
    if channel == 'la_1ere':
        realChannel = 'la_1ere_reunion%2C' \
                      'la_1ere_guyane%2C' \
                      'la_1ere_polynesie%2C' \
                      'la_1ere_martinique%2C' \
                      'la_1ere_mayotte%2C' \
                      'la_1ere_nouvellecaledonie%2C' \
                      'la_1ere_guadeloupe%2C' \
                      'la_1ere_wallisetfutuna%2C' \
                      'la_1ere_saintpierreetmiquelon'

    filPrgm = utils.getWebContentSave(channelCatalog % (realChannel),'catalog_%s.json' % (channel));
    jsonParser = json.loads(filPrgm)
    emissions = jsonParser['reponse']['emissions']

    if len(params)==1:
        for emission in emissions:
            rubrique = emission['rubrique'].encode('utf-8')
            if rubrique not in uniqueItem:
                uniqueItem[rubrique] = rubrique
                list.append(item.Directory(change_to_nicer_name(rubrique),param, rubrique))

    elif len(params)==2:
        for emission in emissions:
            rubrique = emission['rubrique'].encode('utf-8')
            if rubrique == params[1]:
                titre = emission['titre_programme'].encode('utf-8')
                if titre != '':
                    id = emission['id_programme'].encode('utf-8')
                    if id == '':
                        id = emission['id_emission'].encode('utf-8')
                    if id not in uniqueItem:
                        uniqueItem[id] = id
                        list.append(item.Directory(titre,param, id,imgURL % (emission['image_large'])))
    elif len(params)==3:
        for emission in emissions:
            id = emission['id_programme'].encode('utf-8')
            if id == '':
                id = emission['id_emission'].encode('utf-8')
            if id == params[2]:
                titre=''
                image=''
                if 'titre' in emission:
                    titre = emission['titre'].encode('utf-8')
                if 'soustitre' in emission:
                    if emission['soustitre']!='':
                        titre += ' - ' + emission['soustitre'].encode('utf-8')
                if 'image_medium' in emission:
                    image = imgURL % emission['image_medium']                         
                id_diffusion = emission['id_diffusion'].encode('utf-8')
                
                i=item.Directory(titre,param,id_diffusion,image)
                if 'accroche' in emission:
                    i.plot = emission['accroche'].encode('utf-8')
                if 'real_duration' in emission:
                    i.duration = int(emission['real_duration'])
                if 'date_diffusion' in emission:
                    i.date_diffusion = emission['date_diffusion']
    
                list.append(i)
    elif len(params)==4:
        list=[]                
        filPrgm = utils.getWebContent(showInfo % (params[3]))
        jsonParser = json.loads(filPrgm)
        for video in jsonParser['videos']:
            if video['format']=='hls_v5_os':
                list=m3u8.parse_m3u8s('TBD',video['url'])
        
    return list

def change_to_nicer_name(original_name):
    if original_name in categories:
        return categories[original_name]
    return original_name