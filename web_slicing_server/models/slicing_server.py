from odoo import _, api, models, fields


class SlicingServer(models.Model):
    _name = 'slicing.server'
    _description = 'SuperSlicer Server'
    _sql_constraints = [('unique_ss_server', 'UNIQUE(name,address,port)',
                         'The SuperSlicer Server infos should be unique!')]

    address = fields.Char(
        string="IP Address",
        help="SuperSlicer Server Address [domain name ; ip]",
        required=True,
        default="localhost",
        index=True,
    )

    port = fields.Integer(
        string='Port',
        help="Listening port of the SuperSlicer Server",
        required=True,
        default=5000,
        index=True,
    )

    name = fields.Char(
        string="Name",
        required=True,
        default="SuperSlicer Server",
        index=True,
    )

    default_server = fields.Boolean(
        string="Default server?",
        help="Use as the default SuperSlicer Server",
        default=False,
        index=True,
    )

    @api.onchange('default_server')
    def _onchange_default_server(self):
        if self.default_server:
            result = self.search([('default_server', '=', True)], limit=1)
            result.write({'default_server': False})
        else:
            result = self.search([('default_server', '=', False)], order='id', limit=1)
            result.write({'default_server': True})
