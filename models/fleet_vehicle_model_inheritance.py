from odoo import api, fields, models, _


# class FleetVehicleModelBrandInheritance(models.Model):
#     _inherit = 'fleet.vehicle.model.brand'
#
#     erp_code = fields.Char(string='Manufacturer ERP Code', help='Manufacturer ERP Code')


class FleetVehicleModelInheritance(models.Model):
    _inherit = 'fleet.vehicle.model'
    # _inherit = ['fleet.vehicle.model', 'mail.thread', 'mail.activity.mixin']

    # erp_code = fields.Char(string='Model ERP Code', help='Model ERP Code')
    fuel_type_id = fields.Many2one(comodel_name='general.entry', string='Fuel Type ',
                                   required=True,
                                   domain=[('type', '=', 'FUEL_TYPE')])
    variant_name = fields.Char('Variant Name', required=True)
    vehicle_group_id = fields.Many2one(comodel_name='fleet.vehicle.group', string='Vehicle Group', required=True)
    model_status = fields.Selection([
        ('A', 'Active'),
        ('I', 'Inactive')
    ], 'Status', default='A', required=True)
    category_id = fields.Many2one('fleet.vehicle.model.category', 'Vehicle Type ', required=True)
    kmpl = fields.Integer('KMPL', required=True)

