from odoo import api, fields, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ------------------------------------------------------------
# General Entry
# ------------------------------------------------------------

class GeneralEntry(models.Model):
    _name = "general.entry"
    _description = "General Entry"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name')
    type = fields.Char('Type', required=True, tracking=True)
    text = fields.Char('Text', required=True, tracking=True)
    value = fields.Char('Value', required=True, tracking=True)

    @api.depends('text')
    def _compute_display_name(self):
        for record in self:
            record.name = record.text
            record.display_name = record.text

# ------------------------------------------------------------
# Fleet State
# ------------------------------------------------------------

class FleetState(models.Model):
    _name = "fleet.state"
    _description = "Fleet State"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # state_id = fields.Integer('State Id')
    name = fields.Char("State Name", required=True, tracking=True)
    state_inv_display_name = fields.Char("State Inv Display Name", tracking=True)
    state_gstin = fields.Char("GSTIN", required=True, tracking=True)
    state_short_code = fields.Char("State Initials", required=True, tracking=True)
    state_gst_code = fields.Char("State GST Code", tracking=True)
    state_gstin_address = fields.Text("GSTIN Address", required=True, tracking=True)
    state_postal_code = fields.Char("GSTIN Postal", required=True, tracking=True)
    billing_add = fields.Text("Billing Address", required=True, tracking=True)
    billing_postal = fields.Char("Billing Postal", required=True, tracking=True)
    # cdat = fields.Datetime('CDAT')
    # mdat = fields.Datetime('MDAT')
    # uidc = fields.Char('UIDC')
    # uidm = fields.Char('UIDM')
    last_inv_no = fields.Integer('Last Invoice No.', tracking=True)
    state_status = fields.Selection([
            ('A', 'Active'),
            ('I', 'Inactive')
    ], 'Status', default='A', required=True, tracking=True)
    inactivation_date = fields.Datetime('Inactivation Datetime', tracking=True)

    @api.onchange('state_status')
    def _onchange_state_status(self):
        record = self
        if record.state_status == 'A':
            record.inactivation_date = False

# ------------------------------------------------------------
# Fleet Branch
# ------------------------------------------------------------

class FleetBranch(models.Model):
    _name = "fleet.branch"
    _description = "Fleet Branch"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # br_id = fields.Integer('')
    name = fields.Char('Branch Name', required=True, tracking=True)
    br_add = fields.Text('Branch Address', tracking=True)
    br_postal = fields.Char('Branch Postal', tracking=True)
    br_status = fields.Selection([
            ('A', 'Active'),
            ('I', 'Inactive')
    ], 'Status', default='A', required=True, tracking=True)
    # uidc = fields.Char('')
    # cdat = fields.Datetime('')
    # uidm = fields.Char('')
    # mdat = fields.Datetime('')
    lut_no = fields.Char('LUT No.', tracking=True)

# ------------------------------------------------------------
# Fleet City
# ------------------------------------------------------------

class FleetCity(models.Model):
    _name = "fleet.city"
    _description = "Fleet City"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # city_id = fields.Integer('')
    name = fields.Char('City Name', required=True, tracking=True)
    city_inv_display_name = fields.Char('City Inv Display Name', tracking=True)
    state_id = fields.Many2one(comodel_name='fleet.state', required=True, string='State', tracking=True)
    city_address = fields.Text('City Address', tracking=True)
    city_postal = fields.Char('City Postal', tracking=True)
    city_lang = fields.Float('City Longitude', tracking=True)
    city_lat = fields.Float('City Latitude', tracking=True)
    city_contact_no = fields.Char('Contact No.', tracking=True)
    city_email1 = fields.Char('Email', tracking=True)
    other_emails = fields.Char('Other Email', tracking=True)
    city_status = fields.Selection([
            ('A', 'Active'),
            ('I', 'Inactive')
    ], 'Status', default='A', required=True, tracking=True)
    inactivation_date = fields.Char('Inactivation Date', tracking=True)
    # cdat = fields.Float('')
    # mdat = fields.Float('')
    # uidm = fields.Char('')
    # uidc = fields.Char('')
    branch_id = fields.Many2one(comodel_name='fleet.branch', required=True, string='Branch', tracking=True)

# ------------------------------------------------------------
# Fleet Garage
# ------------------------------------------------------------

class FleetGarage(models.Model):
    _name = "fleet.garage"
    _description = "Fleet Garage"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # branch_code = fields.Integer('')
    # cdat = fields.Datetime('')
    # mdat = fields.Datetime('')
    # uidc = fields.Char('')
    # uidm = fields.Char('')
    name = fields.Char('Garage Name', required=True, tracking=True)
    garage_display_name = fields.Char('Branch Display Name', tracking=True)
    garage_email = fields.Char('Garage Email', tracking=True)
    garage_mobile = fields.Char('Garage Mobile', tracking=True)
    city_id = fields.Many2one(comodel_name='fleet.city', required=True, string='Garage City', tracking=True)
    default_hub = fields.Selection([
            ('Y', 'Yes'),
            ('N', 'No')
    ], 'Main Garage', default='Y', required=True, tracking=True)
    garage_status = fields.Selection([
            ('Y', 'Yes'),
            ('N', 'No')
    ], 'Garage Status', default='Y', required=True, tracking=True)
    inactivation_date = fields.Datetime('Inactivation Date', tracking=True)
    gps_yn = fields.Selection([
            ('Y', 'Yes'),
            ('N', 'No')
    ], 'GPS', default='Y', required=True, tracking=True)
    offline_days_btc = fields.Integer('BackDate Allowed Days (BTC)', tracking=True)
    offline_days_cc = fields.Integer('BackDate Allowed Days (CC)', tracking=True)
    garage_lat = fields.Float('Garage Latitude', tracking=True)
    garage_long = fields.Float('Garage longitude', tracking=True)
    garage_add = fields.Text('Garage Address', required=True, tracking=True)
    garage_postal = fields.Char('Garage Postal', required=True, tracking=True)

    gst_state_id = fields.Many2one(comodel_name='fleet.state', required=True, string='GST State', tracking=True)
    gst_billing_add_logic = fields.Many2one(comodel_name='general.entry', string='Billing Address Logic',
                                            domain=[('type', '=', 'BILLINGADD')], required=True, tracking=True)
    billing_add = fields.Text('Billing Address', compute='_compute_billing_add', readonly=True)


    @api.depends('gst_state_id', 'gst_billing_add_logic')
    def _compute_billing_add(self):
        for record in self:
            if record.gst_state_id and record.gst_billing_add_logic:
                print(record.gst_billing_add_logic.value)
                if record.gst_billing_add_logic.value == '1':
                    record.billing_add = f"{record.gst_state_id.state_gstin_address} - {record.gst_state_id.state_postal_code}"
                elif record.gst_billing_add_logic.value == '2':
                    record.billing_add = f"{record.gst_state_id.billing_add} - {record.gst_state_id.billing_postal}"
                else:
                    record.billing_add = record.garage_add
            else:
                record.billing_add = False
# class FleetCityGroup(models.Model):
#     _name = "fleet.city.group"
#     _description = "Fleet City Group"
#
#     # id = fields.Integer('')
#     group_id = fields.Integer('')
#     group_name = fields.Char('')
#     city_id = fields.Integer('')
#     group_status = fields.Char('')
#     # cdat = fields.Datetime('')
#     # uidc = fields.Char('')
#     # mdat = fields.Datetime('')
#     # uidm = fields.Char('')

# ------------------------------------------------------------
# Fleet Vehicle Group
# ------------------------------------------------------------

class FleetVehicleGroup(models.Model):
    _name = "fleet.vehicle.group"
    _description = "Fleet Vehicle Group"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # id = fields.Integer('')
    name = fields.Char('Group Name', required=True, tracking=True)
    group_short_code = fields.Char('Group Short Code', required=True, tracking=True)
    group_rank = fields.Integer('Group Rank', required=True, tracking=True)
    group_enabled = fields.Selection([
            ('Y', 'Yes'),
            ('N', 'No')
    ], 'Enabled', default='Y', required=True, tracking=True)
    # cdat = fields.Datetime('')
    # cby = fields.Char('')
    # mdat = fields.Datetime('')
    # mby = fields.Char('')


# class FleetModelAndVariant(models.Model):
#     _name = "fleet.model.and.variant"
#     _description = "Fleet Model and Variant"
#
#     model_id = fields.Integer('')
#     model_name = fields.Char('')
#     variant_name = fields.Char('')
#     manufacturer = fields.Integer('')
#     veh_group = fields.Char('')
#     veh_type = fields.Integer('')
#     fuel_type = fields.Integer('')
#     model_status = fields.Char('')
#     # cdat = fields.Datetime('')
#     # uidc = fields.Char('')
#     # mdat = fields.Datetime('')
#     # uidm = fields.Char('')
#     kmpl = fields.Float('')


# class FleetVehicle(models.Model):
#     _name = "fleet.vehicle"
#     _description = "Fleet Vehicle"
#
#     # id = fields.Integer('')
#     plate_no = fields.Char('')
#     receipt_dt = fields.Datetime('')
#     reg_dt = fields.Datetime('')
#     manufacturer = fields.integer('')
#     model_id = fields.integer('')
#     veh_group = fields.Char('')
#     model_year = fields.Integer('')
#     chasis_no = fields.Char('')
#     engine_no = fields.Char('')
#     managed = fields.Integer('')
#     br_id = fields.Integer('')
#     city_id = fields.integer('')
#     garage_location = fields.Integer('')
#     gps_device = fields.Char('')
#     receipt_odometer = fields.Integer('')
#     veh_status = fields.Char('')
#     current_odometer = fields.Integer('')
#     last_dutyno = fields.Integer('')
#     last_check_out_garage = fields.Integer('')
#     last_checkin_garage = fields.Integer('')
#     current_status = fields.Integer('')
#     # uidc = fields.Char('')
#     # cdat = fields.Datetime('')
#     # uidm = fields.Char('')
#     # mdat = fields.Datetime('')
#     vendor_code = fields.Integer('')

# ------------------------------------------------------------
# Fleet Chauffeur
# ------------------------------------------------------------

class FleetChauffeur(models.Model):
    _name = "fleet.chauffeur"
    _description = "Fleet Chauffeur"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # id = fields.Integer('')
    name = fields.Char('Name', compute='_compute_fullname')
    chf_fname = fields.Char('First Name', required=True, tracking=True)
    chf_lname = fields.Char('Last Name', tracking=True)
    chf_mobile = fields.Char('Mobile No.', tracking=True)
    chf_email = fields.Char('Email', tracking=True)
    br_id = fields.Many2one(comodel_name='fleet.branch', required=True, string='Branch', tracking=True)
    city_id = fields.Many2one(comodel_name='fleet.city', required=True, string='City', tracking=True)
    garage_id = fields.Many2one(comodel_name='fleet.garage', required=True, string='Garage', tracking=True)
    last_check_in_branch = fields.Integer('Last Check-In Branch', tracking=True)
    pv = fields.Selection([
            ('Y', 'Yes'),
            ('N', 'No')
    ], 'Police Verification', default='Y', required=True, tracking=True)
    fadv = fields.Selection([
            ('Y', 'Yes'),
            ('N', 'No')
    ], 'FADV', default='Y', required=True, tracking=True)
    license_no = fields.Char('License No.', tracking=True)
    licence_expiry_date = fields.Date('License Validity', tracking=True)
    chf_doj = fields.Date('Date Of Joining', default=lambda self: datetime.today(), tracking=True)
    chf_dob = fields.Date('Date Of Birth', default=lambda self: (datetime.today() - relativedelta(years=20)).date(), tracking=True)
    # uidc = fields.Char('')
    # cdat = fields.Datetime('')
    # mdat = fields.Datetime('')
    # uidm = fields.Char('')
    chf_status = fields.Selection([
            ('A', 'Active'),
            ('I', 'Inactive')
    ], 'Status', default='A', required=True, tracking=True)

    def _default_general_entry_id(self):
        default_general_entry = self.env['general.entry'].search(['&', ('type', '=', 'FLEET_MANAGED'), ('text', '=', 'Own')], limit=1)
        return default_general_entry.id if default_general_entry else False

    general_entry_id = fields.Many2one(comodel_name='general.entry', required=True, string='Managed',
                                 domain=[('type', '=', 'FLEET_MANAGED')],
                                 default=_default_general_entry_id, tracking=True)
    managed = fields.Char('Managed Value', related='general_entry_id.value', store=True, readonly=True)
    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor', readonly=False, tracking=True)
    device_id = fields.Char('Device Id', tracking=True)
    device_type = fields.Char('Device Type', tracking=True)
    login_otp = fields.Char('Login Otp', tracking=True)
    on_duty = fields.Char('On Duty', tracking=True)
    current_booking_no = fields.Integer('Current Booking No.', tracking=True)
    os_type = fields.Char('OS Type', tracking=True)
    os_version = fields.Char('OS Version', tracking=True)
    device_manufacturer = fields.Char('Device Manufacturer', tracking=True)
    device_model = fields.Char('Device Model', tracking=True)
    android_build_version = fields.Char('Android Build Version', tracking=True)
    app_version = fields.Char('App Version', tracking=True)


    @api.depends('chf_fname', 'chf_lname')
    def _compute_fullname(self):
        for record in self:
            record.name = f"{record.chf_fname or ''} {record.chf_lname or ''}".strip()
