from odoo import api, fields, models, _


class ResUsers(models.Model):
    _inherit = "res.users"

    # branch_ids = fields.Many2many('fleet.branch', string='Branch')
    # hub_ids = fields.Many2many('fleet.hub', string='Hub')

    # @api.onchange('branch_ids')
    # def _onchange_branch_ids(self):
    #     if self.branch_ids:
    #         return {
    #             'domain': {
    #                 'hub_ids': [('branch_id', 'in', self.branch_ids.ids)]
    #             }
    #         }
    #     else:
    #         return {
    #             'domain': {
    #                 'hub_ids': []
    #             }
    #         }
    # hub_ids = fields.Many2many('fleet.hub', domain=lambda self: [('branch_id', 'in', self.branch_ids.ids)])
    #
    # @api.onchange('branch_ids')
    # def _onchange_branch_ids(self):
    #     return {
    #         'domain': {'hub_ids': [('branch_id', 'in', self.branch_ids.ids)]}
    #     }
