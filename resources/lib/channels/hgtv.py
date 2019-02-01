# -*- coding: utf-8 -*-
import json
import re

import resources.lib.utils as utils
import resources.lib.item as item
import resources.lib.globalvar as globalvar
import resources.lib.m3u8 as m3u8

title = ['HGTV']
img = ['hgtv']
readyForUse = True

listShow='https://www.hgtv.com/shows/shows-a-z'

formats=[
    [6,'720x1280'],
    [5,'540x960'],
    [4,'480x854'],
    [3,'320x568'],
    [2,'270x480'],
    [1,'224x400'],
    ]

def getList(param):
    list = []
    params=param.split("|")
    channel=utils.getChannel(param)
    uniqueItem = dict()
    
    if len(params)==1:
        html=utils.getWebContentSave(listShow,'catalog_%s.html' % channel).replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
        html=' '.join(html.split())
        match = re.compile(r'<li class="m-PromoList__a-ListItem"><a href="(.*?)">(.*?)</a></li>',re.DOTALL).findall(html)
        if match:
            for link,title in match:
                if 'target' not in link and 'Connect With HGTV Talent' not in title:
                    list.append(item.Directory(title,param, 'https:' + link))
    if len(params)==2:
        html=utils.getWebContent(params[1] + '/videos').replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
        html=' '.join(html.split())
        match = re.compile(r'<div class="m-MediaBlock"> <div class="m-MediaBlock__m-MediaWrap" data-type="video-launcher" data-video-no="(.*?)"> <a href="(.*?)"> <img (.*?) src="(.*?)" (.*?)<span class="m-MediaBlock__a-HeadlineText">(.*?)</span> <span class="m-MediaBlock__a-AssetInfo">(.*?)</span>',re.DOTALL).findall(html)
        if match:
            for empty,link,empty2,img,empty3,title,duration in match:
                id=link[-(len(link)-link.rfind('-')-1):]
                list.append(item.Directory(title,param, id, 'https:' + img))
    if len(params)==3:
        for format in formats:
            url='http://sniidevices-a.akamaihd.net/%s/%s_%s.mp4' % (params[2][:4],params[2],format[0])
            if utils.url_exists(url):
                list.append(item.Video(url,format[1],format[0],'mp4'))
    return list