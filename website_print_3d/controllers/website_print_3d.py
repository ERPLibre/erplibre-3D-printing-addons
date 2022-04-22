import math
from os.path import splitext, join

import orjson
import logging
import os

import requests as requests

from ..gcode_analyser.gcode_analyzer import Analyzer
from odoo.http import Controller, route, request

_logger = logging.getLogger(__name__)
MODULE_PATH = os.path.join(os.path.dirname(__file__), '..')


class P3DController(Controller):

    @route('/slice-model', auth='public', website=True)
    def slicemodel(self, **kwargs):
        if kwargs.get('model_file', False):
            filename = kwargs.get('model_file').filename

            file = kwargs.get('model_file').read()
            profile_id = kwargs.get('p3d_profile_id')
            Profile = request.env['slicing.profile']
            # SaleOrder = request.env['sale.order']
            # sale_order = SaleOrder.search([('id', '=', kwargs.get('website_sale_id'))], limit=1)
            SuperSlicerServer = request.env['slicing.server']
            actual_server = SuperSlicerServer.search([('default_server', '=', True)], limit=1)
            actual_server_url = f"http://{actual_server.address}:{actual_server.port}/slice"

            profile_sale = Profile.search([('id', '=', profile_id)], limit=1)
            profile_json = orjson.dumps(profile_sale._datadict())

            # websocket here ??
            # send file and connect to channel
            post_files = {
                f'{filename}': file,
                'profile.json': profile_json,
            }
            response = requests.post(actual_server_url, files=post_files)
            # superslicer server send each line with a finish message or close the connection
            # get the gcode to analyze
            gcode_filename = splitext(filename)[0] + '.gcode'
            gcode_url = f"http://{actual_server.address}:{actual_server.port}/files/gcode/{gcode_filename}"
            gcode_response = requests.get(gcode_url)
            with open(join(MODULE_PATH, gcode_filename), "wb") as fp:
                fp.write(gcode_response.content)
            # # analyze the file
            # analyzer = Analyzer(join(MODULE_PATH, gcode_filename))
            # print_time = analyzer.get_formatted_time()
            # filament_usage = analyzer.get_filament_usage() / float(10.0)  # in cm
            # # Calculate filament quantity
            # density = profile_sale.filament_density  # in g/cm3
            # diameter = profile_sale.filament_diameter / float(10.0)  # in cm
            # volume = math.pi * (float(diameter)**2) * filament_usage / float(4.0)  # in cm3
            # mass = volume * density / float(1000.0)  # in kg
            # _logger.info(mass)

            # # Update the order
            # order_lines = sale_order.order_line
            # for line in order_lines:
            #     _logger.info(line.product_id.name)
            #     line.write({'product_uom_qty': mass})
            return response.text
        return "No File Uploaded"
