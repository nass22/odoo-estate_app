from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"

    # SQL CONSTRAINTS
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique!')
    ]

    name = fields.Char(required=True)