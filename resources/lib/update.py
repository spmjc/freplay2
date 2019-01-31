import base64
import urllib2
import json
import os

baseGithubURL='https://api.github.com/repos/spmjc/freplay2/contents'
baseLocalURL='/home/ubuntu/workspace/freplay/'

addFile=[]
updateFile=[]

def getGithubContent(file):
    url='https://raw.githubusercontent.com/spmjc/freplay2/master' + file
    req = urllib2.Request(url)
    response= urllib2.urlopen(req)
    return response.read()

def getFileContent(inputFile):
    openedFile = open(inputFile)
    return openedFile.read()

def compareDirGithubLocal(sGHDir,sLocDir):
    url='https://api.github.com/repos/spmjc/freplay2/contents' + '/' + sGHDir
    req = urllib2.Request(url)
    response= urllib2.urlopen(req)
    jsonParser     = json.loads(response.read()) 
    for i in range(len(jsonParser)):
        g=jsonParser[i]['name']
        locFile=os.path.join(sLocDir, g)
        if os.path.exists(locFile):
            if jsonParser[i]['type']=='file':
                if getFileContent(locFile)!=getGithubContent(sGHDir + '/' + g):
                    updateFile.append([sGHDir + '/' + g,locFile])
            else:
                compareDirGithubLocal(sGHDir + '/' + g, sLocDir + g + '/')
        else:
            addFile.append([sGHDir + '/' + g,locFile])

def getRateLimits():
    url='https://api.github.com/rate_limit'
    req = urllib2.Request(url)
    response= urllib2.urlopen(req)
    print response.read()

def update_file(file_path, content):
    file = open(file_path, 'w')
    file.write(content)
    file.close()

def run():
    getRateLimits()
    print'Generating list of files to update'
    compareDirGithubLocal('',baseLocalURL)
    print str(len(addFile)) + ' to create'
    print str(len(updateFile)) + ' to update'
    for i in addFile:
        update_file(i[1],getGithubContent(i[0]))
    for i in updateFile:
        update_file(i[1],getGithubContent(i[0]))
    print 'Done'

