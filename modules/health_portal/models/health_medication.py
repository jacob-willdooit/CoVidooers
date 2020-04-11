from odoo import api, fields, models, _


class HealthMedication(models.Model):
    _name = 'health.medication'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Health Medication'

    name = fields.Char(string='Name', translate=True, required=True)
    active = fields.Boolean(default=True)


class HealthMedicationEvent(models.Model):
    _name = 'health.medication.event'
    _description = 'Medication Event'

    medication_id = fields.Many2one('health.medication', string='Medication')
    dosage_note = fields.Char(string='Dosage Description')
    active = fields.Boolean(default=True)
