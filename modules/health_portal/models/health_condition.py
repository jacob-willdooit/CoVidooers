from odoo import api, fields, models, _


class HealthCondition(models.Model):
    _name = 'health.condition'
    _description = 'Health Condition'
    _order = 'started_at desc'

    name = fields.Char(string='Name', translate=True, required=True)
    active = fields.Boolean(default=True)
    type_id = fields.Many2one('health.condition.type', string='Type', required=True)
    started_at = fields.Datetime(string='Started', group_operator='min', default=fields.Datetime.now, required=True)
    ended_at = fields.Datetime(string='Ended', group_operator='min')


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
