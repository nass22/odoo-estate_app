from odoo import api, fields, models
from datetime import timedelta, date
from odoo.exceptions import UserError

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