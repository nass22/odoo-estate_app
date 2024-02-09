from odoo import fields, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_property(self):
        res = super().sold_property()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        # FONCTIONNE PAS!
        # journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()

        for prop in self:
            self.env['account.move'].create(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                }
            )

        return res

    