# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError

class AccountInvoiceRefund(models.TransientModel):
    """Refunds invoice - TODO: Reimplement using account.move.reversal for Odoo 17"""
    _name = "account.invoice.refund"
    _description = "Legacy Invoice Refund Wizard"

    journal_id = fields.Many2one('account.journal', 'Diario', domain="[('type_report','in',['anu','ndc'])]")
    # sale = fields.Boolean('Es Venta?', compute='_is_sale')
    # ... legacy logic ...
    pass
