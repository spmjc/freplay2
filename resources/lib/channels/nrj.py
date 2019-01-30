#-*- coding: utf-8 -*-
import urllib2
import re
import base64
from resources.lib import utils
import resources.lib.item as item

title=['NRJ12','Chérie 25']
img=['nrj12','cherie25']

readyForUse=True

def getList(param):
    list=[]
    params=param.split("|")
    channel=utils.getChannel(param)
    
    if len(params)==1:
        html=utils.getWebContent('http://www.nrj-play.fr/%s/replay' % channel).replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
        html=' '.join(html.split())
        match = re.compile(r'<li class="subNav-menu-item">(.*?)<a href="(.*?)" class=(.*?)>(.*?)</a>',re.DOTALL).findall(html)
        if match:
            for empty,link,empty2,title in match:
                if 'active' not in empty2:
                    list.append(item.Directory(title,param, link))
    if len(params)==2:
        html=utils.getWebContent('http://www.nrj-play.fr%s' % (params[1])).replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
        html=' '.join(html.split()) 
        
        match = re.compile(r'<h2 class="linkProgram-title"> <a href="(.*?)">(.*?)</a> </h2>',re.DOTALL).findall(html)
        if match:
            for link,title in match:
                list.append(item.Directory(title,param, link))
    if len(params)==3:
        html=utils.getWebContent('http://www.nrj-play.fr%s' % (params[2])).replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
        html=' '.join(html.split())    
        match = re.compile(r'<h3 class="thumbnailReplay-title" itemprop="name"> <a href="(.*?)">(.*?)</a> </h3>',re.DOTALL).findall(html)
        
        if match:
          for link,title in match:
            list.append(item.Directory(title,param, link))
        else:         
          match = re.compile(r'<meta itemprop="name" content="(.*?)" />',re.DOTALL).findall(html) 
          if match:
            for title in match:
                list.append(item.Directory(title,param, link))
    if len(params)==4:
        html=utils.getWebContent('http://www.nrj-play.fr%s' % (params[3])).replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
        html=' '.join(html.split())    
          
        match = re.compile(r'<meta itemprop="contentUrl" content="(.*?)" alt="(.*?)"/>',re.DOTALL).findall(html)
        
        if match:
            for link,title in match:
                list.append(item.Video(link,title,1,'mp4'))
    
    return list
            