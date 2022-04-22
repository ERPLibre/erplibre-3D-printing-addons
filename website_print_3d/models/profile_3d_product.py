from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Profile3DProduct(models.Model):
    # _name = "p3d.product"
    _inherit = "product.template"
    # _description = "Slicing Profile as 3D Product"
    # _sql_constraints = [('unique_name', 'UNIQUE(name)', 'The profile name should be unique.!')]

    profile = fields.Many2one(
        comodel_name="slicing.profile",
        string="Profile",
        default=lambda self: self.env["slicing.profile"],
        required=True,
    )
