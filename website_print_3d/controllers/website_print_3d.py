import logging
import os

from odoo.http import Controller, route, request

_logger = logging.getLogger(__name__)
MODULE_PATH = os.path.join(os.path.dirname(__file__), '..')


class P3DController(Controller):

    @route('/slice-model', auth='public', website=True)
    def slicemodel(self, **kwargs):
        _logger.info('Request Model upload received')
        _logger.info(kwargs.items())
        if kwargs.get('model_file', False):
            filename = kwargs.get('model_file').filename
            _logger.info('Request Model File uploaded : ' + filename)
            file = kwargs.get('model_file').read()
            sale_order = request.env['sale.order']
            # websocket here
            # send file and connect to channel
            # superslicer server send each line with a finish message or close the connection
            # && return the gcode
            # pass the gcode to pgviewer
            return f"Filename : {filename}. File size :."
        return "Hello"
