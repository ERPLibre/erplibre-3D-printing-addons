from tornado.ioloop import IOLoop
from tornado.web import Application

from server.filerequest import FileRequestHandler
from server.handler import SuperSlicerHandler, ServerInfosHandler
from server.websocket import ServerSocketHandler

PORT = 5000
ADDRESS = ''


def make_app():
    urls = [(r'/', ServerInfosHandler),
            (r'/slice', SuperSlicerHandler, {'has_redis': 'True'}),
            (r'/files/stl/(.*)', FileRequestHandler, {'folder': 'stls'}),
            (r'/files/obj/(.*)', FileRequestHandler, {'folder': 'objs'}),
            (r'/files/amf/(.*)', FileRequestHandler, {'folder': 'amfs'}),
            (r'/files/gcode/(.*)', FileRequestHandler, {'folder': 'gcodes'}),
            (r'/slicing/status/(.*)', ServerSocketHandler)
            ]
    return Application(urls)


if __name__ == '__main__':
    try:
        print(f'Starting application on {ADDRESS if ADDRESS else "*"}:{PORT}')
        app = make_app()
        app.listen(PORT, ADDRESS)
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print('\nStopping application')
