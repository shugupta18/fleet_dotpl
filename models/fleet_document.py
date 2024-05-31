from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class FleetDocument(models.Model):
    _name = "fleet.document"
    _description = 'Fleet Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id desc'

    # def name_get(self):
    #     return [(record.id, f"{record.document_type_id.name}: {record.issue_date}") for record in self]

    name = fields.Char(string='Document No.', required=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)
    sequence = fields.Integer(string="Sequence", default=10)

    issue_date = fields.Date(string='Issue Date', required=True, tracking=True)
    attachment_data = fields.Binary(string='Attachment')
    attachment_name = fields.Char(string='Attachment Name')
    remarks = fields.Text(string='Remarks')
    tag_ids = fields.Many2many('fleet.document.tag', string='Tags')
    new_flag = fields.Boolean(string='New/Old', default=True, tracking=True, help='True means the document is "New"')
    state = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('renewed', 'Renewed'),
        ('hold', 'Hold'),
    ], string='State', default='active', tracking=True)

    expiry_date = fields.Date(string='Expiry Date', store=True, tracking=True)

    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle', string='Vehicle', required=True, tracking=True)
    license_plate = fields.Char(related='vehicle_id.license_plate')
    model_id = fields.Many2one(related='vehicle_id.model_id')
    # branch_id = fields.Many2one(related='vehicle_id.branch_id')
    # hub_id = fields.Many2one(related='vehicle_id.hub_id')
    document_type_id = fields.Many2one('fleet.document.type', string='Document Type', required=True, tracking=True)
    recurring_flag = fields.Boolean(string='Is Recurring?', related='document_type_id.recurring_flag', store=False)
    category_id = fields.Many2one(string='Document Type Category', related='document_type_id.category_id', store=True)

    _sql_constraints = [
        ('doc_no_uniq', 'unique (name)', "A document number with the same name already exists."),
    ]

    is_near_expiry = fields.Boolean(compute='_compute_is_near_expiry', search='_search_is_near_expiry')

    @api.depends('document_type_id', 'document_type_id.reminder_required_in_days')
    def _compute_is_near_expiry(self):
        print('in compute.....')
        for document in self:
            document.is_near_expiry = False

    def _search_is_near_expiry(self, operator, value):
        query = '''
            SELECT fd.id, fd.document_type_id, fd.state, fd.expiry_date, fdt.id, fdt.reminder_required_in_days
            FROM fleet_document fd
            LEFT JOIN fleet_document_type fdt ON fd.document_type_id = fdt.id
            WHERE fd.state = 'active' AND
                ((CURRENT_DATE BETWEEN fd.expiry_date - INTERVAL '1 day' * fdt.reminder_required_in_days AND fd.expiry_date) OR fd.expiry_date < CURRENT_DATE)
        '''
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        return [('id', 'in', tuple(r[0] for r in res))]

    @api.onchange('issue_date', 'vehicle_id')
    def _onchange_issue_date_vehicle(self):
        if self.issue_date and self.document_type_id and self.document_type_id.expire_in_days:
            self.expiry_date = self.issue_date + relativedelta(days=self.document_type_id.expire_in_days)
        else:
            self.expiry_date = False

    @api.onchange('document_type_id')
    def _onchange_document_type(self):
        if self.document_type_id and not self.document_type_id.recurring_flag:
            self.new_flag = True


    @api.model
    def create_renewed_document(self):
        new_document = self.create({
            'issue_date': fields.Date.today(),
            'expiry_date': fields.Date.today() + relativedelta(days=self.document_type_id.expire_in_days),
            'state': 'active',
            'vehicle_id': self.vehicle_id.id,
            'document_type_id': self.document_type_id.id,
        })
        self.write({'state': 'renewed', 'new_flag': False})
        return new_document

    def action_renew_document(self):
        new_document = self.create_renewed_document()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.document',
            'res_id': new_document.id,
            'view_mode': 'form',
            'view_id': False,
            'target': 'current',
        }

    def copy(self, default=None):
        default = {} if not default else default
        default['name'] = f'{self.name} (copy)'
        return super(FleetDocument, self).copy(default)

