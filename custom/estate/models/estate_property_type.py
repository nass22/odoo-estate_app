from ast import Try
from odoo import models, fields

class Type(models.Model):
    _name="estate.property.type"
    _description = "Property Type Model"

    name = fields.Char(required=True)