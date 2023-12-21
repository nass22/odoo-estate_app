from odoo import api, fields, models
from datetime import timedelta, date

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for property"

    price = fields.Float("Price", required=True)
    status = fields.Selection(string="Status", selection=[('acccepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                date = record.create_date.date()
            else:
                date = fields.Date.today()

            record.date_deadline = date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                date = record.create_date.date()
            else:
                date = fields.Date.today()

            record.validity = (record.date_deadline - date).days