from odoo import api, fields, models, _


class FleetVehicleInheritance(models.Model):
    _inherit = 'fleet.vehicle'

    vehicle_group_id = fields.Many2one(comodel_name='fleet.vehicle.group', string='Vehicle Group', tracking=True)
    engine_no = fields.Char('Engine No.', required=True, tracking=True)

    def _default_general_entry_id(self):
        default_general_entry = self.env['general.entry'].search(
            ['&', ('type', '=', 'FLEET_MANAGED'), ('text', '=', 'Own')], limit=1)
        return default_general_entry.id if default_general_entry else False

    general_entry_id = fields.Many2one(comodel_name='general.entry', required=True, string='Managed',
                                       domain=[('type', '=', 'FLEET_MANAGED')],
                                       default=_default_general_entry_id, tracking=True)
    managed = fields.Char('Managed Value', related='general_entry_id.value', store=True, readonly=True)
    branch_id = fields.Many2one(comodel_name='fleet.branch', string='Branch', tracking=True)
    city_id = fields.Many2one(comodel_name='fleet.city', string='City', tracking=True)
    garage_id = fields.Many2one(comodel_name='fleet.garage', string='Garage', tracking=True)
    gps_device = fields.Selection([
        ('Y', 'Yes'),
        ('N', 'No')
    ], 'GPS Device', default='N', required=True, tracking=True)

    received_odometer = fields.Float('Received Odometer', tracking=True)
    vehicle_status = fields.Selection([
            ('A', 'Active'),
            ('I', 'Inactive')
    ], 'Status', default='A', required=True, tracking=True)

    last_duty_no = fields.Integer('', required=True, tracking=True)
    last_check_out_garage = fields.Integer('', required=True, tracking=True)
    last_check_in_garage = fields.Integer('', required=True, tracking=True)
    current_status = fields.Integer('Current Status', tracking=True)
    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor', readonly=False, tracking=True)

    # last_odometer = fields.Float('Last Odometer ')
    # def _set_odometer(self):
    #     for record in self:
    #         if record.odometer:
    #             date = fields.Date.context_today(record)
    #             data = {'value': record.odometer, 'date': date, 'vehicle_id': record.id}
    #             self.env['fleet.vehicle.odometer'].create(data)
    # #             # Update the odometer field in fleet.vehicle
    #             record.write({'last_odometer': record.odometer})



