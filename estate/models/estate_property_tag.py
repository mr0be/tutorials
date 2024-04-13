from odoo import fields, models

class EstatepropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estateproperty Tag Model"
    _order = "name"

    name = fields.Char('Name',required=True)
    color = fields.Integer('Color')