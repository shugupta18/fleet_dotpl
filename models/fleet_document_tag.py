from odoo import api, fields, models, _


class DocumentTag(models.Model):
    _name = "fleet.document.tag"
    _description = "Fleet Document Tag"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color', default=10)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]
