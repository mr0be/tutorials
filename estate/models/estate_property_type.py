from odoo import fields, models

class EstatepropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estateproperty Type Model"

    name = fields.Char('Name',required=True)