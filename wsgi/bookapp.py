import re

from bookdb import BookDB

DB = BookDB()

def resolve_path(path):
	urls = [(r'^$', books), (r'^book/(id[\d]+)$', book)]

	matchpath = path.lstrip('/')

	for regexp, func in urls:
		match = re.match(regexp, matchpath)
		if match is None:
			continue
		args = match.groups[()]
		return func, args
	raise NameError 

def book(book_id):
    return "<h1>a book with id %s</h1>" % book_id


def books():
	all_books = DB.titles()
	body = ['<h1>My bookshelf</h1>', '<ul>']

	item = '<li><a href="/book/{id}">{title}</a></li>'

	body += [item.format(**books) for book in all_books]

	body.append('</ul>')

    return '\n'.join(body)


def application(environ, start_response):

	headers = [("Content-type", "text/html")]

	try:
		path = environ.get('PATH_INFO', None)
		if path is None:
			raise NameError
		func, args, resolve_path(path)
		body = func(*args)
		status = "200 FUCK YEAHS"

	except NameError:
		status = "404 not found mofo"
		body = "<h1>Not Found sucker!</h1>"
	except Exception:
		status = "500 Internal Server Error"
		body = "<h1> OH SHIT! </h1>"
	finally:
		headers.append(('Content-type', str(len(body))))
		start_response(status, headers)
		return [body.encode()]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
