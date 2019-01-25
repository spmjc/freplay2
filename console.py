import cmd
import os

import resources.lib.utils
import resources.lib.globalvar
import resources.lib.process.m3u8download


resources.lib.globalvar.TMP_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

def loadList(param):
    i=0
    list=[]
    if param is None:
        list=resources.lib.utils.getChannelsList()
    else:
        list=resources.lib.utils.getListFromChannel(param)
    
    print "============================"
    for name, url, icon, infoLabels, mode in list:
        print "[" + str(i) + "] " + name + " (" + url + ")"
        i=i+1        
    
    print "[P] Parent Folder"
    print "[Q] Quit"
    text = raw_input("Enter choice: ")
    if text=="q" or text=="Q":
        quit()
    elif text=="p" or text=="P":
        loadList(param[:param.rfind('|')])
    else:
        item=int(text)
        param=list[item][1]
        print "Option Selected: " + param
        if list[item][4]=="video":
            if list[item][3]=="m3u8_mp4":
                file_path = os.path.join(resources.lib.globalvar.TMP_DIR, 'test.mp4')
                resources.lib.process.m3u8download.download_m3u8_ts_mp4(list[item][1],file_path,resources.lib.globalvar.TMP_DIR)
            elif list[item][3]=="mp4":
                print "soon"
        else:
            loadList(param)

loadList(None)

#resources.lib.utils.getChannelsList()
#loadList('arte|ACT|AJO|087505-000-A')
