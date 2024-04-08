from odoo import fields, models

class EstatepropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estateproperty Tag Model"

    name = fields.Char('Name',required=True)