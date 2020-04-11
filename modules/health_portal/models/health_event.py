from odoo import api, fields, models, _


class HealthEvent(models.Model):
    _name = 'health.event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Health Event'
    _order = 'create_date desc'

    name = fields.Char(string='Description', translate=True, required=True)
    active = fields.Boolean(default=True)
    patient_id = fields.Many2one('health.patient', string='Patient', required=True)
    type = fields.Selection(
        [
            ('in_patient', 'In Patient'),
            ('condition', 'Condition'),
            ('treatment', 'Treatment'),
            ('out_patient', 'Out Patient'),
        ], string="Event Type", default='in_patient')
    practitioner_ids = fields.Many2many('res.users', column2='user_id', string='Health Practitioners', required=True)
    primary_practitioner_id = fields.Many2one('res.users', string='Primary Practitioner', domain="[('id', 'in', practitioner_ids)]", required=True)
    location_id = fields.Many2one('stock.location', string='Location', required=True)

    condition_ids = fields.Many2many('health.condition', string='Health Conditions')
    medication_ids = fields.Many2many('health.medication.event', string='Medications')