from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"
    _order = "sequence, name"
    # SQL CONSTRAINTS
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique!')
    ]

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer")

    def _compute_offer(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            
        
        