from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"
    _order = "sequence, name"
    property_ids = fields.One2many("estate.property", "property_type_id")

    # SQL CONSTRAINTS
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique!')
    ]

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)