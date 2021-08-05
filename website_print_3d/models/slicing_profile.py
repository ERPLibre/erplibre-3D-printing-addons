from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class SlicingProfile(models.Model):
    _name = "slicing.profile"
    _description = "Slicing Profile Settings"
    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'The profile name should be unique!')]

    @api.model
    def _get_algo_selection(self):
        return [("none", "Disabled"),
                ("noperi", "Remove perimeters"),
                ("bridges", "Keep only bridges"),
                ("bridgesoverhangs", "Keep bridges and overhangs"),
                ("filled", "Fill the voids with bridges")]

    @api.model
    def _get_seam_selection(self):
        return [("hidden", "Cost-based"),
                ("random", "Random"),
                ("aligned", "Aligned"),
                ("rear", "Rear")]

    @api.model
    def _get_fill_pattern_selection(self):
        return [("rectilinear", "Rectilinear"),
                ("monotonic", "Monotonic"),
                ("grid", "Grid"),
                ("triangles", "Triangles"),
                ("stars", "Stars"),
                ("cubic", "Cubic"),
                ("line", "Line"),
                ("concentric", "Concentric"),
                ("honeycomb", "Honeycomb"),
                ("3dhoneycomb", "3D Honeycomb"),
                ("gyroid", "Gyroid"),
                ("hilbertcurve", "Hilbert Curve"),
                ("archimedeanchords", "Archimedean Chords"),
                ("octagramspiral", "Octagram Spiral"),
                ("scatteredrectilinear", "Scattered Rectilinear"),
                ("adaptivecubic", "Adaptive Cubic"),
                ("supportcubic", "Support Cubic")]

    @api.model
    def _get_fill_density_selection(self):
        return [("0%", "0 %"),
                ("4%", "4 %"),
                ("5.5%", "5.5 %"),
                ("7.5%", "7.5 %"),
                ("10%", "10 %"),
                ("13%", "13 %"),
                ("18%", "18 %"),
                ("23%", "23 %"),
                ("31%", "31 %"),
                ("42%", "42 %"),
                ("55%", "55 %"),
                ("75%", "75 %"),
                ("100%", "100 %")]

    @api.model
    def _get_top_pattern_selection(self):
        return [("smooth", "Ironing"),
                ("rectilinear", "Rectilinear"),
                ("rectilineargapfill", "Rectilinear (filled)"),
                ("monotonic", "Monotonic"),
                ("concentric", "Concentric"),
                ("concentricgapfill", "Concentric (filled)"),
                ("hilbertcurve", "Hilbert Curve"),
                ("archimedeanchords", "Archimedean Chords"),
                ("octagramspiral", "Octagram Spiral"),
                ("sawtooth", "Sawtooth")]

    @api.model
    def _get_support_pattern_selection(self):
        return [("smooth", "Ironing"),
                ("rectilinear", "Rectilinear"),
                ("monotonic", "Monotonic"),
                ("concentric", "Concentric"),
                ("concentricgapfill", "Concentric (filled)"),
                ("hilbertcurve", "Hilbert Curve"),
                ("sawtooth", "Sawtooth")]

    @api.model
    def _get_solid_pattern_selection(self):
        return [("smooth", "Ironing"),
                ("rectilinear", "Rectilinear"),
                ("rectilineargapfill", "Rectilinear (filled)"),
                ("monotonic", "Monotonic"),
                ("concentric", "Concentric"),
                ("concentricgapfill", "Concentric (filled)"),
                ("hilbertcurve", "Hilbert Curve"),
                ("archimedeanchords", "Archimedean Chords"),
                ("octagramspiral", "Octagram Spiral")]

    @api.model
    def _get_connection_selection(self):
        return [("connected", "Connected"),
                ("holes", "Connected to holes perimeters"),
                ("outershell", "Connected to outer perimeters"),
                ("notconnected", "Not Connected")]

    @api.model
    def _get_infill_algo_selection(self):
        return [("automatic", "Automatic"),
                ("autoenlarged", "Automatic or anchored if too big"),
                ("autosmall", "Automatic only for small areas"),
                ("enlarged", "Anchored")]

    @api.model
    def _get_filament_type_selection(self):
        return [("PLA", "PLA"), ("PET", "PET"), ("ABS", "ABS"), ("ASA", "ASA"), ("FLEX", "FLEX"), ("HIPS", "HIPS"),
                ("EDGE", "EDGE"), ("NGEN", "NGEN"), ("NYLON", "NYLON"), ("PVA", "PVA"), ("PC", "PC"), ("PP", "PP"),
                ("PEI", "PEI"), ("PEEK", "PEEK"), ("PEKK", "PEKK"), ("POM", "POM"), ("PSU", "PSU"),
                ("PVDF", "PVDF"),
                ("SCAFF", "SCAFF")]

    @api.model
    def _get_flavor_selection(self):
        return [("reprapfirmware", "RepRapFirmware"),
                ("repetier", "Repetier"),
                ("teacup", "Teacup"),
                ("makerware", "MakerWare (MakerBot)"),
                ("marlin", "Marlin"),
                ("klipper", "Klipper"),
                ("sailfish", "Sailfish (MakerBot)"),
                ("mach3", "Mach3/LinuxCNC"),
                ("machinekit", "Machinekit"),
                ("smoothie", "Smoothie"),
                ("sprinter", "Sprinter"),
                ("lerdge", "Lerdge"),
                ("no-extrusion", "No extrusion")]

    @api.constrains('extruders_count', 'extruders')
    def _validate_extruders_count(self):
        if self.extruders_count != len(self.extruders):
            raise ValidationError("The number of extruders for this profile is different than the field "
                                  "'Extruders count'. Make sure you configure them both well!")

    name = fields.Char(
        string="Name",
        help="",
        default="My Settings",
        required=True,
        index=True,
    )

    image = fields.Binary(
        string="Profile Image",
        help="Image to show in the client website",
    )

    #########################
    # PRINT:MY SETTINGS
    #########################

    allow_empty_layers = fields.Integer(
        string="Allow empty layers",
        help="",
        default=0,
    )

    avoid_crossing_not_first_layer = fields.Boolean(
        string="Avoid crossing not first layer",
        help="",
        default=True,
    )

    avoid_crossing_perimeters = fields.Boolean(
        string="Avoid crossing perimeters",
        help="",
        default=False,
    )

    avoid_crossing_perimeters_max_detour = fields.Integer(
        string="Avoid crossing perimeters max detour",
        help="",
        default=0,
    )

    bottom_fill_pattern = fields.Selection(
        selection='_get_solid_pattern_selection',
        string="Bottom fill pattern",
        help="",
        default="monotonic",
    )

    bottom_solid_layers = fields.Integer(
        string="Bottom solid layers",
        help="",
        default=3,
    )

    bottom_solid_min_thickness = fields.Float(
        string="Bottom solid min thickness",
        help="",
        default=0,
        digits=(1, 3),
    )

    bridge_acceleration = fields.Integer(
        string="Bridge acceleration",
        help="",
        default=0,
    )

    bridge_angle = fields.Integer(
        string="Bridge angle",
        help="",
        default=0,
    )

    bridge_flow_ratio = fields.Char(
        string="Bridge flow ratio",
        help="",
        default="100%",
    )

    bridge_overlap = fields.Char(
        string="Bridge overlap",
        help="",
        default="100%",
    )

    bridge_speed = fields.Integer(
        string="Bridge speed",
        help="",
        default=60,
    )

    bridge_speed_internal = fields.Char(
        string="Bridge speed internal",
        help="",
        default="150%",
    )

    bridged_infill_margin = fields.Char(
        string="Bridged infill margin",
        help="",
        default="200%",
    )

    brim_ears = fields.Boolean(
        string="Brim ears",
        help="",
        default=False,
    )

    brim_ears_detection_length = fields.Integer(
        string="Brim ears detection length",
        help="",
        default=1,
    )

    brim_ears_max_angle = fields.Integer(
        string="Brim ears max angle",
        help="",
        default=125,
    )

    brim_ears_pattern = fields.Selection(
        selection=[("concentric", "Concentric"), ("rectilinear", "Rectilinear")],
        string="Brim ears pattern",
        help="",
        default="concentric",
    )

    brim_inside_holes = fields.Boolean(
        string="Brim inside holes",
        help="",
        default=False,
    )

    brim_offset = fields.Integer(
        string="Brim offset",
        help="",
        default=0,
    )

    brim_width = fields.Integer(
        string="Brim width",
        help="",
        default=0,
    )

    brim_width_interior = fields.Integer(
        string="Brim width interior",
        help="",
        default=0,
    )

    clip_multipart_objects = fields.Boolean(
        string="Clip multipart objects",
        help="",
        default=True,
    )

    complete_objects = fields.Boolean(
        string="Complete objects",
        help="",
        default=False,
    )

    complete_objects_one_skirt = fields.Boolean(
        string="Complete objects one skirt",
        help="",
        default=False,
    )

    complete_objects_sort = fields.Selection(
        selection=[("object", "Right Panel"), ("lowy", "Lowest Y"), ("lowz", "Lowest Z")],
        string="Complete objects sort",
        help="",
        default="object",
    )

    curve_smoothing_angle_concave = fields.Integer(
        string="Curve smoothing angle concave",
        help="",
        default=0,
    )

    curve_smoothing_angle_convex = fields.Integer(
        string="Curve smoothing angle convex",
        help="",
        default=0,
    )

    curve_smoothing_cutoff_dist = fields.Integer(
        string="Curve smoothing cutoff dist",
        help="",
        default=2,
    )

    curve_smoothing_precision = fields.Integer(
        string="Curve smoothing precision",
        help="",
        default=0,
    )

    default_acceleration = fields.Integer(
        string="Default acceleration",
        help="",
        default=0,
    )

    dont_support_bridges = fields.Boolean(
        string="Dont support bridges",
        help="",
        default=True,
    )

    draft_shield = fields.Boolean(
        string="Draft shield",
        help="",
        default=False,
    )

    duplicate_distance = fields.Integer(
        string="Duplicate distance",
        help="",
        default=6,
    )

    enforce_full_fill_volume = fields.Boolean(
        string="Enforce full fill volume",
        help="",
        default=True,
    )

    ensure_vertical_shell_thickness = fields.Boolean(
        string="Ensure vertical shell thickness",
        help="",
        default=False,
    )

    exact_last_layer_height = fields.Integer(
        string="Exact last layer height",
        help="",
        default=0,
    )

    external_infill_margin = fields.Char(
        string="External infill margin",
        help="",
        default="150%",
    )

    external_perimeter_cut_corners = fields.Char(
        string="External perimeter cut corners",
        help="",
        default="0%",
    )

    external_perimeter_extrusion_spacing = fields.Char(
        string="External perimeter extrusion spacing",
        help="",
        default="100%",
    )

    external_perimeter_extrusion_width = fields.Char(
        string="External perimeter extrusion width",
        help="",
        default="",
    )

    external_perimeter_overlap = fields.Char(
        string="External perimeter overlap",
        help="",
        default="100%",
    )

    external_perimeter_speed = fields.Char(
        string="External perimeter speed",
        help="",
        default="50%",
    )

    external_perimeters_first = fields.Boolean(
        string="External perimeters first",
        help="",
        default=False,
    )

    external_perimeters_hole = fields.Boolean(
        string="External perimeters hole",
        help="",
        default=True,
    )

    external_perimeters_nothole = fields.Boolean(
        string="External perimeters nothole",
        help="",
        default=True,
    )

    external_perimeters_vase = fields.Boolean(
        string="External perimeters vase",
        help="",
        default=False,
    )

    extra_perimeters = fields.Integer(
        string="Extra perimeters",
        help="",
        default=0,
    )

    extra_perimeters_odd_layers = fields.Boolean(
        string="Extra perimeters odd layers",
        help="",
        default=False,
    )

    extra_perimeters_overhangs = fields.Boolean(
        string="Extra perimeters overhangs",
        help="",
        default=False,
    )

    extruder_clearance_height = fields.Integer(
        string="Extruder clearance height",
        help="",
        default=20,
    )

    extruder_clearance_radius = fields.Integer(
        string="Extruder clearance radius",
        help="",
        default=20,
    )

    extrusion_spacing = fields.Char(
        string="Extrusion spacing",
        help="",
        default="105%",
    )

    extrusion_width = fields.Char(
        string="Extrusion width",
        help="",
        default="",
    )

    fill_angle = fields.Integer(
        string="Fill angle",
        help="",
        default=45,
    )

    fill_angle_increment = fields.Integer(
        string="Fill angle increment",
        help="",
        default=0,
    )

    fill_density = fields.Selection(
        selection='_get_fill_density_selection',
        string="Fill density",
        help="",
        default="18%",
    )

    fill_pattern = fields.Selection(
        selection='_get_fill_pattern_selection',
        string="Fill pattern",
        help="",
        default="stars",
    )

    fill_smooth_distribution = fields.Char(
        string="Fill smooth distribution",
        help="",
        default="10%",
    )

    fill_smooth_width = fields.Char(
        string="Fill smooth width",
        help="",
        default="50%",
    )

    fill_top_flow_ratio = fields.Char(
        string="Fill top flow ratio",
        help="",
        default="100%",
    )

    first_layer_acceleration = fields.Integer(
        string="First layer acceleration",
        help="",
        default=0,
    )

    first_layer_extrusion_spacing = fields.Char(
        string="First layer extrusion spacing",
        help="",
        default="140%",
    )

    first_layer_extrusion_width = fields.Char(
        string="First layer extrusion width",
        help="",
        default="151%",
    )

    first_layer_flow_ratio = fields.Char(
        string="First layer flow ratio",
        help="",
        default="100%",
    )

    first_layer_height = fields.Char(
        string="First layer height",
        help="",
        default="75%",
    )

    first_layer_infill_speed = fields.Integer(
        string="First layer infill speed",
        help="",
        default=30,
    )

    first_layer_size_compensation = fields.Integer(
        string="First layer size compensation",
        help="",
        default=0,
    )

    first_layer_speed = fields.Integer(
        string="First layer speed",
        help="",
        default=30,
    )

    gap_fill = fields.Boolean(
        string="Gap fill",
        help="",
        default=True,
    )

    gap_fill_min_area = fields.Char(
        string="Gap fill min area",
        help="",
        default="100%",
    )

    gap_fill_overlap = fields.Char(
        string="Gap fill overlap",
        help="",
        default="100%",
    )

    gap_fill_speed = fields.Integer(
        string="Gap fill speed",
        help="",
        default=20,
    )

    gcode_comments = fields.Boolean(
        string="Gcode comments",
        help="",
        default=False,
    )

    gcode_label_objects = fields.Boolean(
        string="Gcode label objects",
        help="",
        default=True,
    )

    hole_size_compensation = fields.Integer(
        string="Hole size compensation",
        help="",
        default=0,
    )

    hole_size_threshold = fields.Integer(
        string="Hole size threshold",
        help="",
        default=100,
    )

    hole_to_polyhole = fields.Boolean(
        string="Hole to polyhole",
        help="",
        default=False,
    )

    hole_to_polyhole_threshold = fields.Float(
        string="Hole to polyhole threshold",
        help="",
        default=0.01,
        digits=(1, 2),
    )

    infill_acceleration = fields.Integer(
        string="Infill acceleration",
        help="",
        default=0,
    )

    infill_anchor = fields.Char(
        string="Infill anchor",
        help="",
        default="600%",
    )

    infill_anchor_max = fields.Integer(
        string="Infill anchor max",
        help="",
        default=0,
    )

    infill_connection = fields.Selection(
        selection='_get_connection_selection',
        string="Infill connection",
        help="",
        default="connected",
    )

    infill_connection_bottom = fields.Selection(
        selection='_get_connection_selection',
        string="Infill connection bottom",
        help="",
        default="connected",
    )

    infill_connection_solid = fields.Selection(
        selection='_get_connection_selection',
        string="Infill connection solid",
        help="",
        default="connected",
    )

    infill_connection_top = fields.Selection(
        selection='_get_connection_selection',
        string="Infill connection top",
        help="",
        default="connected",
    )

    infill_dense = fields.Boolean(
        string="Infill dense",
        help="",
        default=False,
    )

    infill_dense_algo = fields.Selection(
        selection='_get_infill_algo_selection',
        string="Infill dense algo",
        help="",
        default="autoenlarged",
    )

    infill_every_layers = fields.Integer(
        string="Infill every layers",
        help="",
        default=1,
    )

    infill_extruder = fields.Integer(
        string="Infill extruder",
        help="",
        default=1,
    )

    infill_extrusion_spacing = fields.Char(
        string="Infill extrusion spacing",
        help="",
        default="100%",
    )

    infill_extrusion_width = fields.Char(
        string="Infill extrusion width",
        help="",
        default="",
    )

    infill_first = fields.Integer(
        string="Infill first",
        help="",
        default=0,
    )

    infill_only_where_needed = fields.Boolean(
        string="Infill only where needed",
        help="",
        default=False,
    )

    infill_overlap = fields.Char(
        string="Infill overlap",
        help="",
        default="25%",
    )

    infill_speed = fields.Integer(
        string="Infill speed",
        help="",
        default=80,
    )

    inherits = fields.Char(
        string="Inherits",
        help="",
        default="",
    )

    interface_shells = fields.Boolean(
        string="Interface shells",
        help="",
        default=False,
    )

    ironing = fields.Boolean(
        string="Ironing",
        help="",
        default=False,
    )

    ironing_angle = fields.Float(
        string="Ironing angle",
        help="",
        default=-1,
        digits=(1, 0),
    )

    ironing_flowrate = fields.Char(
        string="Ironing flowrate",
        help="",
        default="15%",
    )

    ironing_spacing = fields.Float(
        string="Ironing spacing",
        help="",
        default=0.1,
        digits=(1, 2),
    )

    ironing_speed = fields.Integer(
        string="Ironing speed",
        help="",
        default=15,
    )

    ironing_type = fields.Selection(
        selection=[("top", "All top surfaces"), ("topmost", "Topmost surface only"), ("solid", "All solid surfaces")],
        string="Ironing type",
        help="",
        default="top",
    )

    layer_height = fields.Float(
        string="Layer height",
        help="",
        default=0.2,
        digits=(1, 2),
    )

    max_print_speed = fields.Integer(
        string="Max print speed",
        help="",
        default=80,
    )

    max_volumetric_speed = fields.Integer(
        string="Max volumetric speed",
        help="",
        default=0,
    )

    milling_after_z = fields.Char(
        string="Milling after z",
        help="",
        default="200%",
    )

    milling_extra_size = fields.Char(
        string="Milling extra size",
        help="",
        default="150%",
    )

    milling_post_process = fields.Boolean(
        string="Milling post process",
        help="",
        default=False,
    )

    milling_speed = fields.Integer(
        string="Milling speed",
        help="",
        default=30,
    )

    min_skirt_length = fields.Integer(
        string="Min skirt length",
        help="",
        default=0,
    )

    min_width_top_surface = fields.Char(
        string="Min width top surface",
        help="",
        default="200%",
    )

    model_precision = fields.Float(
        string="Model precision",
        help="",
        default=0.0001,
        digits=(1, 4),
    )

    no_perimeter_unsupported_algo = fields.Selection(
        selection='_get_algo_selection',
        string="No perimeter unsupported algo",
        help="",
        default="none",
    )

    notes = fields.Text(
        string="Notes",
        help="",
        default="",
    )

    only_one_perimeter_top = fields.Boolean(
        string="Only one perimeter top",
        help="",
        default=True,
    )

    only_one_perimeter_top_other_algo = fields.Integer(
        string="Only one perimeter top other algo",
        help="",
        default=0,
    )

    only_retract_when_crossing_perimeters = fields.Boolean(
        string="Only retract when crossing perimeters",
        help="",
        default=True,
    )

    ooze_prevention = fields.Boolean(
        string="Ooze prevention",
        help="",
        default=False,
    )

    output_filename_format = fields.Char(
        string="Output filename format",
        help="",
        default="[input_filename_base].gcode",
    )

    over_bridge_flow_ratio = fields.Char(
        string="Over bridge flow ratio",
        help="",
        default="100%",
    )

    overhangs_reverse = fields.Boolean(
        string="Overhangs reverse",
        help="",
        default=False,
    )

    overhangs_reverse_threshold = fields.Char(
        string="Overhangs reverse threshold",
        help="",
        default="250%",
    )

    overhangs_speed = fields.Char(
        string="Overhangs speed",
        help="",
        default="100%",
    )

    overhangs_width = fields.Char(
        string="Overhangs width",
        help="",
        default="75%",
    )

    overhangs_width_speed = fields.Char(
        string="Overhangs width speed",
        help="",
        default="55%",
    )

    perimeter_acceleration = fields.Integer(
        string="Perimeter acceleration",
        help="",
        default=0,
    )

    perimeter_bonding = fields.Char(
        string="Perimeter bonding",
        help="",
        default="0%",
    )

    perimeter_extruder = fields.Integer(
        string="Perimeter extruder",
        help="",
        default=1,
    )

    perimeter_extrusion_spacing = fields.Char(
        string="Perimeter extrusion spacing",
        help="",
        default="105%",
    )

    perimeter_extrusion_width = fields.Char(
        string="Perimeter extrusion width",
        help="",
        default="",
    )

    perimeter_loop = fields.Boolean(
        string="Perimeter loop",
        help="",
        default=False,
    )

    perimeter_loop_seam = fields.Selection(
        selection=[("rear", "Rear"), ("hidden", "Nearest")],
        string="Perimeter loop seam",
        help="",
        default="rear",
    )

    perimeter_overlap = fields.Char(
        string="Perimeter overlap",
        help="",
        default="100%",
    )

    perimeter_round_corners = fields.Boolean(
        string="Perimeter round corners",
        help="",
        default=False,
    )

    perimeter_speed = fields.Integer(
        string="Perimeter speed",
        help="",
        default=60,
    )

    perimeters = fields.Integer(
        string="Perimeters",
        help="",
        default=3,
    )

    post_process = fields.Text(
        string="Post process",
        help="",
        default="",
    )

    print_extrusion_multiplier = fields.Char(
        string="Print extrusion multiplier",
        help="",
        default="100%",
    )

    print_retract_length = fields.Float(
        string="Print retract length",
        help="",
        default=-1,
        digits=(1, 0),
    )

    print_retract_lift = fields.Float(
        string="Print retract lift",
        help="",
        default=-1,
        digits=(1, 0),
    )

    print_settings_id = fields.Char(
        string="Print settings id",
        help="",
        default="",
    )

    print_temperature = fields.Integer(
        string="Print temperature",
        help="",
        default=0,
    )

    raft_layers = fields.Integer(
        string="Raft layers",
        help="",
        default=0,
    )

    resolution = fields.Float(
        string="Resolution",
        help="",
        default=0.002,
        digits=(1, 3),
    )

    seam_angle_cost = fields.Char(
        string="Seam angle cost",
        help="",
        default="100%",
    )

    seam_position = fields.Selection(
        selection='_get_seam_selection',
        string="Seam position",
        help="",
        default="hidden",
    )

    seam_travel_cost = fields.Char(
        string="Seam travel cost",
        help="",
        default="100%",
    )

    single_extruder_multi_material_priming = fields.Boolean(
        string="Single extruder multi material priming",
        help="",
        default=True,
    )

    skirt_distance = fields.Integer(
        string="Skirt distance",
        help="",
        default=6,
    )

    skirt_extrusion_width = fields.Char(
        string="Skirt extrusion width",
        help="",
        default="110%",
    )

    skirt_height = fields.Integer(
        string="Skirt height",
        help="",
        default=1,
    )

    skirts = fields.Integer(
        string="Skirts",
        help="",
        default=1,
    )

    slice_closing_radius = fields.Float(
        string="Slice closing radius",
        help="",
        default=0.049,
        digits=(1, 3),
    )

    small_perimeter_max_length = fields.Integer(
        string="Small perimeter max length",
        help="",
        default=20,
    )

    small_perimeter_min_length = fields.Integer(
        string="Small perimeter min length",
        help="",
        default=6,
    )

    small_perimeter_speed = fields.Integer(
        string="Small perimeter speed",
        help="",
        default=15,
    )

    solid_fill_pattern = fields.Selection(
        selection='_get_solid_pattern_selection',
        string="Solid fill pattern",
        help="",
        default="rectilineargapfill",
    )

    solid_infill_below_area = fields.Integer(
        string="Solid infill below area",
        help="",
        default=70,
    )

    solid_infill_every_layers = fields.Integer(
        string="Solid infill every layers",
        help="",
        default=0,
    )

    solid_infill_extruder = fields.Integer(
        string="Solid infill extruder",
        help="",
        default=1,
    )

    solid_infill_extrusion_spacing = fields.Char(
        string="Solid infill extrusion spacing",
        help="",
        default="105%",
    )

    solid_infill_extrusion_width = fields.Char(
        string="Solid infill extrusion width",
        help="",
        default="",
    )

    solid_infill_speed = fields.Integer(
        string="Solid infill speed",
        help="",
        default=20,
    )

    spiral_vase = fields.Boolean(
        string="Spiral vase",
        help="",
        default=False,
    )

    standby_temperature_delta = fields.Float(
        string="Standby temperature delta",
        help="",
        default=-5,
        digits=(1, 0),
    )

    support_material = fields.Boolean(
        string="Support material",
        help="",
        default=False,
    )

    support_material_angle = fields.Integer(
        string="Support material angle",
        help="",
        default=0,
    )

    support_material_auto = fields.Boolean(
        string="Support material auto",
        help="",
        default=True,
    )

    support_material_buildplate_only = fields.Boolean(
        string="Support material buildplate only",
        help="",
        default=False,
    )

    support_material_contact_distance_bottom = fields.Float(
        string="Support material contact distance bottom",
        help="",
        default=0.2,
        digits=(1, 2),
    )

    support_material_contact_distance_top = fields.Float(
        string="Support material contact distance top",
        help="",
        default=0.2,
        digits=(1, 2),
    )

    support_material_contact_distance_type = fields.Selection(
        selection=[("plane", "From plane"), ("filament", "From filament"), ("none", "None")],
        string="Support material contact distance type",
        help="",
        default="plane",
    )

    support_material_enforce_layers = fields.Integer(
        string="Support material enforce layers",
        help="",
        default=0,
    )

    support_material_extruder = fields.Integer(
        string="Support material extruder",
        help="",
        default=1,
    )

    support_material_extrusion_width = fields.Char(
        string="Support material extrusion width",
        help="",
        default="100%",
    )

    support_material_interface_contact_loops = fields.Boolean(
        string="Support material interface contact loops",
        help="",
        default=False,
    )

    support_material_interface_extruder = fields.Integer(
        string="Support material interface extruder",
        help="",
        default=1,
    )

    support_material_interface_layers = fields.Integer(
        string="Support material interface layers",
        help="",
        default=3,
    )

    support_material_interface_pattern = fields.Selection(
        selection='_get_support_pattern_selection',
        string="Support material interface pattern",
        help="",
        default="rectilinear",
    )

    support_material_interface_spacing = fields.Integer(
        string="Support material interface spacing",
        help="",
        default=0,
    )

    support_material_interface_speed = fields.Char(
        string="Support material interface speed",
        help="",
        default="100%",
    )

    support_material_pattern = fields.Selection(
        selection=[("rectilinear", "Rectilinear"), ("rectilinear-grid", "Rectilinear grid"),
                   ("honeycomb", "Honeycomb")],
        string="Support material pattern",
        help="",
        default="rectilinear",
    )

    support_material_solid_first_layer = fields.Integer(
        string="Support material solid first layer",
        help="",
        default=0,
    )

    support_material_spacing = fields.Float(
        string="Support material spacing",
        help="",
        default=2.5,
        digits=(1, 2),
    )

    support_material_speed = fields.Integer(
        string="Support material speed",
        help="",
        default=60,
    )

    support_material_synchronize_layers = fields.Boolean(
        string="Support material synchronize layers",
        help="",
        default=False,
    )

    support_material_threshold = fields.Integer(
        string="Support material threshold",
        help="",
        default=0,
    )

    support_material_with_sheath = fields.Boolean(
        string="Support material with sheath",
        help="",
        default=True,
    )

    support_material_xy_spacing = fields.Char(
        string="Support material xy spacing",
        help="",
        default="50%",
    )

    thin_perimeters = fields.Boolean(
        string="Thin perimeters",
        help="",
        default=True,
    )

    thin_perimeters_all = fields.Boolean(
        string="Thin perimeters all",
        help="",
        default=False,
    )

    thin_walls = fields.Boolean(
        string="Thin walls",
        help="",
        default=True,
    )

    thin_walls_merge = fields.Boolean(
        string="Thin walls merge",
        help="",
        default=True,
    )

    thin_walls_min_width = fields.Char(
        string="Thin walls min width",
        help="",
        default="33%",
    )

    thin_walls_overlap = fields.Char(
        string="Thin walls overlap",
        help="",
        default="50%",
    )

    thin_walls_speed = fields.Integer(
        string="Thin walls speed",
        help="",
        default=30,
    )

    threads = fields.Integer(
        string="Threads",
        help="",
        default=8,
    )

    top_fill_pattern = fields.Selection(
        selection='_get_top_pattern_selection',
        string="Top fill pattern",
        help="",
        default="monotonic",
    )

    top_infill_extrusion_spacing = fields.Char(
        string="Top infill extrusion spacing",
        help="",
        default="100%",
    )

    top_infill_extrusion_width = fields.Char(
        string="Top infill extrusion width",
        help="",
        default="",
    )

    top_solid_infill_speed = fields.Integer(
        string="Top solid infill speed",
        help="",
        default=15,
    )

    top_solid_layers = fields.Integer(
        string="Top solid layers",
        help="",
        default=3,
    )

    top_solid_min_thickness = fields.Float(
        string="Top solid min thickness",
        help="",
        default=0,
        digits=(1, 3),
    )

    travel_speed = fields.Integer(
        string="Travel speed",
        help="",
        default=130,
    )

    travel_speed_z = fields.Integer(
        string="Travel speed z",
        help="",
        default=0,
    )

    wipe_tower = fields.Boolean(
        string="Wipe tower",
        help="",
        default=False,
    )

    wipe_tower_bridging = fields.Integer(
        string="Wipe tower bridging",
        help="",
        default=10,
    )

    wipe_tower_brim = fields.Char(
        string="Wipe tower brim",
        help="",
        default="150%",
    )

    wipe_tower_no_sparse_layers = fields.Boolean(
        string="Wipe tower no sparse layers",
        help="",
        default=False,
    )

    wipe_tower_rotation_angle = fields.Integer(
        string="Wipe tower rotation angle",
        help="",
        default=0,
    )

    wipe_tower_width = fields.Integer(
        string="Wipe tower width",
        help="",
        default=60,
    )

    wipe_tower_x = fields.Integer(
        string="Wipe tower x",
        help="",
        default=180,
    )

    wipe_tower_y = fields.Integer(
        string="Wipe tower y",
        help="",
        default=140,
    )

    xy_inner_size_compensation = fields.Integer(
        string="XY inner size compensation",
        help="",
        default=0,
    )

    xy_size_compensation = fields.Integer(
        string="XY size compensation",
        help="",
        default=0,
    )

    #########################
    # FILAMENT:MY SETTINGS
    #########################

    bed_temperature = fields.Integer(
        string="Bed temperature",
        help="",
        default=0,
    )

    bridge_fan_speed = fields.Integer(
        string="Bridge fan speed",
        help="",
        default=100,
    )

    chamber_temperature = fields.Integer(
        string="Chamber temperature",
        help="",
        default=0,
    )

    cooling = fields.Integer(
        string="Cooling",
        help="",
        default=1,
    )

    disable_fan_first_layers = fields.Integer(
        string="Disable fan first layers",
        help="",
        default=3,
    )

    end_filament_gcode = fields.Text(
        string="End filament gcode",
        help="",
        default="; Filament-specific end gcode \n;END gcode for filament\n",
    )

    external_perimeter_fan_speed = fields.Integer(
        string="External perimeter fan speed",
        help="",
        default=-1,
    )

    extrusion_multiplier = fields.Integer(
        string="Extrusion multiplier",
        help="",
        default=1,
    )

    fan_always_on = fields.Boolean(
        string="Fan always on",
        help="",
        default=False,
    )

    fan_below_layer_time = fields.Integer(
        string="Fan below layer time",
        help="",
        default=60,
    )

    filament_colour = fields.Char(
        string="Filament colour",
        help="",
        default="#29B2B2",
    )

    filament_cooling_final_speed = fields.Float(
        string="Filament cooling final speed",
        help="",
        default=3.4,
        digits=(1, 1),
    )

    filament_cooling_initial_speed = fields.Float(
        string="Filament cooling initial speed",
        help="",
        default=2.2,
        digits=(1, 1),
    )

    filament_cooling_moves = fields.Integer(
        string="Filament cooling moves",
        help="",
        default=4,
    )

    filament_cooling_zone_pause = fields.Integer(
        string="Filament cooling zone pause",
        help="",
        default=0,
    )

    filament_cost = fields.Integer(
        string="Filament cost",
        help="",
        default=0,
    )

    filament_density = fields.Integer(
        string="Filament density",
        help="",
        default=0,
    )

    filament_deretract_speed = fields.Char(
        string="Filament deretract speed",
        help="",
        default="nil",
    )

    filament_diameter = fields.Float(
        string="Filament diameter",
        help="",
        default=1.75,
        digits=(1, 2),
    )

    filament_dip_extraction_speed = fields.Integer(
        string="Filament dip extraction speed",
        help="",
        default=70,
    )

    filament_dip_insertion_speed = fields.Integer(
        string="Filament dip insertion speed",
        help="",
        default=33,
    )

    filament_enable_toolchange_part_fan = fields.Boolean(
        string="Filament enable toolchange part fan",
        help="",
        default=False,
    )

    filament_enable_toolchange_temp = fields.Boolean(
        string="Filament enable toolchange temp",
        help="",
        default=False,
    )

    filament_load_time = fields.Integer(
        string="Filament load time",
        help="",
        default=0,
    )

    filament_loading_speed = fields.Integer(
        string="Filament loading speed",
        help="",
        default=28,
    )

    filament_loading_speed_start = fields.Integer(
        string="Filament loading speed start",
        help="",
        default=3,
    )

    filament_max_speed = fields.Integer(
        string="Filament max speed",
        help="",
        default=0,
    )

    filament_max_volumetric_speed = fields.Integer(
        string="Filament max volumetric speed",
        help="",
        default=0,
    )

    filament_max_wipe_tower_speed = fields.Integer(
        string="Filament max wipe tower speed",
        help="",
        default=0,
    )

    filament_melt_zone_pause = fields.Integer(
        string="Filament melt zone pause",
        help="",
        default=0,
    )

    filament_minimal_purge_on_wipe_tower = fields.Integer(
        string="Filament minimal purge on wipe tower",
        help="",
        default=15,
    )

    filament_notes = fields.Text(
        string="Filament notes",
        help="",
        default="",
    )

    filament_ramming_parameters = fields.Char(
        string="Filament ramming parameters",
        help="",
        default="120 100 6.6 6.8 7.2 7.6 7.9 8.2 8.7 9.4 9.9 10.0| 0.05 6.6 0.45 6.8 0.95 7.8 1.45 8.3 1.95 9.7 2.45 "
                "10 2.95 7.6 3.45 7.6 3.95 7.6 4.45 7.6 4.95 7.6",
    )

    filament_retract_before_travel = fields.Char(
        string="Filament retract before travel",
        help="",
        default="nil",
    )

    filament_retract_before_wipe = fields.Char(
        string="Filament retract before wipe",
        help="",
        default="nil",
    )

    filament_retract_layer_change = fields.Boolean(
        string="Filament retract layer change",
        help="",
        default=False,
    )

    filament_retract_length = fields.Char(
        string="Filament retract length",
        help="",
        default="nil",
    )

    filament_retract_lift = fields.Char(
        string="Filament retract lift",
        help="",
        default="nil",
    )

    filament_retract_lift_above = fields.Char(
        string="Filament retract lift above",
        help="",
        default="nil",
    )

    filament_retract_lift_below = fields.Char(
        string="Filament retract lift below",
        help="",
        default="nil",
    )

    filament_retract_restart_extra = fields.Char(
        string="Filament retract restart extra",
        help="",
        default="nil",
    )

    filament_retract_speed = fields.Char(
        string="Filament retract speed",
        help="",
        default="nil",
    )

    filament_settings_id = fields.Char(
        string="Filament settings id",
        help="",
        default="",
    )

    filament_shrink = fields.Char(
        string="Filament shrink",
        help="",
        default="100%",
    )

    filament_skinnydip_distance = fields.Integer(
        string="Filament skinnydip distance",
        help="",
        default=31,
    )

    filament_soluble = fields.Boolean(
        string="Filament soluble",
        help="",
        default=False,
    )

    filament_spool_weight = fields.Integer(
        string="Filament spool weight",
        help="",
        default=0,
    )

    filament_toolchange_delay = fields.Integer(
        string="Filament toolchange delay",
        help="",
        default=0,
    )

    filament_toolchange_part_fan_speed = fields.Integer(
        string="Filament toolchange part fan speed",
        help="",
        default=50,
    )

    filament_toolchange_temp = fields.Integer(
        string="Filament toolchange temp",
        help="",
        default=200,
    )

    filament_type = fields.Selection(
        selection="_get_filament_type_selection",
        string="Filament type",
        help="",
        default="PLA",
    )

    filament_unload_time = fields.Integer(
        string="Filament unload time",
        help="",
        default=0,
    )

    filament_unloading_speed = fields.Integer(
        string="Filament unloading speed",
        help="",
        default=90,
    )

    filament_unloading_speed_start = fields.Integer(
        string="Filament unloading speed start",
        help="",
        default=100,
    )

    filament_use_fast_skinnydip = fields.Boolean(
        string="Filament use fast skinnydip",
        help="",
        default=False,
    )

    filament_use_skinnydip = fields.Boolean(
        string="Filament use skinnydip",
        help="",
        default=False,
    )

    filament_vendor = fields.Char(
        string="Filament vendor",
        help="",
        default="(Unknown)",
    )

    filament_wipe = fields.Boolean(
        string="Filament wipe",
        help="",
        default=False,
    )

    filament_wipe_advanced_pigment = fields.Float(
        string="Filament wipe advanced pigment",
        help="",
        default=0.5,
        digits=(1, 1),
    )

    filament_wipe_extra_perimeter = fields.Char(
        string="Filament wipe extra perimeter",
        help="",
        default="nil",
    )

    first_layer_bed_temperature = fields.Integer(
        string="First layer bed temperature",
        help="",
        default=0,
    )

    first_layer_temperature = fields.Integer(
        string="First layer temperature",
        help="",
        default=200,
    )

    full_fan_speed_layer = fields.Integer(
        string="Full fan speed layer",
        help="",
        default=0,
    )

    max_fan_speed = fields.Integer(
        string="Max fan speed",
        help="",
        default=100,
    )

    max_speed_reduction = fields.Char(
        string="Max speed reduction",
        help="",
        default="90%",
    )

    min_fan_speed = fields.Integer(
        string="Min fan speed",
        help="",
        default=35,
    )

    min_print_speed = fields.Integer(
        string="Min print speed",
        help="",
        default=10,
    )

    slowdown_below_layer_time = fields.Integer(
        string="Slowdown below layer time",
        help="",
        default=5,
    )

    start_filament_gcode = fields.Text(
        string="Start filament gcode",
        help="",
        default="; Filament gcode\n",
    )

    temperature = fields.Integer(
        string="Temperature",
        help="",
        default=200,
    )

    top_fan_speed = fields.Integer(
        string="Top fan speed",
        help="",
        default=-1,
    )

    #########################
    # PRINTER:MY SETTINGS
    #########################

    bed_custom_model = fields.Char(
        string="Bed custom model",
        help="",
        default="",
    )

    bed_custom_texture = fields.Char(
        string="Bed custom texture",
        help="",
        default="",
    )

    bed_shape = fields.Char(
        string="Bed shape",
        help="",
        default="0x0,200x0,200x200,0x200",
    )

    before_layer_gcode = fields.Text(
        string="Before layer gcode",
        help="",
        default="",
    )

    between_objects_gcode = fields.Text(
        string="Between objects gcode",
        help="",
        default="",
    )

    color_change_gcode = fields.Text(
        string="Color change gcode",
        help="",
        default="M600",
    )

    cooling_tube_length = fields.Integer(
        string="Cooling tube length",
        help="",
        default=5,
    )

    cooling_tube_retraction = fields.Float(
        string="Cooling tube retraction",
        help="",
        default=91.5,
        digits=(1, 2),
    )

    default_filament_profile = fields.Char(
        string="Default filament profile",
        help="",
        default="",
    )

    default_print_profile = fields.Char(
        string="Default print profile",
        help="",
        default="",
    )

    end_gcode = fields.Text(
        string="End gcode",
        help="",
        default="M104 S0 ; turn off temperature\nG28 X0  ; home X axis\nM84     ; disable motors\n",
    )

    extra_loading_move = fields.Float(
        string="Extra loading move",
        help="",
        default=-2,
        digits=(1, 0),
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

    extruders_count = fields.Integer(
        string="Extruders count",
        help="",
        default=1,
    )

    fan_kickstart = fields.Integer(
        string="Fan kickstart",
        help="",
        default=0,
    )

    fan_percentage = fields.Boolean(
        string="Fan percentage",
        help="",
        default=False,
    )

    fan_speedup_overhangs = fields.Boolean(
        string="Fan speedup overhangs",
        help="",
        default=True,
    )

    fan_speedup_time = fields.Integer(
        string="Fan speedup time",
        help="",
        default=0,
    )

    feature_gcode = fields.Text(
        string="Feature gcode",
        help="",
        default="",
    )

    gcode_flavor = fields.Selection(
        selection="_get_flavor_selection",
        string="G-code flavor",
        help="",
        default="marlin",
    )

    gcode_precision_e = fields.Integer(
        string="Gcode precision e",
        help="",
        default=5,
    )

    gcode_precision_xyz = fields.Integer(
        string="Gcode precision xyz",
        help="",
        default=3,
    )

    high_current_on_filament_swap = fields.Integer(
        string="High current on filament swap",
        help="",
        default=0,
    )

    host_type = fields.Char(
        string="Host type",
        help="",
        default="octoprint",
    )

    layer_gcode = fields.Text(
        string="Layer gcode",
        help="",
        default="",
    )

    machine_limits_usage = fields.Selection(
        selection=[("emit_to_gcode", "Also emit limits to G-code"),
                   ("time_estimate_only", "Use also for time estimate"),
                   ("limits", "Use only as safeguards"), ("ignore", "Disable")],
        string="Machine limits usage",
        help="",
        default="time_estimate_only",
    )

    machine_max_acceleration_e = fields.Char(
        string="Machine max acceleration e",
        help="",
        default="10000,5000",
    )

    machine_max_acceleration_extruding = fields.Char(
        string="Machine max acceleration extruding",
        help="",
        default="1500,1250",
    )

    machine_max_acceleration_retracting = fields.Char(
        string="Machine max acceleration retracting",
        help="",
        default="1500,1250",
    )

    machine_max_acceleration_travel = fields.Char(
        string="Machine max acceleration travel",
        help="",
        default="1500,1250",
    )

    machine_max_acceleration_x = fields.Char(
        string="Machine max acceleration x",
        help="",
        default="9000,1000",
    )

    machine_max_acceleration_y = fields.Char(
        string="Machine max acceleration y",
        help="",
        default="9000,1000",
    )

    machine_max_acceleration_z = fields.Char(
        string="Machine max acceleration z",
        help="",
        default="500,200",
    )

    machine_max_feedrate_e = fields.Char(
        string="Machine max feedrate e",
        help="",
        default="120,120",
    )

    machine_max_feedrate_x = fields.Char(
        string="Machine max feedrate x",
        help="",
        default="500,200",
    )

    machine_max_feedrate_y = fields.Char(
        string="Machine max feedrate y",
        help="",
        default="500,200",
    )

    machine_max_feedrate_z = fields.Char(
        string="Machine max feedrate z",
        help="",
        default="12,12",
    )

    machine_max_jerk_e = fields.Char(
        string="Machine max jerk e",
        help="",
        default="2.5,2.5",
    )

    machine_max_jerk_x = fields.Char(
        string="Machine max jerk x",
        help="",
        default="10,10",
    )

    machine_max_jerk_y = fields.Char(
        string="Machine max jerk y",
        help="",
        default="10,10",
    )

    machine_max_jerk_z = fields.Char(
        string="Machine max jerk z",
        help="",
        default="0.2,0.4",
    )

    machine_min_extruding_rate = fields.Char(
        string="Machine min extruding rate",
        help="",
        default="0,0",
    )

    machine_min_travel_rate = fields.Char(
        string="Machine min travel rate",
        help="",
        default="0,0",
    )

    max_print_height = fields.Integer(
        string="Max print height",
        help="",
        default=200,
    )

    milling_count = fields.Integer(
        string="Milling count",
        help="",
        default=0,
    )

    milling_diameter = fields.Char(
        string="Milling diameter",
        help="",
        default="",
    )

    milling_toolchange_end_gcode = fields.Text(
        string="Milling toolchange end gcode",
        help="",
        default="",
    )

    milling_toolchange_start_gcode = fields.Text(
        string="Milling toolchange start gcode",
        help="",
        default="",
    )

    milling_z_lift = fields.Char(
        string="Milling z lift",
        help="",
        default="",
    )

    min_length = fields.Float(
        string="Min length",
        help="",
        default=0.035,
        digits=(1, 3),
    )

    parking_pos_retraction = fields.Integer(
        string="Parking pos retraction",
        help="",
        default=92,
    )

    pause_print_gcode = fields.Text(
        string="Pause print gcode",
        help="",
        default="M601",
    )

    print_host = fields.Char(
        string="Print host",
        help="",
        default="",
    )

    printer_model = fields.Char(
        string="Printer model",
        help="",
        default="",
    )

    printer_notes = fields.Text(
        string="Printer notes",
        help="",
        default="",
    )

    printer_settings_id = fields.Char(
        string="Printer settings id",
        help="",
        default="",
    )

    printer_technology = fields.Char(
        string="Printer technology",
        help="",
        default="FFF",
    )

    printer_variant = fields.Char(
        string="Printer variant",
        help="",
        default="",
    )

    printer_vendor = fields.Char(
        string="Printer vendor",
        help="",
        default="",
    )

    printhost_apikey = fields.Char(
        string="Printhost apikey",
        help="",
        default="",
    )

    printhost_cafile = fields.Char(
        string="Printhost cafile",
        help="",
        default="",
    )

    printhost_port = fields.Char(
        string="Printhost port",
        help="",
        default="",
    )

    remaining_times = fields.Boolean(
        string="Remaining times",
        help="",
        default=False,
    )

    retract_length_toolchange = fields.Integer(
        string="Retract length toolchange",
        help="",
        default=10,
    )

    retract_restart_extra = fields.Integer(
        string="Retract restart extra",
        help="",
        default=0,
    )

    retract_restart_extra_toolchange = fields.Integer(
        string="Retract restart extra toolchange",
        help="",
        default=0,
    )

    silent_mode = fields.Boolean(
        string="Silent mode",
        help="",
        default=True,
    )

    single_extruder_multi_material = fields.Boolean(
        string="Single extruder multi material",
        help="",
        default=False,
    )

    start_gcode = fields.Text(
        string="Start gcode",
        help="",
        default="G28 ; home all axes\nG1 Z5 F5000 ; lift nozzle\n",
    )

    start_gcode_manual = fields.Boolean(
        string="Start gcode manual",
        help="",
        default=False,
    )

    template_custom_gcode = fields.Text(
        string="Template custom gcode",
        help="",
        default="",
    )

    thumbnails = fields.Char(
        string="Thumbnails (x_small x y_small , x_big x y_big)",
        help="",
        default="0x0,0x0",
    )

    thumbnails_color = fields.Char(
        string="Thumbnails color",
        help="",
        default="#018aff",
    )

    thumbnails_custom_color = fields.Boolean(
        string="Thumbnails custom color",
        help="",
        default=False,
    )

    thumbnails_with_bed = fields.Boolean(
        string="Thumbnails with bed",
        help="",
        default=True,
    )

    time_estimation_compensation = fields.Char(
        string="Time estimation compensation",
        help="",
        default="100%",
    )

    tool_name = fields.Char(
        string="Tool name",
        help="",
        default="",
    )

    toolchange_gcode = fields.Text(
        string="Toolchange gcode",
        help="",
        default="",
    )

    use_firmware_retraction = fields.Boolean(
        string="Use firmware retraction",
        help="",
        default=False,
    )

    use_relative_e_distances = fields.Boolean(
        string="Use relative e distances",
        help="",
        default=False,
    )

    use_volumetric_e = fields.Boolean(
        string="Use volumetric e",
        help="",
        default=False,
    )

    variable_layer_height = fields.Boolean(
        string="Variable layer height",
        help="",
        default=True,
    )

    wipe_advanced = fields.Integer(
        string="Wipe advanced",
        help="",
        default=0,
    )

    wipe_advanced_algo = fields.Char(
        string="Wipe advanced algo",
        help="",
        default="linear",
    )

    wipe_advanced_multiplier = fields.Integer(
        string="Wipe advanced multiplier",
        help="",
        default=60,
    )

    wipe_advanced_nozzle_melted_volume = fields.Integer(
        string="Wipe advanced nozzle melted volume",
        help="",
        default=120,
    )

    z_offset = fields.Integer(
        string="Z offset",
        help="",
        default=0,
    )

    z_step = fields.Float(
        string="Z step",
        help="",
        default=0.005,
        digits=(1, 3),
    )

    extruders = fields.One2many(
        comodel_name="slicing.extruder",
        inverse_name="profile",
        string="Extruders",
        default=lambda self: self.env['slicing.extruder'],
    )
