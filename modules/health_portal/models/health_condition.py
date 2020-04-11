from odoo import api, fields, models, _


class HealthCondition(models.Model):
    _name = 'health.condition'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Health Condition'
    _order = 'started_at desc'

    name = fields.Char(string='Name', translate=True, required=True)
    active = fields.Boolean(default=True)
    type_id = fields.Many2one('health.condition.type', string='Type', required=True)
    started_at = fields.Datetime(string='Started', group_operator='min', default=fields.Datetime.now, required=True)
    ended_at = fields.Datetime(string='Ended', group_operator='min')
    state = fields.Selection(
        [
            ('ongoing', 'Ongoing'),
            ('treated', 'Treated'),
            ('terminal', 'Terminal'),
            ('fatal', 'Fatal'),
        ], string='Status', required=True, default='ongoing')
    note = fields.Text(string='Notes')

    medication_ids = fields.Many2many('health.medication.event', string='Medications')


    @api.onchange('state', 'started_at')
    def _onchange_state(self):
        for condition in self:
            if condition.state == 'fatal':
                condition.ended_at == condition.started_at
    
    def write(self, vals):
        res = super(HealthCondition, self).write(vals)
        for condition in self:
            if condition.state == 'fatal':
                patients = self.env['health.patient'].search([(condition, 'in', 'condition_ids')])
                patients.tod = 'deceased'
                patients.tod = condition.ended_at
        return res


class HealthConditionCategory(models.Model):
    _name = 'health.condition.category'
    _description = 'Health Condition Category'

    name = fields.Char(string='Name', translate=True, required=True)
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one('health.condition.category', string='Parent Category')


class HealthConditionType(models.Model):
    _name = 'health.condition.type'
    _description = 'Health Condition Type'

    name = fields.Char(string='Name', translate=True, required=True)
    active = fields.Boolean(default=True)
    category_id = fields.Many2one('health.condition.category', string='Category', required=True)
