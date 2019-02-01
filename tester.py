# -*- coding: utf-8 -*-
import cmd
import os
import json
import time

import resources.lib.utils as utils
import resources.lib.globalvar as globalvar
import resources.lib.item as item


globalvar.TMP_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

testResult={}

def saveTestResult():
    file_path = os.path.join(globalvar.TMP_DIR, 'testResult.json')
    file = open(file_path, 'w')
    file.write(json.dumps(testResult, sort_keys=False,indent=4))
    file.close()
    
def start():
    testResult['start']=round(time.time(),0)
    
def end():
    testResult['end']=round(time.time(),0)
    testResult['duration']=testResult['end']-testResult['start']  
    saveTestResult()
    print 'Testing complete'
    
def addVideo(chan):
    if chan not in testResult:
        testResult[chan]={}
        
    if 'videos' not in testResult[chan]:
        testResult[chan]['videos']=0
        
    testResult[chan]['videos']+=1
    
def addSuccess(param):
    params=param.split('|')
    chan=params[0]
    
    if chan not in testResult:
        testResult[chan]={}
        
    if 'links' not in testResult[chan]:
        testResult[chan]['links']=0
        
    testResult[chan]['links']+=1
    
def addError(param,error):
    params=param.split('|')
    chan=params[0]
    
    if chan not in testResult:
        testResult[chan]={}
    
    if error not in testResult[chan]:
        testResult[chan][error]=[]
        
    testResult[chan][error].append(param)
        

def tester(param):
    list=[]
   
    if param != None:
        print 'Testing: ' + param
    
    try:
        url=''
        list=utils.getList(param)  
        if len(list)==0:
            addError(param,'No item in list')
        for itm in list:
            if itm.mode!="video":
                addSuccess(itm.url)
                if(itm.name!='<< Page Precedente' and param!='tools+tools'):
                    tester(itm.url)
            else:
                addVideo(param.split('|')[0])
    except Exception, e:
        if url=='':
            addError(param,str(e))
        else:
            addError(url,str(e))

start()

tester('thecw+thecw')
#tester(None)
utils.empty_TMP()
end()

#https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    