from odoo import _, api, models, fields


class SlicingProfile(models.Model):
    _name = "slicing.profile"
    _description = "Slicing Profile"

    name = fields.Char(
        string="Name",
        required=True,
    )

    ##########################################
    # LAYERS AND PERIMETERS
    ##########################################

    perimeters = fields.Integer(
        string="Perimeters",
        default=2,
        required=True,
    )

    top_solid_layers = fields.Integer(
        string="Top Solid Layers",
    )

    bottom_solid_layers = fields.Integer(
        string="Bottom Solid Layers"
    )

    top_solid_min_thickness = fields.Integer(
        string="Top Solid Min Thickness",
    )

    bottom_solid_min_thickness = fields.Integer(
        string="Bottom Solid Min Thickness",
    )

    one_perimeter_top = fields.Boolean(
        string="Only One Perimeter Top ?",
    )

    min_width_top_surface = fields.Float(
        string="Min Width Top Surface (%)",
        default=200,
    )

    extra_perimeters_overhangs = fields.Boolean(
        string="Extra Perimeters Overhangs",
        default=False,
    )

    extra_perimeters_odd_layers = fields.Boolean(
        string="Extra Perimeters Odd Layers",
        default=False,
    )

    ############################################
    # SLICING
    ############################################

    layer_height = fields.Float(
        string="Layer Height",
        required=True,
    )

    first_layer_height = fields.Float(
        string="First Layer Height (%)",
        default=30.0,
        required=True,
    )

    resolution = fields.Float(
        string="Resolution (mm)",
        default=0.002,
        digits=(1, 3),
    )

    model_precision = fields.Float(
        string="Model Precision (mm)",
        default=0.0001,
        digits=(1, 4),
    )

    slice_closing_radius = fields.Float(
        string="Slice Closing Radius (mm)",
        default=0.049,
        digits=(1, 3),
    )

    remarks = fields.Html(
        string="Remarks",
        required=False,
    )
