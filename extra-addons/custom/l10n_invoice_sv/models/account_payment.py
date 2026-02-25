# -*- coding: utf-8 -*-

from odoo import models, _, exceptions


class AccountPayment(models.Model):
  _inherit = "account.payment"

  # _get_shared_move_line_vals was removed/changed significantly in Odoo 17.
  # If the PUP (Payment Unique Partner) logic is needed, it should be re-implemented
  # in Odoo 17's _seek_for_lines or similar move synchronization methods.
  """
  def _get_shared_move_line_vals(self, debit, credit, amount_currency, move_id, invoice_id=False):
      ...
  """

