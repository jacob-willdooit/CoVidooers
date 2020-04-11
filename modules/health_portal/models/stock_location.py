from odoo import api, fields, models, _


class Location(models.Model):
    _inherit = 'stock.location'

    bed_location = fields.Boolean('Is a Bed Location?', default=False)
    wait_location = fields.Boolean('Is a Waiting Location?', default=False)
