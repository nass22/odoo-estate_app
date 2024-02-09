from odoo import fields, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_property(self):
        print(super().sold_property)
    