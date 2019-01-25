import web

import resources.lib.utils

urls = (
	'/', 'index'
)

app = web.application(urls, globals())

render = web.template.render('web/templates/')

class index:
	def GET(self):
	    myList=resources.lib.utils.getChannelsList()
	    return render.index(myList = myList)

if __name__ == "__main__":
	app.run()