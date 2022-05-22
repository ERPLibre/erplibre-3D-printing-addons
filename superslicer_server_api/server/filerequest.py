import os
from abc import ABC
from os import scandir
from os.path import dirname, join, abspath

import orjson
from tornado.web import RequestHandler, stream_request_body

from server.base import BaseHandler


# ROOT_FOLDER = dirname(dirname(abspath(__file__)))
# FILES_FOLDER = join(ROOT_FOLDER, "files")
# STL_FOLDER = join(FILES_FOLDER, "stls")
# GCODE_FOLDER = join(FILES_FOLDER, "gcodes")
# OBJ_FOLDER = join(FILES_FOLDER, "objs")


# @stream_request_body
# class FileUploadHandler(RequestHandler):
#     """Files Request Handler for PUT"""
#
#     def initialize(self):
#         self.bytes_read = 0
#
#     def data_received(self, chunk: bytes):
#         self.bytes_read += len(chunk)
#
#     def put(self):
#         for field_name, files in self.request.files.items():
#             for info in files:
#                 filename, content_type = info["filename"], info['content_type']
#                 body = info["body"]
#                 stl_file = open(STL_FOLDER + filename, "wb")
#                 stl_file.write(body)
#                 stl_file.close()


class FileRequestHandler(BaseHandler, ABC):
    """Usual Files Handler (POST, GET, DELETE)"""

    def delete(self, filename):
        file_existed = False
        if self.folder == 'stls':
            stl_files = scandir(self.stl_folder)
            with stl_files:
                for entry in stl_files:
                    file_existed = entry.name == filename and entry.is_file()
                    if file_existed:
                        os.remove(join(self.stl_folder, filename))
                        break

        elif self.folder == 'gcodes':
            gcodes_files = scandir(self.gcode_folder)
            with gcodes_files:
                for entry in gcodes_files:
                    file_existed = entry.name == filename and entry.is_file()
                    if file_existed:
                        os.remove(join(self.gcode_folder, filename))
                        break

        if file_existed:
            payload = orjson.dumps({'message': f'File {filename} deleted successfully'})
            self.write(payload)
        else:
            payload = orjson.dumps({'message': 'The file specified does not exist'})
            self.write(payload)

    def post(self):
        for field_name, files in self.request.files.items():
            for info in files:
                filename = info["filename"]
                body = info["body"]
                stl_file = open(self.stl_folder + filename, "wb")
                stl_file.write(body)
                stl_file.close()
                payload = orjson.dumps({'message': f'File {filename} uploaded'})
                self.write(payload)

    def get(self, filename):
        """
        Download {filename} contained in `folder`
        Or return the number of files in `folder`
        """
        files = []
        if self.folder == "stls":
            stl_files = scandir(self.stl_folder)
            with stl_files:
                for file in stl_files:
                    if filename and file.name == filename:
                        self.set_header('Content-Type', 'application/octet-stream')
                        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
                        file_to_send = open(join(self.stl_folder, file.name), "rb")
                        data = file_to_send.read()
                        file_to_send.close()
                        self.write(data)
                        self.finish()
                        return
                    files.append(file.name)
        elif self.folder == "gcodes":
            gcode_files = scandir(self.gcode_folder)
            with gcode_files:
                for file in gcode_files:
                    if filename and file.name == filename:
                        self.set_header('Content-Type', 'application/octet-stream')
                        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
                        file_to_send = open(join(self.gcode_folder, file.name), "rb")
                        data = file_to_send.read()
                        file_to_send.close()
                        self.write(data)
                        self.finish()
                        return
                    files.append(file.name)
        elif self.folder == "amfs":
            amf_files = scandir(self.amf_folder)
            with amf_files:
                for file in amf_files:
                    if filename and file.name == filename:
                        self.set_header('Content-Type', 'application/octet-stream')
                        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
                        file_to_send = open(join(self.amf_folder, file.name), "rb")
                        data = file_to_send.read()
                        file_to_send.close()
                        self.write(data)
                        self.finish()
                        return
                    files.append(file.name)
        elif self.folder == "objs":
            gcode_files = scandir(self.obj_folder)
            with gcode_files:
                for file in gcode_files:
                    if filename and file.name == filename:
                        self.set_header('Content-Type', 'application/octet-stream')
                        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
                        file_to_send = open(join(self.obj_folder, file.name), "rb")
                        data = file_to_send.read()
                        file_to_send.close()
                        self.write(data)
                        self.finish()
                        return
                    files.append(file.name)

        if filename:
            payload = orjson.dumps({'error': f'{filename} not found'})
        else:
            payload = orjson.dumps({'message': f'{len(files)} files found',
                                    'files': files})
        self.write(payload)
