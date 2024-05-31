from odoo import api, fields, models, _


class DocumentType(models.Model):
    _name = "fleet.document.type"
    _description = "Document Type"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Name', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    expire_in_days = fields.Integer(string='Expire in (Days)', default=0, tracking=True)
    reminder_required_in_days = fields.Integer(string='Reminder Required in (Days)', default=0, tracking=True)
    recurring_flag = fields.Boolean(string='Is Recurring?', default=True, help='True means its a "Recurring" document')

    category_id = fields.Many2one('fleet.document.type.category', string='Document Category', required=True)

    @api.onchange('recurring_flag')
    def _onchange_recurring_flag(self):
        if not self.recurring_flag:
            self.expire_in_days = False
            self.reminder_required_in_days = False
