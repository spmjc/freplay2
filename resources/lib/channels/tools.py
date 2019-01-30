# -*- coding: utf-8 -*-
import resources.lib.utils as utils
import resources.lib.update as update
import resources.lib.item as item

title=['Tools']
img=['tools']
readyForUse=True

def getList(param):
    list=[]
    params=param.split("|")
    channel=utils.getChannel(param)
    
    if len(params)==1:
        list.append(item.Directory('Clean cache',param,'clean'))
        list.append(item.Directory('Check for updates',param,'update'))
    if len(params)==2:
        if params[1]=='clean':
            utils.empty_TMP()
        elif params[1]=='update':
            update.run()
        list=getList(params[0])

    return list