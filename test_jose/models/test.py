from odoo import _, api, models, fields


class Test(models.Model):
    _name = "test"
    _description = "Ceci est un test"

    date = fields.Datetime(help="Ceci est une date")

    name = fields.Char()

    texte = fields.Html(
        string="Description",
        translate=True,
        help="Ceci est du texte",
    )

    valide = fields.Boolean(
        string="Est valide",
        help="Ceci serait valide?",
    )
