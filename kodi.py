# -*- coding: utf-8 -*-
import cmd
import os 
import urllib
import urlparse                

import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon


import resources.lib.utils as utils
import resources.lib.globalvar as globalvar


globalvar.TMP_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])   
args = urlparse.parse_qs(sys.argv[2][1:])


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def loadList(param):
    i=0
    list=utils.getList(param)
    
    for itm in list: 
        url2 = build_url({'mode': itm.mode, 'param': itm.url})
        li = xbmcgui.ListItem(
            itm.getDisplayTitle(),
            iconImage=itm.icon,
            thumbnailImage=itm.icon,
            path=itm.url) 
        if itm.mode == 'video':
            li.setInfo( type='Video', infoLabels={})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_NONE)
            xbmcplugin.setPluginCategory(addon_handle, 'episodes')
            xbmcplugin.setContent(addon_handle, 'episodes')
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url2,
            listitem=li,
            isFolder=itm.mode != 'video')
    
    xbmcplugin.endOfDirectory(addon_handle)
    
if args=={}:
    loadList(None)
else:
    if args['mode'][0]=='video':
        item = xbmcgui.ListItem(path=args['param'][0])
        xbmcplugin.setResolvedUrl(addon_handle, True, item)
        xbmcplugin.endOfDirectory(
          handle=int(addon_handle),
          succeeded=True,
          updateListing=False)
    else:
        loadList(args['param'][0])