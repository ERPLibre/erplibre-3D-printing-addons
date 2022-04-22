from odoo import _, api, models, fields


class KlipperInstance(models.Model):
    _name = "klipper.klipper"
    _description = "Model containing the HOST and PORT for the Klipper instance (Moonraker)"

    name = fields.Char(
        string="Name",
        help="Instance Name",
        required=True,
        default="Klipper - Moonraker",
    )

    host = fields.Char(
        string="Host Address",
        help="The address (IP,Domain) of the Moonraker instance",
        required=True,
        default="127.0.0.1",
    )

    port = fields.Char(
        string="Port",
        help="The listening port of the Moonraker instance",
        required=True,
        default="7125",
    )

    ready = fields.Boolean(
        string="Printer ready",
        help="is the printer ready ?",
        default=False,
    )

    printing = fields.Boolean(
        string="Printer printing",
        help="Is the printer printing ?",
        default=False,
    )

    printer_state = fields.Char(
        string="Printer State",
        help="The state of the Klipper instance",
        default=""
    )
