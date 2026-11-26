import gunicorn
from gunicorn.http import wsgi

gunicorn.SERVER_SOFTWARE = 'WebServer'

timeout = 120

threads = 2


class Response(wsgi.Response):
    def default_headers(self, *args, **kwargs):
        headers = super(Response, self).default_headers(*args, **kwargs)
        return [h for h in headers if not h.startswith('Server:')]


wsgi.Response = Response
