# -*- coding: utf-8 -*-
import cmd
import os

import resources.lib.utils as utils
import resources.lib.item as item
import resources.lib.globalvar as globalvar
import resources.lib.m3u8 as m3u8
import resources.lib.mp4 as mp4


globalvar.TMP_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

def loadList(param):
    i=0
    list=utils.getList(param)
    
    print "============================"
    
    for itm in list:
        print "[" + str(i) + "] " + itm.getDisplayTitle() + " (" + itm.url + ")" 
        i+=1
    print "[P] Parent Folder"
    print "[Q] Quit"
    text = raw_input("Enter choice: ")
    
    if text=="q" or text=="Q":
        quit()
    elif text=="p" or text=="P":
        if param.rfind('|')==-1:
            loadList(None)
        else:
            loadList(param[:param.rfind('|')])
    else:
        itemSelected=int(text)
        param=list[itemSelected].url
        print "Option Selected: " + param
        if list[itemSelected].mode=="video":
            if list[itemSelected].fileType=="m3u8_mp4":
                file_path = os.path.join(globalvar.TMP_DIR, list[itemSelected][3][0])
                m3u8.download_m3u8_ts_mp4(list[itemSelected][1],file_path,globalvar.TMP_DIR)
            elif list[itemSelected].fileType=="mp4":
                file_path = os.path.join(globalvar.TMP_DIR, list[itemSelected].name)
                mp4.downloadfile(list[itemSelected].url,file_path)
        else:
            loadList(param)

lloadList(None)
#loadList('thecw+thecw|more-video|1|80fb61c2-5425-4f8c-9e83-af951df318c8')