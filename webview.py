import web
import urllib

import resources.lib.utils as utils

urls = (
	'/playVideo/(.*)' , 'video',
	'/(.*)', 'index'
)

app = web.application(urls, globals())

render = web.template.render('web/templates/')

class index:
	def GET(self,param):
		if param=="":
			param=None
		myList=utils.getList(param)
		return render.index(myList = myList)
		
class video(object):
        def GET(self,param):
        	url = urllib.unquote(param).decode('utf8')
        	return render.video(videoLink = url)
            
if __name__ == "__main__":
	app.run()