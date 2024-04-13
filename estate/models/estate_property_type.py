from odoo import fields, models

class EstatepropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estateproperty Type Model"
    _order = "sequence,name"

    name = fields.Char('Name',required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1)