from odoo import _, api, models, fields


class Extruder(models.Model):
    _name = "slicing.extruder"
    _description = "Extruder for this Slicing Profile"

    @api.model
    def _get_lift_top_selection(self):
        return [("All surfaces", "All surfaces"),
                ("Not on top", "Not on top"),
                ("Only on top", "Only on top")]

    nozzle_diameter = fields.Float(
        string="Nozzle diameter",
        help="",
        default=0.4,
        digits=(1, 2),
    )

    min_layer_height = fields.Float(
        string="Min layer height",
        help="",
        default=0.07,
        digits=(1, 2),
    )

    max_layer_height = fields.Float(
        string="Max layer height",
        help="",
        default=0,
        digits=(1, 2),
    )

    extruder_offset = fields.Char(
        string="Extruder offset (X*Y)",
        help="",
        default="0x0",
    )

    retract_length = fields.Integer(
        string="Retract length",
        help="",
        default=2,
    )

    retract_lift = fields.Integer(
        string="Retract lift (Z)",
        help="",
        default=0,
    )

    retract_lift_above = fields.Integer(
        string="Retract lift above Z",
        help="",
        default=0,
    )

    retract_lift_below = fields.Integer(
        string="Retract lift below Z",
        help="",
        default=0,
    )

    retract_lift_first_layer = fields.Boolean(
        string="Retract lift first layer",
        help="",
        default=False,
    )

    retract_lift_top = fields.Selection(
        selection='_get_lift_top_selection',
        string="Retract lift top",
        help="",
        default="All surfaces",
    )

    retract_speed = fields.Integer(
        string="Retract speed",
        help="",
        default=40,
    )

    deretract_speed = fields.Integer(
        string="Deretract speed",
        help="",
        default=0,
    )

    retract_before_travel = fields.Integer(
        string="Retract before travel",
        help="",
        default=2,
    )

    retract_layer_change = fields.Boolean(
        string="Retract layer change",
        help="",
        default=False,
    )

    wipe = fields.Boolean(
        string="Wipe",
        help="",
        default=False,
    )

    retract_before_wipe = fields.Char(
        string="Retract before wipe",
        help="",
        default="0%",
    )

    wipe_extra_perimeter = fields.Integer(
        string="Wipe extra perimeter",
        help="",
        default=0,
    )

    extruder_colour = fields.Char(
        string="Extruder colour",
        help="",
        default="",
    )

    profile = fields.Many2one(
        comodel_name="slicing.profile",
        string="Profile",
        ondelete="cascade",
    )
