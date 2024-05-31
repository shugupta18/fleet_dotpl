from odoo import api, fields, models, _


class FleetHub(models.Model):
    _name = "fleet.hub"
    _description = "Fleet Hub"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    address = fields.Char(string='Address')
    lat = fields.Char(string='Latitude')
    long = fields.Char(string='Longitude')
    erp_code = fields.Char(string='Hub ERP Code', tracking=True)
    manager_email = fields.Char(string='Manager Email', tracking=True)
    fleet_manager_email = fields.Char(string='Fleet Manager Email', tracking=True)
    email = fields.Char(string='Hub Email')
    operations_email = fields.Char(string='Hub Operations Email')
    fleet_email = fields.Char(string='Hub Fleet Email')

    vehicle_count = fields.Integer(compute='_compute_vehicle_count', store=True)
    branch_id = fields.Many2one('fleet.branch', string="Branch", required=True)
    manager = fields.Many2one('res.users', string='Manager', tracking=True)
    fleet_manager = fields.Many2one('res.users', string='Fleet Manager', tracking=True)

    def _compute_vehicle_count(self):
        for hub in self:
            hub.vehicle_count = self.env['fleet.vehicle'].search_count([
                ('hub_id', '=', hub.id),
            ])

    def action_model_vehicle(self):
        self.ensure_one()
        view = {
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'res_model': 'fleet.vehicle',
            'name': _('Vehicles'),
            'context': {
                'search_default_hub_id': self.id,
                'default_branch_id': self.branch_id.id,
                'default_hub_id': self.id,
            }
        }
        return view
