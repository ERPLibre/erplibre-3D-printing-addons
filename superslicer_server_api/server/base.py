import configparser
import subprocess
from abc import ABC
from os.path import dirname, abspath, join, basename, splitext

import orjson
from tornado.process import Subprocess
from tornado.web import RequestHandler

from server.websocket import ServerSocketHandler

ROOT_FOLDER = dirname(dirname(abspath(__file__)))
FILES_FOLDER = join(ROOT_FOLDER, 'files')
STL_FOLDER = join(FILES_FOLDER, 'stls')
GCODE_FOLDER = join(FILES_FOLDER, 'gcodes')
OBJ_FOLDER = join(FILES_FOLDER, 'objs')
AMF_FOLDER = join(FILES_FOLDER, 'amfs')
CONFIG_FOLDER = join(FILES_FOLDER, 'configs_tmp')

STREAM = Subprocess.STREAM
STDOUT = subprocess.STDOUT
PIPE = subprocess.PIPE
global tmp_base_name


class BaseHandler(RequestHandler, ABC):
    """
    BaseHandler to prepare the request and the response.
    Serves also for sending commands to SuperSlicer
    """

    def initialize(self, folder=None, has_redis=None) -> None:
        self.folder = folder
        self.process = None
        self.stl_folder = STL_FOLDER
        self.gcode_folder = GCODE_FOLDER
        self.obj_folder = OBJ_FOLDER
        self.amf_folder = AMF_FOLDER
        self.websocket = None
        if has_redis:
            self.socket = ServerSocketHandler(self.application, self.request)
        else:
            self.socket = None

    def prepare(self):
        pass  # self.args = json_decode(self.request.body)

    def options(self, file):
        print(file)
        self.set_status(200, "ok")

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with, X-Api-Key, Content-Type')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEADER')

    async def start_slicing_command(self, file, profile):
        global tmp_base_name
        cmd_list = ['/usr/local/bin/superslicer', '--gcode']
        filename = join(STL_FOLDER, file)
        # print(filename)
        cmd_list.append(filename)
        # print(filename)
        cmd_list.append('--output')

        tmp_base_name = output_filename = splitext(basename(filename))[0]
        output_filename += '.gcode'
        out_filename = join(GCODE_FOLDER, output_filename)
        # print(out_filename)
        cmd_list.append(out_filename)

        # self.add_profile_data_to_command(profile)
        config_filename = tmp_base_name + '.ini'
        config_file = join(CONFIG_FOLDER, config_filename)
        self.save_profile_data_to_file(profile, config_file)
        cmd_list.append('--load')
        cmd_list.append(config_file)

        # self.process = Subprocess(cmd_list, stdin=STREAM, stdout=PIPE, stderr=STDOUT)
        # print(str(cmd_list))
        proc = subprocess.Popen(cmd_list, stdout=PIPE)
        line = proc.stdout.readline()
        while line:
            print(str(line.decode().strip()))
            if self.websocket:
                self.websocket.publish_message(str(line.decode().strip()))
            line = proc.stdout.readline()

    def exit_callback(self, returncode):
        result = self.process.stdout.read_until_close().result().decode()
        print(returncode)
        print(result)

    # def add_profile_data_to_command(self, profile):  # profile is JSON
    #     count = 0
    #     for (ke, val) in profile.items():
    #         parameter = str(ke).replace('_', '-')
    #         # count += 1
    #         # if count == 50:
    #         #     break
    #         if isinstance(val, bool) and val is True:
    #             cmd_list.append(f'--{parameter}')
    #         elif isinstance(val, dict):
    #             res = {}
    #             for (k, v) in val.items():
    #                 for (ket, vl) in v.items():
    #                     parameter = str(ket).replace('_', '-')
    #                     if parameter in res:
    #                         if isinstance(vl, bool):
    #                             res[f'{parameter}'] += ',' + str(int(vl))
    #                         else:
    #                             res[f'{parameter}'] += ',' + str(vl)
    #                     else:
    #                         if isinstance(vl, bool):
    #                             res[f'{parameter}'] = str(int(vl))
    #                         else:
    #                             res[f'{parameter}'] = str(vl)
    #             for (k, v) in res.items():
    #                 cmd_list.append(f'--{k}')
    #                 cmd_list.append(f'{v}')
    #         elif not isinstance(val, bool):
    #             if isinstance(val, str) and len(val):
    #                 cmd_list.append(f'--{parameter}')
    #                 cmd_list.append(f'{val}')
    #             elif not isinstance(val, str):
    #                 cmd_list.append(f'--{parameter}')
    #                 cmd_list.append(f'{val}')

    def save_profile_data_to_file(self, profile, file):
        """
        Save the profile data to an INI file to facilitate the command to SuperSlicer
        @param profile: JSON data of the chosen profile
        @param file: str filename based on the 3D model file uploaded
        @return: None
        """
        config_data = configparser.ConfigParser(allow_no_value=True, delimiters='=', interpolation=None)
        config_data['Settings'] = {}
        data = config_data['Settings']
        for (ke, val) in profile.items():
            parameter = str(ke)  # .replace('_', '-')
            # count += 1
            # if count == 50:
            #     break
            if isinstance(val, bool):
                data[f'{parameter}'] = str(int(val))
                # cmd_list.append(f'--{parameter}')
            elif isinstance(val, dict):
                res = {}
                for (k, v) in val.items():
                    for (ket, vl) in v.items():
                        parameter = str(ket)  # .replace('_', '-')
                        if parameter in res:
                            if isinstance(vl, bool):
                                res[f'{parameter}'] += ',' + str(int(vl))
                            else:
                                res[f'{parameter}'] += ',' + str(vl)
                        else:
                            if isinstance(vl, bool):
                                res[f'{parameter}'] = str(int(vl))
                            else:
                                res[f'{parameter}'] = str(vl)
                for (k, v) in res.items():
                    data[f'{k}'] = v
                    # cmd_list.append(f'--{k}')
                    # cmd_list.append(f'{v}')
            elif not isinstance(val, bool):
                if isinstance(val, str):
                    if 'gcode' not in parameter:
                        data[f'{parameter}'] = str(val)
                    # else:
                    #     data[f'{parameter}'] = str(val)
                    # cmd_list.append(f'--{parameter}')
                    # cmd_list.append(f'{val}')
                elif not isinstance(val, str):
                    data[f'{parameter}'] = str(val)
                    # cmd_list.append(f'--{parameter}')
                    # cmd_list.append(f'{val}')
        with open(file, 'w') as configfile:
            config_data.write(configfile, space_around_delimiters=True)
