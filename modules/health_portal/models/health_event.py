from odoo import api, fields, models, _


class HealthEvent(models.Model):
    _name = 'health.event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Health Event'

    @api.model
    def default_get(self, fields_list):
        res = super(HealthEvent, self).default_get(fields_list)

        res['new_rec'] = not self

        waiting_rooms = self.env['stock.location'].search([('wait_location', '=', True)])
        occupied_beds = self.env['health.patient'].search([('location_id', '!=', False)]).mapped('location_id')
        available_beds = waiting_rooms
        available_beds |= self.env['stock.location'].search(['&', ('bed_location', '=', True), ('id', 'not in', occupied_beds._ids)])

        res['location_allowed'] = [(6, 0, available_beds._ids)]

        res['active'] = True

        return res

    name = fields.Char(string='Description', translate=True)
    active = fields.Boolean(default=True)
    new_rec = fields.Boolean(store=False, readonly=True)
    patient_id = fields.Many2one('health.patient', string='Patient', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={'draft': [('readonly', False)]},
                                 default=lambda self: self.env.company)
    type = fields.Selection(
        [
            ('in_patient', 'In Patient'),
            ('condition', 'Condition'),
            ('treatment', 'Treatment'),
            ('ward', 'Ward'),
            ('out_patient', 'Out Patient'),
        ], string="Event Type", default='in_patient')
    practitioner_ids = fields.Many2many('res.users', column2='user_id', string='Health Practitioners', required=True)
    primary_practitioner_id = fields.Many2one('res.users', string='Primary Practitioner', domain="[('id', 'in', practitioner_ids)]", required=True)
    location_allowed = fields.Many2many('stock.location', compute='_compute_location_allowed')
    location_id = fields.Many2one('stock.location', string='Location', required=True)

    condition_ids = fields.Many2many('health.condition', string='Health Conditions')
    medication_ids = fields.Many2many('health.medication.event', string='Medications')


    def _compute_location_allowed(self):
        waiting_rooms = self.env['stock.location'].search([('wait_location', '=', True)])
        occupied_beds = self.env['health.patient'].search([('location_id', '!=', False)]).mapped('location_id')
        available_beds = waiting_rooms
        available_beds |= self.env['stock.location'].search(['&', ('bed_location', '=', True), ('id', 'not in', occupied_beds._ids)])
        for patient in self:
            patient.location_allowed = available_beds
