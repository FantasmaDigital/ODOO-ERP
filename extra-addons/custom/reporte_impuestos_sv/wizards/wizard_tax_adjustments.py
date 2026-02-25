# -*- coding: utf-8 -*-
# tax.adjustments.wizard was removed in Odoo 17+.
# This wizard is now a standalone TransientModel for El Salvador tax adjustments.
from odoo import api, fields, models


class TaxAdjustmentsSV(models.TransientModel):
    _name = "tax.adjustments.wizard.sv"
    _description = "Ajuste de Impuestos El Salvador"

    reason = fields.Char(string='Motivo', required=True)
    journal_id = fields.Many2one(
        'account.journal', string='Diario', required=True,
        default=lambda self: self.env['account.journal'].search([
            ('type', '=', 'general'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
    )
    date = fields.Date(string='Fecha', required=True, default=fields.Date.context_today)
    debit_account_id = fields.Many2one(
        'account.account', string='Cuenta de Débito', required=True,
    )
    credit_account_id = fields.Many2one(
        'account.account', string='Cuenta de Crédito', required=True,
    )
    tax_id = fields.Many2one(
        'account.tax', string='Impuesto',
    )
    amount = fields.Monetary(string='Importe', required=True)
    currency_id = fields.Many2one(
        'res.currency', string='Moneda',
        default=lambda self: self.env.company.currency_id
    )
    company_id = fields.Many2one(
        'res.company', string='Compañía', ondelete='restrict',
        default=lambda self: self.env.company
    )
    partner_id = fields.Many2one(
        'res.partner', string='Proveedor', ondelete='restrict',
    )

    def action_create_move(self):
        self.ensure_one()
        debit_vals = {
            'name': self.reason,
            'debit': self.amount,
            'credit': 0.0,
            'company_id': self.company_id.id,
            'partner_id': self.partner_id.id,
            'account_id': self.debit_account_id.id,
            'tax_line_id': self.tax_id.id if self.tax_id else False,
        }
        credit_vals = {
            'name': self.reason,
            'debit': 0.0,
            'credit': self.amount,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'account_id': self.credit_account_id.id,
            'tax_line_id': self.tax_id.id if self.tax_id else False,
        }
        vals = {
            'journal_id': self.journal_id.id,
            'date': self.date,
            'ref': self.reason,
            'company_id': self.company_id.id,
            'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
        }
        move = self.env['account.move'].create(vals)
        move.action_post()
        return {'type': 'ir.actions.act_window_close'}
