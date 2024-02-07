from odoo import api, fields, models
from datetime import timedelta, date
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for property"
    _order = "price desc"

    # SQL CONSTRAINTS
    _sql_constraints = [
        ('check_price', 'CHECK(price>0)', 'The price must be strictly positive!')
    ]

    price = fields.Float("Price", required=True)
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id", store=True, string="Property Type")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
   

    def accept_offer(self):
        if "accepted" in self.mapped("property_id.offer_ids.status"):
            raise UserError("An offer as already accepted!")
        else:
            self.write({"status":"accepted"})
            return self.mapped("property_id").write(
                {
                    "state":"offer_accepted",
                    "selling_price": self.price,
                    "buyer_id": self.partner_id.id
                }
            )

    def reject_offer(self):
        return self.write(
            {
                "status": "refused"
            }
        )


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

    @api.model
    def create(self, vals):
        property_id = vals['property_id']
        property = self.env['estate.property'].browse(property_id)

        if property.offer_ids:
            max_offer = max(property.mapped('offer_ids.price'))

            if float_compare(vals['price'], max_offer, precision_rounding=0.01) <= 0:
                raise UserError("The offer must be higher than %.2f" % max_offer)
            
        property.state = 'offer_received'

        return super().create(vals)