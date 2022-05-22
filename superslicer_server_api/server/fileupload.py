from typing import Optional, Awaitable

from tornado.web import RequestHandler, stream_request_body


@stream_request_body
class FileUploadHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info["filename"], info['content_type']
                body = info["body"]
