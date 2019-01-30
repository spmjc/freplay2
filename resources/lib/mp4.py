import requests

def downloadfile(url,name):
    with open(name, 'w') as f:
        data = requests.get(url, stream=True)
        for chunk in data.iter_content(chunk_size=512):
			if chunk:
				f.write(chunk)
    f.close()