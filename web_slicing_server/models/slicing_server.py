from odoo import _, api, models, fields


class SlicingServer(models.Model):
    _name = 'slicing.server'
    _description = 'SuperSlicer Server'

    ip = fields.Char(
        string='IP Address',
        required=True,
    )

    port = fields.Integer(
        string='Port',
        required=True,
    )

    name = fields.Char(
        string='Name',
        required=True,
    )
