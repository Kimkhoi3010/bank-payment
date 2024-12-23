# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    selected_for_payment = fields.Boolean("To Pay")

    def action_toggle_select_for_payment(self):
        selected = self.filtered(lambda rec: rec.selected_for_payment)
        unselected = self - selected
        if selected:
            selected.write({"selected_for_payment": False})
        if unselected:
            unselected.write({"selected_for_payment": True})

    def action_register_payment(self):
        active_ids = self.env.context.get("active_ids")
        if active_ids:
            invoices = self.env["account.move"].search(
                [("id", "in", active_ids), ("selected_for_payment", "=", True)]
            )
            invoices.write({"selected_for_payment": False})
        return super().action_register_payment()
