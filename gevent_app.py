from main import app
import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_socket()
http_server = WSGIServer(('0.0.0.0', 8090), app)
http_server.serve_forever()