from odoo import api, fields, models, _


class HealthPatient(models.Model):
    _name = 'health.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'

    @api.model
    def default_get(self, fields_list):
        res = super(HealthPatient, self).default_get(fields_list)

        res['new_rec'] = not self

        return res

    partner_id = fields.Many2one('res.partner', string="Contact", required=True)
    partner_image = fields.Image("Image", related="partner_id.image_1920", readonly=True)
    name = fields.Char(related='partner_id.name', store=True, readonly=True)
    display_name = fields.Char(related='partner_id.display_name', store=True, readonly=True)
    active = fields.Boolean(default=True)
    new_rec = fields.Boolean(store=False, readonly=True)
    bio_gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('intersex', 'Intersex'),
        ], string='Biological Gender', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    tod = fields.Datetime(string='Time of Death', group_operator='min')
    exp_out_date = fields.Date(string='Expected Out-Patient Date')
    age = fields.Char(string='Age', compute='_compute_age', store=True, readonly=True)
    barcode = fields.Char(string='Barcode')
    medicare_num = fields.Integer(string='Medicare Number')
    admitted = fields.Boolean(string='Admitted', compute='_compute_admitted', store=True, readonly=True)
    state = fields.Selection(
        [
            ('living', 'Living'),
            ('deceased', 'Deceased'),
        ], string='Status', required=True, default='living')

    event_ids = fields.One2many('health.event', 'patient_id', string='Events')
    condition_ids = fields.One2many('health.condition', compute='_compute_condition_ids')
    medication_ids = fields.One2many('health.medication', compute='_compute_medication_ids')
    location_id = fields.Many2one('stock.location', string='Location', compute='_compute_location_id', store=True, readonly=True)


    @api.depends('event_ids')
    def _compute_location_id(self):
        for patient in self:
            if patient.event_ids:
                last_event = patient.event_ids.sorted('create_date', reverse=True)[-1]
                patient.location_id = last_event.location_id
            else:
                patient.location_id = False

    def _compute_condition_ids(self):
        for patient in self:
            patient.condition_ids = patient.event_ids.condition_ids

    def _compute_medication_ids(self):
        for patient in self:
            patient.medication_ids = patient.event_ids.medication_ids

    # Would need a cron job to call this function each day to update age consistently
    @api.depends('dob')
    def _compute_age(self):
        for patient in self:
            today = fields.Date.context_today(self)
            patient.age = patient.dob and ((today.year - patient.dob.year) - ((today.month, today.day) < (patient.dob.month, patient.dob.day)))

    @api.depends('location_id')
    def _compute_admitted(self):
        for patient in self:
            patient.admitted = patient.location_id and (patient.location_id.usage == 'internal')
