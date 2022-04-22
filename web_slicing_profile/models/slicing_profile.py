from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class SlicingProfile(models.Model):
    _name = "slicing.profile"
    _inherit = "mail.thread"
    _description = "Slicing Profile Settings"
    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'The profile name should be unique!')]

    def _datadict(self):
        # Remove unnecessary parameters from the Profile
        attr = [a for a in dir(self) if not a.startswith('_') and not a.startswith('id') and not a.startswith('create_')
                and 'lambda' not in a and 'CONCURRENCY' not in a and not a.startswith('write_')
                and not a.startswith('message') and not a.startswith('website') and not a.startswith('image')
                and 'note' not in a and not a.startswith('display') and not a.startswith('extruders_count')
                and not a.startswith('milling_count') and 'name' not in a and not a.startswith('no_perimeter_')
                and not callable(getattr(self, a))]
        data = {}
        for a in attr:
            if a != "extruders":
                data[f'{a}'] = getattr(self, a)
            else:
                list_extruders = self.extruders
                count = 1
                data[f'{a}'] = {}
                for ext in list_extruders:
                    attr_ex = [a_ex for a_ex in dir(ext) if not a_ex.startswith('_') and not a_ex.startswith('id')
                               and 'lambda' not in a_ex and 'CONCURRENCY' not in a_ex and not a_ex.startswith('create_')
                               and not a_ex.startswith('write_') and 'profile' not in a_ex and 'note' not in a_ex
                               and not a_ex.startswith('display') and 'name' not in a_ex
                               and not callable(getattr(ext, a_ex))]
                    data_ex = {}
                    for a_ex in attr_ex:
                        data_ex[f'{a_ex}'] = getattr(ext, a_ex)
                    data[f'{a}'][f'{count}'] = data_ex
                    count += 1
        return data

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
        help="Do not prevent the gcode builder to trigger an exception if a full layer is "
             "empty and so the print will have to start from thin air afterward.",
        default=0,
    )

    avoid_crossing_not_first_layer = fields.Boolean(
        string="Avoid crossing not first layer",
        help="Do not use the 'Avoid crossing perimeters' on the first layer.",
        default=True,
    )

    avoid_crossing_perimeters = fields.Boolean(
        string="Avoid crossing perimeters",
        help="Optimize travel moves in order to minimize the crossing of perimeters. This is "
             "mostly useful with Bowden extruders which suffer from oozing. This feature slows "
             "down both the print and the G_code generation.",
        default=False,
    )

    avoid_crossing_perimeters_max_detour = fields.Integer(
        string="Avoid crossing perimeters max detour",
        help="The maximum detour length for avoid crossing perimeters. If the detour is longer "
             "than this value, avoid crossing perimeters is not applied for this travel path. "
             "Detour length could be specified either as an absolute value or as percentage "
             "(for example 50%) of a direct travel path. (mm or % (zero to disable), default: 0)",
        default=0,
    )

    bottom_fill_pattern = fields.Selection(
        selection='_get_solid_pattern_selection',
        string="Bottom fill pattern",
        help="Fill pattern for bottom infill. This only affects the bottom visible layer, and "
             "not its adjacent solid shells. (rectilinear, monotonicgapfill, monotonic, "
             "concentric, concentricgapfill, hilbertcurve, archimedeanchords, octagramspiral, "
             "smooth; default: monotonic)",
        default="monotonic",
    )

    bottom_solid_layers = fields.Integer(
        string="Bottom solid layers",
        help="Number of solid layers to generate on bottom surfaces. (default: 3)",
        default=3,
    )

    bottom_solid_min_thickness = fields.Float(
        string="Bottom solid min thickness",
        help="The number of bottom solid layers is increased above bottom_solid_layers if "
             "necessary to satisfy minimum thickness of bottom shell. (mm, default: 0)",
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
        help="Bridging angle override. If left to zero, the bridging angle will be calculated "
             "automatically. Otherwise the provided angle will be used for all bridges. Use "
             "180° for zero angle. (°, default: 0)",
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
        help="This parameter grows the bridged solid infill layers by the specified mm to "
             "anchor them into the part. Put 0 to deactivate it. Can be a % of the width of "
             "the external perimeter. (mm/%, default: 200%)",
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
        help="Pattern for the ear. The concentric is the default one. The rectilinear has a "
             "perimeter around it, you can try it if the concentric has too many problems to "
             "stick to the build plate. (concentric, rectilinear; default: concentric)",
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
        help="When printing multi_material objects, this settings will make Slic3r to clip the "
             "overlapping object parts one by the other (2nd part will be clipped by the 1st,"
             "3rd part will be clipped by the 1st and 2nd etc).",
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
        help="Minimum (concave) angle at a vertex to enable smoothing (trying to create a "
             "curve around the vertex). 180 : nothing will be smooth, 0 : all angles will be "
             "smoothened. (°, default: 0)",
        default=0,
    )

    curve_smoothing_angle_convex = fields.Integer(
        string="Curve smoothing angle convex",
        help="Minimum (convex) angle at a vertex to enable smoothing (trying to create a curve "
             "around the vertex). 180 : nothing will be smooth, 0 : all angles will be "
             "smoothened. (°, default: 0)",
        default=0,
    )

    curve_smoothing_cutoff_dist = fields.Integer(
        string="Curve smoothing cutoff dist",
        help="Maximum distance between two points to allow adding new ones. Allow to avoid"
             "distorting long strait areas. 0 to disable. (mm, default: 2)",
        default=2,
    )

    curve_smoothing_precision = fields.Integer(
        string="Curve smoothing precision",
        help="These parameters allow the slicer to smooth the angles in each layer. The "
             "precision will be at least the new precision of the curve. Set to 0 to "
             "deactivate. Note: as it uses the polygon's edges and only works in the 2D "
             "planes, you must have a very clean or hand_made 3D model. It's really only "
             "useful to smoothen functional models or very wide angles. (mm, default: 0)",
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
        help="If enabled, the skirt will be as tall as a highest printed object. This is "
             "useful to protect an ABS or ASA print from warping and detaching from print bed "
             "due to wind draft.",
        default=False,
    )

    duplicate_distance = fields.Integer(
        string="Duplicate distance",
        help="",
        default=6,
    )

    enforce_full_fill_volume = fields.Boolean(
        string="Enforce full fill volume",
        help="Experimental option which modifies (in solid infill) fill flow to have the exact "
             "amount of plastic inside the volume to fill (it generally changes the flow from "
             "_7% to +4%, depending on the size of the surface to fill and the overlap "
             "parameters, but it can go as high as +50% for infill in very small areas where "
             "rectilinear doesn't have good coverage). It has the advantage to remove the"
             "over_extrusion seen in thin infill areas, from the overlap ratio",
        default=True,
    )

    ensure_vertical_shell_thickness = fields.Boolean(
        string="Ensure vertical shell thickness",
        help="Add solid infill near sloping surfaces to guarantee the vertical shell thickness "
             "(top+bottom solid layers).",
        default=False,
    )

    exact_last_layer_height = fields.Integer(
        string="Exact last layer height",
        help="This setting controls the height of last object layers to put the last layer at "
             "the exact highest height possible. Experimental.",
        default=0,
    )

    external_infill_margin = fields.Char(
        string="External infill margin",
        help="This parameter grows the top/bottom/solid layers by the specified mm to anchor "
             "them into the part. Put 0 to deactivate it. Can be a % of the width of the "
             "perimeters. (mm/%, default: 150%)",
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
        default="105%",
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
        help="Print contour perimeters from the outermost one to the innermost one instead of "
             "the default inverse order.",
        default=False,
    )

    external_perimeters_hole = fields.Boolean(
        string="External perimeters hole",
        help="Only do the vase trick on the external side. Useful when you only want to remove "
             "seam from screw hole.",
        default=True,
    )

    external_perimeters_nothole = fields.Boolean(
        string="External perimeters nothole",
        help="Only do the vase trick on the external side. Useful when the thickness is too low.",
        default=True,
    )

    external_perimeters_vase = fields.Boolean(
        string="External perimeters vase",
        help="Print contour perimeters in two circles, in a continuous way, like for a vase "
             "mode. It needs the external_perimeters_first parameter to work. Doesn't work for "
             "the first layer, as it may damage the bed overwise. Note that it will use "
             "min_layer_height from your hardware setting as the base height (it doesn't start "
             "at 0), so be sure to put here the lowest value your printer can handle. if it's "
             "not lower than two times the current layer height, it falls back to the normal "
             "algorithm, as there is not enough room to do two loops.",
        default=False,
    )

    extra_perimeters = fields.Integer(
        string="Extra perimeters",
        help="Add more perimeters when needed for avoiding gaps in sloping walls. Slic3r keeps "
             "adding perimeters, until more than 70% of the loop immediately above is "
             "supported. If you succeed in triggering the algorithm behind this setting, "
             "please send me a message. Personally, I think it's useless.",
        default=0,
    )

    extra_perimeters_odd_layers = fields.Boolean(
        string="Extra perimeters odd layers",
        help="Add one perimeter every odd layer. With this, infill is taken into the sandwich "
             "and you may be able to reduce drastically the infill/perimeter overlap setting.",
        default=False,
    )

    extra_perimeters_overhangs = fields.Boolean(
        string="Extra perimeters overhangs",
        help="Add more perimeters when needed for avoiding gaps in sloping walls. Slic3r keeps "
             "adding perimeters until all overhangs are filled. !! this is a very slow "
             "algorithm !! If you use this setting, strongly consider also using "
             "overhangs_reverse.",
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
        default="116%",
    )

    fill_angle = fields.Integer(
        string="Fill angle",
        help="Default base angle for infill orientation. Cross_hatching will be applied to "
             "this. Bridges will be infilled using the best direction Slic3r can detect, so "
             "this setting does not affect them. (°, default: 45)",
        default=45,
    )

    fill_angle_increment = fields.Integer(
        string="Fill angle increment",
        help="Add this angle each layer to the base angle for infill. May be useful for art, "
             "or to be sure to hit every object's feature even with very low infill. Still "
             "experimental, tell me what makes it useful, or the problems that arise using it. (°, default: 0)",
        default=0,
    )

    fill_density = fields.Selection(
        selection='_get_fill_density_selection',
        string="Fill density",
        help="Density of internal infill, expressed in the range 0% _ 100%. (%, default: 18%)",
        default="18%",
    )

    fill_pattern = fields.Selection(
        selection='_get_fill_pattern_selection',
        string="Fill pattern",
        help="Fill pattern for general low_density infill. (rectilinear, monotonic, grid, "
             "triangles, stars, cubic, line, concentric, honeycomb, 3dhoneycomb, gyroid, "
             "hilbertcurve, archimedeanchords, octagramspiral, scatteredrectilinear, "
             "adaptivecubic, supportcubic; default: stars)",
        default="stars",
    )

    fill_smooth_distribution = fields.Char(
        string="Fill smooth distribution",
        help="This is the percentage of the flow that is used for the second ironing pass. "
             "Typical 10_20%. Should not be higher than 20%, unless you have your top "
             "extrusion width greatly superior to your nozzle width. A value too low and your "
             "extruder will eat the filament. A value too high and the first pass won't print well. (%, default: 10%)",
        default="10%",
    )

    fill_smooth_width = fields.Char(
        string="Fill smooth width",
        help="This is the width of the ironing pass, in a % of the top infill extrusion width, "
             "should not be more than 50% (two times more lines, 50% overlap). It's not "
             "necessary to go below 25% (four times more lines, 75% overlap). If you have "
             "problems with your ironing process, don't forget to look at the flow_>above "
             "bridge flow, as this setting should be set to min 110% to let you have enough "
             "plastic in the top layer. A value too low will make your extruder eat the "
             "filament. (mm/%, default: 50%)",
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
        help="When printing with very low layer heights, you might still want to print a "
             "thicker bottom layer to improve adhesion and tolerance for non perfect build "
             "plates. This can be expressed as an absolute value or as a percentage (for "
             "example: 75%) over the default nozzle width. (mm or %, default: 75%)",
        default="75%",
    )

    first_layer_infill_speed = fields.Integer(
        string="First layer infill speed",
        help="",
        default=30,
    )

    first_layer_size_compensation = fields.Integer(
        string="First layer size compensation",
        help="The first layer will be grown / shrunk in the XY plane by the configured value "
             "to compensate for the 1st layer squish aka an Elephant Foot effect. (should be "
             "negative = inwards) (mm, default: 0)",
        default=0,
    )

    first_layer_speed = fields.Integer(
        string="First layer speed",
        help="",
        default=30,
    )

    gap_fill = fields.Boolean(
        string="Gap fill",
        help="Enable gap fill algorithm. It will extrude small lines between perimeters when "
             "there is not enough space for another perimeter or an infill.",
        default=True,
    )

    gap_fill_min_area = fields.Char(
        string="Gap fill min area",
        help="This setting represents the minimum mm² for a gapfill extrusion to be created. "
             "Can be a % of (perimeter width)² (default: 100%)",
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
        help="The convex holes will be grown / shrunk in the XY plane by the configured value "
             "(negative = inwards, positive = outwards, should be negative as the holes are "
             "always a bit smaller irl). This might be useful for fine_tuning hole sizes. This "
             "setting behaves the same as 'Inner XY size compensation' but only for convex "
             "shapes. It's added to 'Inner XY size compensation', it does not replace it. (mm, default: 0)",
        default=0,
    )

    hole_size_threshold = fields.Integer(
        string="Hole size threshold",
        help="Maximum area for the hole where the hole_size_compensation will apply fully. "
             "After that, it will decrease down to 0 for four times this area. Set to 0 to let "
             "the hole_size_compensation apply fully for all detected holes (mm², default: 100)",
        default=100,
    )

    hole_to_polyhole = fields.Boolean(
        string="Hole to polyhole",
        help="Search for almost_circular holes that span more than one layer and convert the "
             "geometry to polyholes. Use the nozzle size and the (biggest) diameter to compute "
             "the polyhole. See http://hydraraptor.blogspot.com/2011/02/polyholes.html",
        default=False,
    )

    hole_to_polyhole_threshold = fields.Float(
        string="Hole to polyhole threshold",
        help="Maximum defection of a point to the estimated radius of the circle. As cylinders "
             "are often exported as triangles of varying size, points may not be on the circle "
             "circumference. This setting allows you some leway to broaden the detection. In "
             "mm or in % of the radius. (mm², default: 0.01)",
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
        help="Connect an infill line to an internal perimeter with a short segment of an "
             "additional perimeter. If expressed as percentage (example: 15%) it is calculated "
             "over infill extrusion width. Slic3r tries to connect two close infill lines to a "
             "short perimeter segment. If no such perimeter segment shorter than "
             "infill_anchor_max is found, the infill line is connected to a perimeter segment "
             "at just one side and the length of the perimeter segment taken is limited to "
             "this parameter, but no longer than anchor_length_max. Set this parameter to zero "
             "to disable anchoring perimeters connected to a single infill line. (mm or %, default: 600%)",
        default="600%",
    )

    infill_anchor_max = fields.Integer(
        string="Infill anchor max",
        help="Connect an infill line to an internal perimeter with a short segment of an "
             "additional perimeter. If expressed as percentage (example: 15%) it is calculated "
             "over infill extrusion width. Slic3r tries to connect two close infill lines to a "
             "short perimeter segment. If no such perimeter segment shorter than this "
             "parameter is found, the infill line is connected to a perimeter segment at just "
             "one side and the length of the perimeter segment taken is limited to "
             "infill_anchor, but no longer than this parameter. If set to 0, the old algorithm "
             "for infill connection will be used, it should create the same result as with "
             "1000 & 0. (mm or %, default: 0)",
        default=0,
    )

    infill_connection = fields.Selection(
        selection='_get_connection_selection',
        string="Infill connection",
        help="Give to the infill algorithm if the infill needs to be connected, and on which "
             "perimeters Can be useful for art or with high infill/perimeter overlap. The "
             "result may vary between infill types. (connected, holes, outershell, notconnected; default: connected)",
        default="connected",
    )

    infill_connection_bottom = fields.Selection(
        selection='_get_connection_selection',
        string="Infill connection bottom",
        help="Give to the infill algorithm if the infill needs to be connected, and on which "
             "perimeters Can be useful for art or with high infill/perimeter overlap. The "
             "result may vary between infill types. (connected, holes, outershell, notconnected; default: connected)",
        default="connected",
    )

    infill_connection_solid = fields.Selection(
        selection='_get_connection_selection',
        string="Infill connection solid",
        help="Give to the infill algorithm if the infill needs to be connected, and on which "
             "perimeters Can be useful for art or with high infill/perimeter overlap. The "
             "result may vary between infill types. (connected, holes, outershell, "
             "notconnected; default: connected)",
        default="connected",
    )

    infill_connection_top = fields.Selection(
        selection='_get_connection_selection',
        string="Infill connection top",
        help="Give to the infill algorithm if the infill needs to be connected, and on which "
             "perimeters Can be useful for art or with high infill/perimeter overlap. The "
             "result may vary between infill types. (connected, holes, outershell, notconnected; default: connected)",
        default="connected",
    )

    infill_dense = fields.Boolean(
        string="Infill dense",
        help="Enables the creation of a support layer under the first solid layer. This allows "
             "you to use a lower infill ratio without compromising the top quality. The dense "
             "infill is laid out with a 50% infill density.",
        default=False,
    )

    infill_dense_algo = fields.Selection(
        selection='_get_infill_algo_selection',
        string="Infill dense algo",
        help="Choose the way the dense layer is laid out. The automatic option lets it try to "
             "draw the smallest surface with only strait lines inside the sparse infill. The "
             "Anchored option just slightly enlarges (by 'Default infill margin') the surfaces "
             "that need a better support. (automatic, autosmall, autoenlarged, enlarged; default: autoenlarged)",
        default="autoenlarged",
    )

    infill_every_layers = fields.Integer(
        string="Infill every layers",
        help="This feature allows you to combine infill and speed up your print by extruding "
             "thicker infill layers while preserving thin perimeters, thus accuracy. (layers, default: 1)",
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
        default="111%",
    )

    infill_first = fields.Integer(
        string="Infill first",
        help=" This option will switch the print order of perimeters and infill, making the latter first.",
        default=0,
    )

    infill_only_where_needed = fields.Boolean(
        string="Infill only where needed",
        help="This option will limit infill to the areas actually needed for supporting "
             "ceilings (it will act as internal support material). If enabled, this slows down "
             "the G_code generation due to the multiple checks involved.",
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

    interface_shells = fields.Boolean(
        string="Interface shells",
        help="Force the generation of solid shells between adjacent materials/volumes. Useful "
             "for multi_extruder prints with translucent materials or manual soluble support "
             "material.",
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
        help="This is the rounding error of the input object. It's used to align points that "
             "should be in the same line. Put 0 to disable. (mm, default: 0.0001)",
        default=0.0001,
        digits=(1, 4),
    )

    no_perimeter_unsupported_algo = fields.Selection(
        selection='_get_algo_selection',
        string="No perimeter unsupported algo",
        help="Experimental option to remove perimeters where there is nothing under them and "
             "where a bridged infill should be better. * Remove perimeters: remove the "
             "unsupported perimeters, leave the bridge area as_is. * Keep only bridges: remove "
             "the perimeters in the bridge areas, keep only bridges that end in solid area. * "
             "Keep bridges and overhangs: remove the unsupported perimeters, keep only bridges "
             "that end in solid area, fill the rest with overhang perimeters+bridges. * Fill "
             "the voids with bridges: remove the unsupported perimeters, draw bridges over the "
             "whole hole.* !! this one can escalate to problems with overhangs shaped like /\\, "
             "so you should use it only on one layer at a time via the height_range modifier! "
             "!!Computationally intensive!!. (none, noperi, bridges, bridgesoverhangs, filled; "
             "default: none)",
        default="none",
    )

    notes = fields.Text(
        string="Notes",
        help="",
        default="",
    )

    only_one_perimeter_top = fields.Boolean(
        string="Only one perimeter top",
        help="Use only one perimeter on flat top surface, to give more space to the top infill pattern.",
        default=True,
    )

    only_one_perimeter_top_other_algo = fields.Boolean(
        string="Only one perimeter top other algo",
        help="If you have some problem with the 'Only one perimeter on Top surfaces' option, "
             "you can try to activate this on the problematic layer.",
        default=False,
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
        help="Extrude perimeters that have a part over an overhang in the reverse direction on "
             "odd layers. This alternating pattern can drastically improve steep overhang. !! "
             "this is a very slow algorithm (it uses the same results as extra_perimeters_overhangs) !!",
        default=False,
    )

    overhangs_reverse_threshold = fields.Char(
        string="Overhangs reverse threshold",
        help="Number of mm the overhang need to be for the reversal to be considered useful. "
             "Can be a % of the perimeter width. (default: 250%)",
        default="250%",
    )

    overhangs_speed = fields.Char(
        string="Overhangs speed",
        help="",
        default="100%",
    )

    overhangs_width = fields.Char(
        string="Overhangs width",
        help="Minimum unsupported width for an extrusion to apply the bridge flow to this "
             "overhang. Can be in mm or in a % of the nozzle diameter. Set to 0 to deactivate. (default: 75%)",
        default="75%",
    )

    overhangs_width_speed = fields.Char(
        string="Overhangs width speed",
        help="Minimum unsupported width for an extrusion to apply the bridge fan & overhang "
             "speed to this overhang. Can be in mm or in a % of the nozzle diameter. Set to 0 "
             "to deactivate. (default: 55%)",
        default="55%",
    )

    perimeter_acceleration = fields.Integer(
        string="Perimeter acceleration",
        help="",
        default=0,
    )

    perimeter_bonding = fields.Char(
        string="Perimeter bonding",
        help="This setting may slightly degrade the quality of your external perimeter, in "
             "exchange for a better bonding between perimeters.Use it if you have great "
             "difficulties with perimeter bonding, for example with high temperature "
             "filaments. This percentage is the % of overlap between perimeters, a bit like "
             "perimeter_overlap and external_perimeter_overlap, but in reverse. You have to "
             "set perimeter_overlap and external_perimeter_overlap to 100%, or this setting "
             "has no effect. 0: no effect, 50%: half of the nozzle will be over an already "
             "extruded perimeter while extruding a new one, unless it's an external one). It's "
             "very experimental, please report about the usefulness. It may be removed if "
             "there is no use for it. (%, default: 0%)",
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
        default="116%",
    )

    perimeter_loop = fields.Boolean(
        string="Perimeter loop",
        help="Join the perimeters to create only one continuous extrusion without any z_hop. "
             "Long inside travel (from external to holes) are not extruded to give some space to the infill.",
        default=False,
    )

    perimeter_loop_seam = fields.Selection(
        selection=[("rear", "Rear"), ("hidden", "Nearest")],
        string="Perimeter loop seam",
        help="Position of perimeters starting points. (nearest, rear; default: rear)",
        default="rear",
    )

    perimeter_overlap = fields.Char(
        string="Perimeter overlap",
        help="",
        default="100%",
    )

    perimeter_round_corners = fields.Boolean(
        string="Perimeter round corners",
        help="Internal perimeters will go around sharp corners by turning around instead of "
             "making the same sharp corner. This can help when there are visible holes in "
             "sharp corners on perimeters",
        default=False,
    )

    perimeter_speed = fields.Integer(
        string="Perimeter speed",
        help="",
        default=60,
    )

    perimeters = fields.Integer(
        string="Perimeters",
        help="This option sets the number of perimeters to generate for each layer. Note that "
             "Slic3r may increase this number automatically when it detects sloping surfaces "
             "which benefit from a higher number of perimeters if the Extra Perimeters option "
             "is enabled. ((minimum)., default: 3)",
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
        help="Minimum detail resolution, used to simplify the input file for speeding up the "
             "slicing job and reducing memory usage. High_resolution models often carry more "
             "details than printers can render. Set to zero to disable any simplification and "
             "use full resolution from input. Note: Slic3r has an internal working resolution"
             "of 0.0001mm. Infill & Thin areas are simplified up to 0.0125mm. (mm, default: 0.002)",
        default=0.002,
        digits=(1, 3),
    )

    seam_angle_cost = fields.Char(
        string="Seam angle cost",
        help="Cost of placing the seam at a bad angle. The worst angle (max penalty) is when "
             "it's flat. (%, default: 100%)",
        default="100%",
    )

    seam_position = fields.Selection(
        selection='_get_seam_selection',
        string="Seam position",
        help="Position of perimeters' starting points. (cost, random, aligned, rear; default: cost)",
        default="hidden",
    )

    seam_travel_cost = fields.Char(
        string="Seam travel cost",
        help="Cost of moving the extruder. The highest penalty is when the point is the "
             "furthest from the position of the extruder before extruding the external perimeter (%, default: 100%)",
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
        help="Fill pattern for solid (internal) infill. This only affects the solid "
             "not_visible layers. You should use rectilinear in most cases. You can try "
             "ironing for translucent material. Rectilinear (filled) replaces zig_zag patterns "
             "by a single big line & is more efficient for filling little spaces. (smooth, "
             "rectilinear, rectilineargapfill, monotonic, concentric, concentricgapfill, "
             "hilbertcurve, archimedeanchords, octagramspiral; default: rectilineargapfill)",
        default="rectilineargapfill",
    )

    solid_infill_below_area = fields.Integer(
        string="Solid infill below area",
        help="Force solid infill for regions having a smaller area than the specified threshold. (mm², default: 70)",
        default=70,
    )

    solid_infill_every_layers = fields.Integer(
        string="Solid infill every layers",
        help="This feature allows you to force a solid layer every given number of layers."
             "Zero to disable. You can set this to any value (for example 9999); Slic3r will "
             "automatically choose the maximum possible number of layers to combine according "
             "to nozzle diameter and layer height. (layers, default: 0)",
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
        default="116%",
    )

    solid_infill_speed = fields.Integer(
        string="Solid infill speed",
        help="",
        default=20,
    )

    spiral_vase = fields.Boolean(
        string="Spiral vase",
        help="This feature will raise Z gradually while printing a single_walled object in "
             "order to remove any visible seam. This option requires a single perimeter, no "
             "infill, no top solid layers and no support material. You can still set any "
             "number of bottom solid layers as well as skirt/brim loops. It won't work when "
             "printing more than one single object.",
        default=False,
    )

    standby_temperature_delta = fields.Float(
        string="Standby temperature delta",
        help="Temperature difference to be applied when an extruder is not active. Enables a "
             "full_height 'sacrificial' skirt on which the nozzles are periodically wiped. "
             "(∆°C, default: -5)",
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
        help="Allow outermost perimeter to overlap itself to avoid the use of thin walls. Note "
             "that flow isn't adjusted and so this will result in over_extruding and undefined behavior.",
        default=True,
    )

    thin_perimeters_all = fields.Boolean(
        string="Thin perimeters all",
        help="Allow all perimeters to overlap, instead of just external ones.",
        default=False,
    )

    thin_walls = fields.Boolean(
        string="Thin walls",
        help="Detect single_width walls (parts where two extrusions don't fit and we need to "
             "collapse them into a single trace). If unchecked, Slic3r may try to fit "
             "perimeters where it's not possible, creating some overlap leading to over_extrusion.",
        default=True,
    )

    thin_walls_merge = fields.Boolean(
        string="Thin walls merge",
        help="Allow the external perimeter to merge the thin walls in the path. You can "
             "deactivate this if you are using thin walls as a custom support, to reduce "
             "adhesion a little.",
        default=True,
    )

    thin_walls_min_width = fields.Char(
        string="Thin walls min width",
        help="Minimum width for the extrusion to be extruded (widths lower than the nozzle "
             "diameter will be over_extruded at the nozzle diameter). If expressed as "
             "percentage (for example 110%) it will be computed over nozzle diameter. The "
             "default behavior of PrusaSlicer is with a 33% value. Put 100% to avoid any sort "
             "of over_extrusion. (default: 33%)",
        default="33%",
    )

    thin_walls_overlap = fields.Char(
        string="Thin walls overlap",
        help="Overlap between the thin wall and the perimeters. Can be a % of the external "
             "perimeter width (default 50%) (default: 50%)",
        default="50%",
    )

    thin_walls_speed = fields.Integer(
        string="Thin walls speed",
        help="",
        default=30,
    )

    top_fill_pattern = fields.Selection(
        selection='_get_top_pattern_selection',
        string="Top fill pattern",
        help="Fill pattern for top infill. This only affects the top visible layer, and not "
             "its adjacent solid shells. (rectilinear, monotonicgapfill, monotonic, "
             "concentric, concentricgapfill, hilbertcurve, archimedeanchords, octagramspiral, "
             "sawtooth, smooth, smoothtriple, smoothhilbert; default: monotonic)",
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
        default="111%",
    )

    top_solid_infill_speed = fields.Integer(
        string="Top solid infill speed",
        help="",
        default=15,
    )

    top_solid_layers = fields.Integer(
        string="Top solid layers",
        help="Number of solid layers to generate on top surfaces. (default: 3)",
        default=3,
    )

    top_solid_min_thickness = fields.Float(
        string="Top solid min thickness",
        help="The number of top solid layers is increased above top_solid_layers if necessary"
             "to satisfy minimum thickness of top shell. This is useful to prevent pillowing "
             "effect when printing with variable layer height. (mm, default: 0)",
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
        help="Maximal distance between supports on sparse infill sections. (mm, default: 10)",
        default=10,
    )

    wipe_tower_brim = fields.Char(
        string="Wipe tower brim",
        help="Width of the brim for the wipe tower. Can be in mm or in % of the (assumed) only "
             "one nozzle diameter. (default: 150%)",
        default="150%",
    )

    wipe_tower_no_sparse_layers = fields.Boolean(
        string="Wipe tower no sparse layers",
        help="",
        default=False,
    )

    wipe_tower_rotation_angle = fields.Integer(
        string="Wipe tower rotation angle",
        help="Wipe tower rotation angle with respect to x_axis. (°, default: 0)",
        default=0,
    )

    wipe_tower_width = fields.Integer(
        string="Wipe tower width",
        help="Width of a wipe tower (mm, default: 60)",
        default=60,
    )

    wipe_tower_x = fields.Integer(
        string="Wipe tower x",
        help="X coordinate of the left front corner of a wipe tower (mm, default: 180)",
        default=180,
    )

    wipe_tower_y = fields.Integer(
        string="Wipe tower y",
        help="Y coordinate of the left front corner of a wipe tower (mm, default: 140)",
        default=140,
    )

    xy_inner_size_compensation = fields.Integer(
        string="XY inner size compensation",
        help="The object will be grown/shrunk in the XY plane by the configured value "
             "(negative = inwards, positive = outwards). This might be useful for fine_tuning "
             "sizes. This one only applies to the 'inner' shell of the object (!!! horizontal "
             "holes break the shell !!!) (mm, default: 0)",
        default=0,
    )

    xy_size_compensation = fields.Integer(
        string="XY size compensation",
        help="The object will be grown/shrunk in the XY plane by the configured value "
             "(negative = inwards, positive = outwards). This might be useful for fine_tuning "
             "sizes. This one only applies to the 'exterior' shell of the object. !!! it's "
             "recommended you put the same value into the 'Inner XY size compensation', unless "
             "you are sure you don't have horizontal holes. !!! (mm, default: 0)",
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
        help="When set to a non-zero value this fan speed is used only for external perimeters "
             "(visible ones). Set to 1 to disable the fan. Set to -1 to use the normal fan"
             "speed on external perimeters.External perimeters can benefit from higher fan"
             "speed to improve surface finish, while internal perimeters, infill, etc. benefit"
             "from lower fan speed to improve layer adhesion. (%, default: -1)",
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
        help="Cooling moves are gradually accelerated towards this speed. (mm/s, default: 3.4)",
        default=3.4,
        digits=(1, 1),
    )

    filament_cooling_initial_speed = fields.Float(
        string="Filament cooling initial speed",
        help="Cooling moves are gradually accelerated, starting at this speed. (mm/s, default: 2.2)",
        default=2.2,
        digits=(1, 1),
    )

    filament_cooling_moves = fields.Integer(
        string="Filament cooling moves",
        help="Filament is cooled by being moved back and forth in the cooling tubes. Specify "
             "desired number of these moves. (default: 4)",
        default=4,
    )

    filament_cooling_zone_pause = fields.Integer(
        string="Filament cooling zone pause",
        help="Can be useful to avoid bondtech gears deforming hot tips, but not ordinarily "
             "needed (milliseconds, default: 0)",
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
        help="The speed for loading of a filament into extruder after retraction (this only "
             "applies to the extruder motor). If left as zero, the retraction speed is used. "
             "(mm/s, default: 0)",
        default="",
    )

    filament_diameter = fields.Float(
        string="Filament diameter",
        help="Enter your filament diameter here. Good precision is required, so use a caliper "
             "and do multiple measurements along the filament, then compute the average. (mm, default: 1.75)",
        default=1.75,
        digits=(1, 2),
    )

    filament_dip_extraction_speed = fields.Integer(
        string="Filament dip extraction speed",
        help="Usually not necessary to change this (mm/sec, default: 70)",
        default=70,
    )

    filament_dip_insertion_speed = fields.Integer(
        string="Filament dip insertion speed",
        help="Usually not necessary to change this (mm/sec, default: 33)",
        default=33,
    )

    filament_enable_toolchange_part_fan = fields.Boolean(
        string="Filament enable toolchange part fan",
        help="Experimental setting. May enable the hotend to cool down faster during "
             "toolchanges (default: 0)",
        default=False,
    )

    filament_enable_toolchange_temp = fields.Boolean(
        string="Filament enable toolchange temp",
        help="Determines whether toolchange temperatures will be applied (default: 0)",
        default=False,
    )

    filament_load_time = fields.Integer(
        string="Filament load time",
        help="Time for the printer firmware (or the Multi Material Unit 2.0) to load a new "
             "filament during a tool change (when executing the T code). This time is added to "
             "the total print time by the G_code time estimator. (s, default: 0)",
        default=0,
    )

    filament_loading_speed = fields.Integer(
        string="Filament loading speed",
        help="Speed used for loading the filament on the wipe tower. (mm/s, default: 28)",
        default=28,
    )

    filament_loading_speed_start = fields.Integer(
        string="Filament loading speed start",
        help="Speed used at the very beginning of loading phase. (mm/s, default: 3)",
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
        help="This setting is used to set the maximum speed when extruding inside the wipe "
             "tower (use M220). In %, set 0 to disable and use the Filament type instead. If "
             "disabled, these filament types will have a defaut value of: _ PVA: 80% to 60% _ "
             "SCAFF: 35% _ FLEX: 35% _ OTHERS: 100% Note that the wipe tower reset the speed "
             "at 100% for the unretract in any case. If using marlin, M220 B/R is used to save "
             "the speed override before the wipe tower print. (%, default: 0)",
        default=0,
    )

    filament_melt_zone_pause = fields.Integer(
        string="Filament melt zone pause",
        help="Stay in melt zone for this amount of time before extracting the filament. Not "
             "usually necessary. (milliseconds, default: 0)",
        default=0,
    )

    filament_minimal_purge_on_wipe_tower = fields.Integer(
        string="Filament minimal purge on wipe tower",
        help="After a tool change, the exact position of the newly loaded filament inside the "
             "nozzle may not be known, and the filament pressure is likely not yet stable. "
             "Before purging the print head into an infill or a sacrificial object, Slic3r "
             "will always prime this amount of material into the wipe tower to produce "
             "successive infill or sacrificial object extrusions reliably. (mm³, default: 15)",
        default=15,
    )

    filament_notes = fields.Text(
        string="Filament notes",
        help="",
        default="",
    )

    filament_ramming_parameters = fields.Char(
        string="Filament ramming parameters",
        help="This string is edited by RammingDialog and contains ramming specific parameters. "
             "(default: '120 100 6.6 6.8 7.2 7.6 7.9 8.2 8.7 9.4 9.9 10.0| 0.05 6.6 0.45 6.8 "
             "0.95 7.8 1.45 8.3 1.95 9.7 2.45 10 2.95 7.6 3.45 7.6 3.95 7.6 4.45 7.6 4.95 7.6')",
        default="120 100 6.6 6.8 7.2 7.6 7.9 8.2 8.7 9.4 9.9 10.0| 0.05 6.6 0.45 6.8 0.95 7.8 1.45 8.3 1.95 9.7 2.45 "
                "10 2.95 7.6 3.45 7.6 3.95 7.6 4.45 7.6 4.95 7.6",
    )

    filament_retract_before_travel = fields.Char(
        string="Filament retract before travel",
        help="Retraction is not triggered when travel moves are shorter than this length. (mm, default: 2)",
        default="",
    )

    filament_retract_before_wipe = fields.Char(
        string="Filament retract before wipe",
        help="With bowden extruders, it may be wise to do some amount of quick retract before "
             "doing the wipe movement. (%, default: 0%)",
        default="",
    )

    filament_retract_layer_change = fields.Boolean(
        string="Filament retract layer change",
        help="This flag enforces a retraction whenever a Z move is done (before it). (default: 0)",
        default=False,
    )

    filament_retract_length = fields.Char(
        string="Filament retract length",
        help="When retraction is triggered, filament is pulled back by the specified amount "
             "(the length is measured on raw filament, before it enters the extruder). (mm "
             "(zero to disable), default: 2)",
        default="",
    )

    filament_retract_lift = fields.Char(
        string="Filament retract lift",
        help="If you set this to a positive value, Z is quickly raised every time a retraction "
             "is triggered. When using multiple extruders, only the setting for the first "
             "extruder will be considered. (mm, default: 0)",
        default="",
    )

    filament_retract_lift_above = fields.Char(
        string="Filament retract lift above",
        help="If you set this to a positive value, Z lift will only take place above the "
             "specified absolute Z. You can tune this setting for skipping lift on the first "
             "layers. (mm, default: 0)",
        default="",
    )

    filament_retract_lift_below = fields.Char(
        string="Filament retract lift below",
        help="If you set this to a positive value, Z lift will only take place below the "
             "specified absolute Z. You can tune this setting for limiting lift to the first "
             "layers. (mm, default: 0)",
        default="",
    )

    filament_retract_restart_extra = fields.Char(
        string="Filament retract restart extra",
        help="When the retraction is compensated after the travel move, the extruder will push "
             "this additional amount of filament. This setting is rarely needed. (mm, default: 0)",
        default="",
    )

    filament_retract_speed = fields.Char(
        string="Filament retract speed",
        help="The speed for retractions (this only applies to the extruder motor). (mm/s, default: 40)",
        default="",
    )

    filament_shrink = fields.Char(
        string="Filament shrink",
        help="Enter the shrinkage percentage that the filament will get after cooling (94% if "
             "you measure 94mm instead of 100mm). The part will be scaled in xy to compensate."
             "Only the filament used for the perimeter is taken into account. Be sure to allow "
             "enough space between objects, as this compensation is done after the checks. (%, default: 100%)",
        default="100%",
    )

    filament_skinnydip_distance = fields.Integer(
        string="Filament skinnydip distance",
        help="For stock extruders, usually 40_42mm. For bondtech extruder upgrade, usually "
             "30_32mm. Start with a low value and gradually increase it until strings are "
             "gone. If there are blobs on your wipe tower, your value is too high. (mm, default: 31)",
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
        help="Time to wait after the filament is unloaded. May help to get reliable "
             "toolchanges with flexible materials that may need more time to shrink to "
             "original dimensions. (s, default: 0)",
        default=0,
    )

    filament_toolchange_part_fan_speed = fields.Integer(
        string="Filament toolchange part fan speed",
        help="Experimental setting. Fan speeds that are too high can clash with the hotend's "
             "PID routine. (%, default: 50)",
        default=50,
    )

    filament_toolchange_temp = fields.Integer(
        string="Filament toolchange temp",
        help="To further reduce stringing, it can be helpful to set a lower temperature just "
             "prior to extracting filament from the hotend. (°C, default: 200)",
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
        help="Time for the printer firmware (or the Multi Material Unit 2.0) to unload a "
             "filament during a tool change (when executing the T code). This time is added to "
             "the total print time by the G_code time estimator. (s, default: 0)",
        default=0,
    )

    filament_unloading_speed = fields.Integer(
        string="Filament unloading speed",
        help="Speed used for unloading the filament on the wipe tower (does not affect initial "
             "part of unloading just after ramming). (mm/s, default: 90)",
        default=90,
    )

    filament_unloading_speed_start = fields.Integer(
        string="Filament unloading speed start",
        help="Speed used for unloading the tip of the filament immediately after ramming. (mm/s, default: 100)",
        default=100,
    )

    filament_use_fast_skinnydip = fields.Boolean(
        string="Filament use fast skinnydip",
        help="Experimental: drops nozzle temperature during cooling moves instead of prior to "
             "extraction to reduce wait time. (default: 0)",
        default=False,
    )

    filament_use_skinnydip = fields.Boolean(
        string="Filament use skinnydip",
        help="Skinnydip performs a secondary dip into the meltzone to burn off fine strings of filament (default: 0)",
        default=False,
    )

    filament_wipe = fields.Boolean(
        string="Filament wipe",
        help="This flag will move the nozzle while retracting to minimize the possible blob on "
             "leaky extruders. (default: 0)",
        default=False,
    )

    filament_wipe_advanced_pigment = fields.Float(
        string="Filament wipe advanced pigment",
        help="The pigment % for this filament (bewteen 0 and 1, 1=100%). 0 for "
             "translucent/natural, 0.2_0.5 for white and 1 for black. (default: 0.5)",
        default=0.5,
        digits=(1, 1),
    )

    filament_wipe_extra_perimeter = fields.Char(
        string="Filament wipe extra perimeter",
        help="When the external perimeter loop extrusion ends, a wipe is done, going slightly "
             "inside the print. The number in this settting increases the wipe by moving the "
             "nozzle along the loop again before the final wipe. (mm, default: 0)",
        default="",
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
        help="Fan speed will be ramped up linearly from zero at layer "
             "'disable_fan_first_layers' to maximum at layer 'full_fan_speed_layer'. "
             "'full_fan_speed_layer' will be ignored if lower than 'disable_fan_first_layers', "
             "in which case the fan will be running at maximum allowed speed at layer "
             "'disable_fan_first_layers' + 1. (default: 0)",
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
        help="This G_code will be used as a code for the color change (default: M600)",
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

    end_gcode = fields.Text(
        string="End gcode",
        help="",
        default="M104 S0 ; turn off temperature\nG28 X0  ; home X axis\nM84     ; disable motors\n",
    )

    extra_loading_move = fields.Float(
        string="Extra loading move",
        help="When set to zero, the distance the filament is moved from parking position "
             "during load is exactly the same as it was moved back during unload. When "
             "positive, it is loaded further, if negative, the loading move is shorter than "
             "unloading. (mm, default: _2)",
        default=-2,
        digits=(1, 0),
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
        help="Distance of the extruder tip from the position where the filament is parked when "
             "unloaded. This should match the value in printer firmware. (mm, default: 92)",
        default=92,
    )

    pause_print_gcode = fields.Text(
        string="Pause print gcode",
        help="This G_code will be used as a code for the pause print (default: M601)",
        default="M601",
    )

    printer_notes = fields.Text(
        string="Printer notes",
        help="",
        default="",
    )

    printer_technology = fields.Char(
        string="Printer technology",
        help="",
        default="FFF",
    )

    remaining_times = fields.Boolean(
        string="Remaining times",
        help="",
        default=False,
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
        help="This G_code will be used as a custom code",
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
        help="Allow Slic3r to compute the purge volume via smart computations. Use the "
             "pigment% of each filament and following parameters",
        default=0,
    )

    wipe_advanced_algo = fields.Char(
        string="Wipe advanced algo",
        help="Algorithm for the advanced wipe. Linear : volume = nozzle + volume_mult * "
             "(pigmentBefore_pigmentAfter) Quadratic: volume = nozzle + volume_mult * "
             "(pigmentBefore_pigmentAfter)+ volume_mult * (pigmentBefore_pigmentAfter)^3 "
             "Hyperbola: volume = nozzle + volume_mult * (0.5+pigmentBefore) / "
             "(0.5+pigmentAfter) (linear, quadra, expo; default: linear)",
        default="linear",
    )

    wipe_advanced_multiplier = fields.Integer(
        string="Wipe advanced multiplier",
        help="The volume multiplier used to compute the final volume to extrude by the "
             "algorithm. (mm3, default: 60)",
        default=60,
    )

    wipe_advanced_nozzle_melted_volume = fields.Integer(
        string="Wipe advanced nozzle melted volume",
        help="The volume of melted plastic inside your nozzle. Used by 'advanced wiping'. (mm3, default: 120)",
        default=120,
    )

    z_offset = fields.Integer(
        string="Z offset",
        help="",
        default=0,
    )

    z_step = fields.Float(
        string="Z step",
        help="Set this to the height moved when your Z motor (or equivalent) turns one step.If "
             "your motor needs 200 steps to move your head/plater by 1mm, this field should be "
             "1/200 = 0.005. Note that the gcode will write the z values with 6 digits after "
             "the dot if z_step is set (it's 3 digits if it's disabled). Put 0 to disable. "
             "(mm, default: 0.005)",
        default=0.005,
        digits=(1, 3),
    )

    extruders = fields.One2many(
        comodel_name="slicing.extruder",
        inverse_name="profile",
        string="Extruders",
        default=lambda self: self.env['slicing.extruder'],
    )
