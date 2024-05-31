from odoo import api, fields, models, _


class FleetBranch(models.Model):
    _name = "fleet.branch"
    _description = "Fleet Branch"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    address = fields.Char(string='Address')
    lat = fields.Char(string='Branch Latitude')
    long = fields.Char(string='Branch Longitude')
    erp_code = fields.Char(string='Hub ERP Code', tracking=True)
    manager_email = fields.Char(string='Manager Email', tracking=True)
    fleet_manager_email = fields.Char(string='Fleet Manager Email', tracking=True)
    branch_email = fields.Char(string='Branch Email')

    hub_count = fields.Integer(string='', compute='_compute_hub_count', store=True)
    vehicle_count = fields.Integer(compute='_compute_vehicle_count', store=True)
    hub_ids = fields.One2many(comodel_name='fleet.hub', inverse_name='branch_id', string='Hubs')
    manager = fields.Many2one('res.users', string='Manager Name', tracking=True)
    fleet_manager = fields.Many2one('res.users', string='Fleet Manager Name', tracking=True)


    @api.depends('hub_ids')
    def _compute_hub_count(self):
        for branch in self:
            branch.hub_count = len(branch.hub_ids)

    def _compute_vehicle_count(self):
        for branch in self:
            branch.vehicle_count = self.env['fleet.vehicle'].search_count([
                ('branch_id', '=', branch.id),
            ])

    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_model_hub(self):
        action = self.env.ref('dotpl_fleet.action_fleet_hub').read()[0]
        action['domain'] = [('branch_id', '=', self.id)]
        action['context'] = {'default_branch_id': self.id}
        return action

    def action_model_vehicle(self):
        self.ensure_one()
        view = {
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'res_model': 'fleet.vehicle',
            'name': _('Vehicles'),
            'context': {
                'search_default_branch_id': self.id,
                'default_branch_id': self.id,
            }
        }
        return view
