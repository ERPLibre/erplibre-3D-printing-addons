from odoo import _, api, fields, models


class MainsailKlipper(models.Model):
    _name = "mainsail.klipper"
    _description = (
        "Model containing the HOST and PORT for the Mainsail instance"
    )

    name = fields.Char(
        string="Name",
        help="Instance Name",
        required=True,
        default="Mainsail - Klipper",
    )

    host = fields.Char(
        string="Host Address",
        help="The address (IP,Domain) of the Mainsail instance to embed",
        required=True,
        default="127.0.0.1",
    )

    port = fields.Char(
        string="Port",
        help="The listening port of the Mainsail instance to embed",
        required=True,
        default="80",
    )
