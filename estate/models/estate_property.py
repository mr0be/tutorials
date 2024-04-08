from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import *

class Estateproperty(models.Model):
    _name = "estate.property"
    _description = "Estateproperty Model"

    name = fields.Char('Title',required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Datetime('Availability From', readonly=False,copy=False, default= fields.Datetime.today() + relativedelta(months=+3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', required=False, readonly=True,copy=False)
    bedrooms = fields.Integer('Bedrooms', required=False,default=2)
    living_area = fields.Integer('Living area', required=False)
    facades = fields.Integer('Facades', required=False)
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area (sqm)', required=False)
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'),('west', 'West'),('east', 'East')])
    active = fields.Boolean('Active', default=False)
    state = fields.Selection([('new', 'New'), ('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'),('sold', 'Sold'),('canceled', 'Canceled')],
    default='new',required=True,copy=False)
    property_type_id = fields.Many2one("estate.property.type","Property Types")
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer',copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.Many2many('estate.property.offer', string='Offers')
    
    total_area = fields.Integer('Total Area', required=False, readonly=True,copy=False,compute="_compute_area_total")
    best_price = fields.Float('Best Offer', required=False, readonly=True, copy=False, compute="_compute_best_price")

    _sql_constraints = [
        ('estate_property_check_expected_price', 'CHECK(expected_price > 0)',
         'an offer price must be strictly positive'),
        ('estate_property_check_selling_price', 'CHECK(selling_price > 0)',
         'an offer price must be strictly positive'),
        ('estate_property_check_unique_name', 'unique(name)', 'a property tag name and property type name must be unique')
    ]

    @api.constrains('expected_price','selling_price')
    def _check_selling_price(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_digits=1)) and record.selling_price < record.expected_price:
                percent = int(record.selling_price / record.expected_price * 100)
                if(percent < 90):
                    raise ValidationError("selling price cannot be lower than 90 of the expected price.")



    @api.depends('living_area','garden_area')
    def _compute_area_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            if len(prices) > 0 :
                record.best_price = max(prices)
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = ''
            self.garden_area = 0


    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("cannot sold, because is cancel")
            record.state = 'sold'
        return True
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("cannot cancel, because is sold")
            record.state = 'canceled'
        return True