# -*- coding:utf-8 -*-
import sys
import os
import requests
import resources.lib.utils
import urllib2
from urlparse import urlparse


cwd = os.getcwd()


def download_ts(path, url_list):
	ts_files = []
	i=0
	for url in url_list:
		print 'Downloading chunk' + str(i) + '/' + str(len(url_list))
		i+=1
		ts_name = url.split("/")[-1:]
		ts_file = os.path.join(path, ts_name[0])
		if os.path.exists(ts_file):
			ts_files.append(ts_file)
			continue
		with open(ts_file, 'w') as f:
			data = requests.get(url, stream=True)
			for chunk in data.iter_content(chunk_size=512):
				if chunk:
					f.write(chunk)
		ts_files.append(ts_file)
	return ts_files

def get_list_m3u8_ts(url):
    req = urllib2.Request(url)
    req.add_header(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
    req.add_header('Referer', url)
    response= urllib2.urlopen(req)
    parsed_uri = urlparse(response.geturl())
    base_URL='{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri)
    base_URL=base_URL[:base_URL.rfind('/')]
    
    list=[]
    webcontent = response.read()
    a=webcontent.splitlines()
    for line in a:
        if line.endswith(".ts"):
            list.append(base_URL + '/' + line)
    return list
    
def download_m3u8_ts_mp4(m3u8_file,mp4_path, tmp_path):
    
	ts_list = get_list_m3u8_ts(m3u8_file)
	ts_file_list = download_ts(tmp_path, ts_list)
	
	with open(mp4_path, 'wa+') as f:
	    for ts_file in ts_file_list:
	        with open(ts_file) as ts:
	            f.write(ts.read())
            
	for ts_file in ts_file_list:
		os.remove(ts_file)