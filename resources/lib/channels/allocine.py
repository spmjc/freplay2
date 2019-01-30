# -*- coding: utf-8 -*-
import re

import resources.lib.utils as utils
import resources.lib.item as item

title=['Allocine']
img=['allocine']
readyForUse=True

def getList(param):
    list=[]
    params=param.split("|")
    
    if len(params)==1:      
        list.append(item.Directory('Bandes Annonces',param,'ba'))
        list.append(item.Directory('Webseries',param, '158001+1'))
        list.append(item.Directory('Mangas',param, '158002+1'))
        list.append(item.Directory('Parodies',param, '158003+1'))
        list.append(item.Directory('Emissions dActu',param, '158004+1'))
        list.append(item.Directory('Emissions Bonus',param, '158005+1'))
        list.append(item.Directory('Stars',param, '158006+1'))
        
    elif len(params)==2:
        if params[1]=='ba':        
            list.append(item.Directory('A ne pas manquer',param,'o|video/bandes-annonces/+1'))
            list.append(item.Directory('Les plus recentes',param,'o|video/bandes-annonces/plus-recentes/+1'))
            list.append(item.Directory('Bientot au cinema',param,'o|video/bandes-annonces/prochainement/+1'))
        else:
            cat,page=params[1].split('+')
            html=utils.getWebContentSave('http://www.allocine.fr/video/prgcat-' + cat + '/?page=' + page ,'allocine' + cat + '-' + page +'.html').replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
            
            match = re.compile(r'btn-primary btn-large (.*?)">(.*?)<i class="icon-arrow-(.*?)"></i>',re.DOTALL).findall(html)
            prev=False
            next=False
            for status,empty,arrow in match:
              if arrow=='left':
                prev=('disabled' not in status)
              if arrow=='right':
                next=('disabled' not in status)
            
            if prev:
                list.append(item.PrevPage(param))
                  
            match = re.compile(r'<h2 class="title "> <span > <a href="(.*?)">(.*?)</a> </span> </h2>',re.DOTALL).findall(html)
            for url,title in match: 
                list.append(item.Directory(title,param, url))
            
            if next :
                list.append(item.NextPage(param))
    
    elif len(params)==3:
        if params[2]=='o':
            list=getList(params[0] + '|' + params[1])
        else:
        
            html=utils.getWebContentSave('http://www.allocine.fr/' + params[2] ,'allocine' + params[2].replace('\\','') +'.html').replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
            
            match = re.compile(r'<a class="button btn-primary btn-large" href="(.*?)">(.*?)</a>',re.DOTALL).findall(html)
            for url,title in match:
                list.append(item.Directory(title.replace("<i class='icon-sign-plus'></i>",""),param, url + '+1'))
            
            if len(list)==0:
                list=getList(params[0] + '|' + params[1] + '|0|' + params[2] + '+1')
    elif len(params)==4:
        cat,page=params[3].split('+')
        html=utils.getWebContentSave('http://www.allocine.fr/' + cat + '/?page=' + page ,'allocine' + cat + '-' + page +'.html').replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', ' ').replace('\r', '')
        
        match = re.compile(r'btn-primary btn-large (.*?)">(.*?)<i class="icon-arrow-(.*?)"></i>',re.DOTALL).findall(html)
        prev=False
        next=False
        for status,empty,arrow in match:
            if arrow=='left':
                prev=('disabled' not in status)
            if arrow=='right':
                next=('disabled' not in status)
        if prev:
            list.append(item.PrevPage(param))
            
        match = re.compile(r'<div class="layer-link-holder"><a href="/video/player_gen_cmedia=(.*?)&amp;cfilm=(.*?).html" class="layer-link">(.*?)</a></div>',re.DOTALL).findall(html)
        if match:
            for idVideo,movie,title in match:
                title=title.replace('<strong>','').replace('</strong>','')
                list.append(item.Directory(title,param, idVideo))
                
        match = re.compile(r'<h3 class="title "> <span > <a href="/video/video-(.*?)/" itemprop="url">(.*?)</a> </span> </h3>',re.DOTALL).findall(html) 
        if match:
            for idVideo,title in match:
                title=title.replace('<strong>','').replace('</strong>','')
                list.append(item.Directory(title,param, idVideo))
        
        if next :
            list.append(item.NextPage(param))
            
    elif len(params)==5:
        id=params[4]
        xml=utils.getWebContent('http://www.allocine.fr/ws/AcVisiondataV4.ashx?media=%s' % (id)) 
        ld=re.findall('ld_path="(.*?)"', xml)[0]
        md=re.findall('md_path="(.*?)"', xml)[0]
        hd=re.findall('hd_path="(.*?)"', xml)[0]
        
        list.append(item.Video(ld,'Low Definition',1,'mp4'))
        list.append(item.Video(md,'Medium Definition',2,'mp4'))
        list.append(item.Video(hd,'High Definition',3,'mp4'))
    return list