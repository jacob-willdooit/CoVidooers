from odoo import api, fields, models, _


class Location(models.Model):
    _inherit = 'stock.location'

    bed_location = fields.Boolean('Is a Bed Location?', default=False)
    wait_location = fields.Boolean('Is a Waiting Location?', default=False)
    ward_location = fields.Boolean('Is a Ward Location?', default=False)
    room_location = fields.Boolean('Is a Room Location?', default=False)
    patient_id = fields.Many2one('health.patient', string='Patient')
    less_half_full_room = fields.Boolean(compute='_compute_room_full', store=True, readonly=True)
    full_room = fields.Boolean(compute='_compute_room_full', store=True, readonly=True)

    @api.depends('room_location', 'child_ids', 'child_ids.patient_id')
    def _compute_room_full(self):
        for location in self:
            if location.room_location and location.child_ids:
                pass
                if (len(location.child_ids.mapped('patient_id')) / len(location.child_ids)) <= 0.5:
                    location.less_half_full_room = True
                    location.full_room = False
                elif (len(location.child_ids.mapped('patient_id')) / len(location.child_ids)) > 0.8:
                    location.less_half_full_room = False
                    location.full_room = True
            else:
                location.less_half_full_room = False
                location.full_room = False
