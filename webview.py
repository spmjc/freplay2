import web

import resources.lib.utils as utils

urls = (
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

if __name__ == "__main__":
	app.run()