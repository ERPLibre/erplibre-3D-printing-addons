import fnmatch
import secrets
import string
from abc import ABC
from os import scandir
from os.path import join

import orjson
from tornado.process import Subprocess

from server.base import BaseHandler
from server.websocket import ServerSocketHandler


def get_random_string(length) -> str:
    # choose from all lowercase letter and digits
    characters = string.ascii_letters + string.digits
    result_str = ''.join(secrets.choice(characters) for i in range(length))
    return result_str


class ServerInfosHandler(BaseHandler, ABC):
    """Handler for infos on the SuperSlicer Server"""

    def get(self):
        """ Infos on the server """
        payload = orjson.dumps({
            'name': 'SuperSlicer Server',
            'description': 'API Web Server for SuperSlicer',
            'version': '1.0.0',
            'author': 'Normil Jose',
            'website': '',
            'repos': 'github'
        })
        self.write(payload)


class SuperSlicerHandler(BaseHandler, ABC):
    """ Handler for `/slice` route """

    async def get(self, filename):
        """
        Slicing status for `filename` (stl).
        Check the slicing progression.
        `filename` (g-code) created ==> slicing finished.

        The sliceStatus(filename) on the website keeps calling this function.
        """
        if self.gcode_exist(filename):
            message = orjson.dumps({'message': f'The slicing of {filename} has finished'})
            self.write(message)
            return
        else:
            message = orjson.dumps({'message': 'The slicing is in progress or there was an error'})
            self.write(message)
            return

    async def post(self):
        """
        Send an STL file to SuperSlicer with the slicing profile parameters.
        The website upload at least 2 files to this function. The last one is a JSON with the
        slicing profile data.
        """

        profile_data = None
        filenames = []
        for field_name, files in self.request.files.items():
            for info in files:
                filename = info["filename"]
                body = info["body"]
                if fnmatch.fnmatch(filename, '*.stl'):
                    stl_file = open(join(self.stl_folder, filename), "wb")
                    stl_file.write(body)
                    stl_file.close()
                    filenames.append(filename)
                elif fnmatch.fnmatch(filename, '*.obj'):
                    stl_file = open(join(self.obj_folder, filename), "wb")
                    stl_file.write(body)
                    stl_file.close()
                    filenames.append(filename)
                elif fnmatch.fnmatch(filename, '*.amf'):
                    stl_file = open(join(self.amf_folder, filename), "wb")
                    stl_file.write(body)
                    stl_file.close()
                    filenames.append(filename)
                elif fnmatch.fnmatch(filename, '*.json'):  # always upload json profile data
                    profile_data = orjson.loads(body)

        # STL Files uploaded, start slicing
        if len(filenames):
            # Send the first STL file to the command processor
            await self.start_slicing_command(filenames[0], profile_data)
            payload = orjson.dumps({
                'message': 'File uploaded successfully. Check the result in the viewer.',
                'file': filenames[0]
            })
        else:
            payload = orjson.dumps({
                'message': 'No file uploaded',
                'files': filenames
            })
        self.write(payload)

    def gcode_exist(self, filename) -> bool:
        file_existed = False
        gcodes_files = scandir(self.gcode_folder)
        with gcodes_files:
            for entry in gcodes_files:
                file_existed = entry.name == filename + '.gcode' and entry.is_file()
        return file_existed
