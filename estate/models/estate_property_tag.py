from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for property"
    _order = "name asc"

    # SQL CONSTRAINTS
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique!')
    ]

    name = fields.Char(required=True)