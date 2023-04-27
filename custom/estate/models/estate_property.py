from odoo import models, fields
from dateutil.relativedelta import relativedelta

class Property(models.Model):
    _name = "estate.property"
    _description = "Property Model"

    #*** FUNCTIONS ***
    def _new_date_availability(self):
        return fields.Date().today() + relativedelta(months=3)

    #*** FIELDS ***
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: self._new_date_availability())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('north', 'North'), ('south','South'), ('east','East'), ('west','West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        selection = [('new', 'New'), ('offer received','Offer Received'), ('offer accepted','Offer Accepted'), ('sold','Sold'), ('canceled', 'Canceled')],
        default="new",
        copy=False
    )