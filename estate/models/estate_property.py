from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    # SQL CONSTRAINTS
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price>0)', 'The selling price must be strictly positive')
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation is used to determinate the orientation of the garden")
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new','New'), ('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'), ('sold','Sold'),('canceled','Canceled')], required=True, copy=False, default='new', string='Status')
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", readonly=True, copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer")



    def sold_property(self):
        if 'canceled' in self.mapped('state'):
            raise UserError("Canceled properties cannot be sold.")
        else:
            self.write({"state": "sold"})
        
    def canceled_property(self):
        if 'sold' in self.mapped('state'):
            raise UserError("Sold properties cannot be canceled.")
        else:
            self.write({"state": "canceled"})

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
        
    @api.constrains('expected_price', 'selling_price')
    def _check_price_difference(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_rounding=0.01) and float_compare(record.selling_price,(record.expected_price/100)*90, precision_rounding=0.01) < 0):
                raise ValidationError("The selling price must be at least 90% of the expected price!")
            
    
    @api.ondelete(at_uninstall=False)
    def _unlik(self):
        for record in self:
            if self.state != "new" or self.state != "canceled":
                raise UserError("Only new and canceled properties can be deleted.")