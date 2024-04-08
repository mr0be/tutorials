from odoo import api, fields, models
from datetime import timedelta, date
from odoo.exceptions import UserError, ValidationError

class EstatepropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estateproperty Tag Model"

    price = fields.Float('Price', required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')],
    required=True,copy=False)
    partner_id = fields.Many2one('res.partner', string='Buyer',copy=False, required=True)
    property_id = fields.Many2one('estate.property', string='Estate',copy=False, required=True)
    validity = fields.Integer('Validity', default=7, copy=False)
    date_deadline = fields.Datetime('Deadline', copy=False,compute='_compute_validity',inverse='_inverse_deadline')


    _sql_constraints = [
        ('estate_property_offer_check_price', 'CHECK(price > 0)',
         'an offer price must be strictly positive')
    ]


    @api.depends('create_date','validity')
    def _inverse_deadline(self):
        for record in self:
            date2 = record.create_date
            date1 = record.date_deadline
            if date2 > date1:   
                record.validity =  (date2-date1).days
            else:
                record.validity = (date1-date2).days
     
    @api.depends('create_date','validity')
    def _compute_validity(self):
        for record in self:
            if record.create_date:
                record.date_deadline =  record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline =  date.today() + timedelta(days=record.validity)
    
     
    def action_refuse(self):
        for record in self:
            record.status = 'refused'

        return True

     
    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold' :
                raise UserError("has already been sold")
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.state = 'sold'
            record.property_id.partner_id = record.partner_id
        return True