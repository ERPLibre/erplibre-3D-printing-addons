import mimetypes

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.mimetypes import guess_mimetype


class Profile3DSale(models.Model):
    # _name = "p3d.profile_sale"
    _inherit = "sale.order"
    # _description = "3D Model file to slice"

    model_file = fields.Binary(
        string="Model file",
        help="The Model file to slice (STL, OBJ, AMF)",
        attachment=True,
        required=True,
    )

    print_time = fields.Char(
        string="Estimated print time",
        help="This is the estimated printing time from the G-Code",
    )

    @api.onchange("model_file")
    def onchange_file(self):
        file = self.model_file
        file_type = guess_mimetype(file)
        if file_type is None:
            raise ValidationError("Unknown file type.")
        else:
            if mimetypes.guess_extension(file) not in [".stl", ".obj", ".amf"]:
                raise ValidationError(
                    "The file type is incorrect. Please choose an STL or an"
                    " OBJ or an AMF file!"
                )

    @api.model
    def website_check_file(self, filename):
        if mimetypes.guess_extension(filename) not in [".stl", ".obj", ".amf"]:
            return {
                "message": {
                    "type": "error",
                    "info": (
                        "Incorrect file type. Please choose an STL or OBJ or"
                        " AMF file!"
                    ),
                }
            }
