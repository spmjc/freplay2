import cmd
import os

import resources.lib.utils
import resources.lib.globalvar


resources.lib.globalvar.TMP_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

def tester(param):
    list=[]
   
    
    if param is None:
        list=resources.lib.utils.getChannelsList()
    else:
         list=resources.lib.utils.getListFromChannel(param)
         if param.find('|')==-1:
            print 'Testing Channel: ' + param
         list=resources.lib.utils.getListFromChannel(param)
    
    try:
        for name, url, icon, infoLabels, mode in list:
            if mode=="video":
                videoLinks= resources.lib.utils.getVideoURL(url)
            else:
                tester(url)
    except Exception, e:
        print 'Error with this link: ' + url + ' ' + str(e)

tester(None)
    