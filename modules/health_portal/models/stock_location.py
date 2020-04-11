from odoo import api, fields, models, _


class Location(models.Model):
    _inherit = 'stock.location'

    bed_location = fields.Boolean('Is a Bed Location?', default=False)
    wait_location = fields.Boolean('Is a Waiting Location?', default=False)
    ward_location = fields.Boolean('Is a Ward Location?', default=False)
    room_location = fields.Boolean('Is a Room Location?', default=False)
    patient_id = fields.Many2one('health.patient', string='Patient')
