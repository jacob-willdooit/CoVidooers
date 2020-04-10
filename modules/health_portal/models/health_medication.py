from odoo import api, fields, models, _


class HealthMedication(models.Model):
    _name = 'health.medication'
    _description = 'Health Medication'

    name = fields.Char(string='Name', translate=True, required=True)
    active = fields.Boolean(default=True)
