from odoo import _, api, fields, models


class Extruder(models.Model):
    _name = "slicing.extruder"
    _description = "Extruder for this Slicing Profile"

    @api.model
    def _get_lift_top_selection(self):
        return [
            ("All surfaces", "All surfaces"),
            ("Not on top", "Not on top"),
            ("Only on top", "Only on top"),
        ]

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

    extruder_fan_offset = fields.Char(
        string="Extruder fan offset",
        help="",
        default="0%",
    )

    extruder_temperature_offset = fields.Integer(
        string="Extruder temperature offset",
        help="",
        default=0,
    )

    tool_name = fields.Char(
        string="Tool name",
        help="",
        default="",
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
        selection="_get_lift_top_selection",
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

    retract_restart_extra = fields.Integer(
        string="Retract restart extra",
        help=(
            "When the retraction is compensated after the travel move, the"
            " extruder will push this additional amount of filament. This"
            " setting is rarely needed. (mm, default: 0)"
        ),
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

    retract_length_toolchange = fields.Integer(
        string="Retract length toolchange",
        help=(
            "When retraction is triggered before changing tool, filament is"
            " pulled back by the specified amount (the length is measured on"
            " raw filament, before it enters the extruder). (mm (zero to"
            " disable), default: 10)"
        ),
        default=10,
    )

    retract_restart_extra_toolchange = fields.Integer(
        string="Retract restart extra toolchange",
        help=(
            "When the retraction is compensated after changing tool, the"
            " extruder will push this additional amount of filament. (mm,"
            " default: 0)"
        ),
        default=0,
    )

    extruder_colour = fields.Char(
        string="Extruder colour",
        help="",
        default="",
    )

    gcode_precision_e = fields.Integer(
        string="Gcode precision e",
        help="",
        default=5,
    )

    profile = fields.Many2one(
        comodel_name="slicing.profile",
        string="Profile",
        ondelete="cascade",
    )
