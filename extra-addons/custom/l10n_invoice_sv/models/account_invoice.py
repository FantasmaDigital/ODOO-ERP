# -*- coding: utf-8 -*-
import json
from odoo.tools import float_is_zero
from .amount_to_text_sv import to_word
from odoo import api, fields, models, _, exceptions

class AccountInvoice(models.Model):
    _inherit = 'account.move'
    
    inv_refund_id = fields.Many2one('account.move','Factura Relacionada', copy=False, tracking=True)

    state_refund = fields.Selection([
            ('refund','Retificada'),
            ('no_refund','No Retificada'),
        ], string="Retificada", index=True, readonly=True, default='no_refund',
        tracking=True, copy=False)
    
    amount_text = fields.Char(string=_('Amount to text'), store=True, readonly=True,
                               compute='_amount_to_text', tracking=True)
       
    @api.depends('amount_total')
    def _amount_to_text(self):
        for record in self:
            record.amount_text = to_word(record.amount_total)

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
      conf = self.env['ir.config_parameter'].sudo()
      iln_str = conf.get_param('invoice_sv.invoice_line_number', '0')
      iln = int(iln_str)
      ivl = len(self.invoice_line_ids)
      if self.move_type in ['out_invoice','out_refund']:
        if iln > 0 and ivl > iln:
          raise exceptions.ValidationError("No puede Crear facturas con %s lineas"\
                    "el maximo permitido es %s" % (ivl,iln))
      for l in self.invoice_line_ids:
        if len(l.tax_ids) > 1:
          raise exceptions.ValidationError("No puede Crear lineas de facturas con %s impuestos."\
                    "Solo puede colocar un impuesto por producto revisar %s" % (len(l.tax_ids),l.display_name))
    
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        # self.sent = True # 'sent' field might not exist in account.move same as invoice
        
        report = self.journal_id.type_report
        
        if report == 'ccf':
            return self.env.ref('l10n_invoice_sv.report_credito_fiscal').report_action(self)
        if report == 'fcf':
            return self.env.ref('account.account_invoices').report_action(self)
        if report == 'exp':
            return self.env.ref('l10n_invoice_sv.report_exportacion').report_action(self)
        if report == 'ndc':
            return self.env.ref('l10n_invoice_sv.report_ndc').report_action(self)
        if report == 'anu':
            return self.env.ref('account.account_invoice_action_report_duplicate').report_action(self)
        if report == 'axp':
            return self.env.ref('l10n_invoice_sv.report_anul_export').report_action(self)
        
        return self.env.ref('account.account_invoices').report_action(self)
    
    def msg_error(self,campo):
      raise exceptions.ValidationError("No puede emitir un documento si falta un campo Legal "\
                                       "Verifique %s" % campo)
    
    def action_post(self):
        '''validamos que partner cumple los requisitos basados en el tipo
        de documento de la sequencia del diario selecionado'''
        for record in self:
            #si es factura normal
            type_report = record.journal_id.type_report
        
            if type_report == 'ccf':
              if not record.partner_id.parent_id:
                if not record.partner_id.nrc:
                  record.msg_error("N.R.C.")
                if not record.partner_id.nit:
                  record.msg_error("N.I.T.")
                if not record.partner_id.giro:
                  record.msg_error("Giro")
              else:
                if not record.partner_id.parent_id.nrc:
                  record.msg_error("N.R.C.")
                if not record.partner_id.parent_id.nit:
                  record.msg_error("N.I.T.")
                if not record.partner_id.parent_id.giro:
                  record.msg_error("Giro")
        
            if type_report == 'fcf':
              if not record.partner_id.parent_id:          
                if not record.partner_id.nit:
                  record.msg_error("N.I.T.")
                if record.partner_id.company_type == 'person':
                  if not record.partner_id.dui:
                    record.msg_error("D.U.I.")
              else:
                if not record.partner_id.parent_id.nit:
                  record.msg_error("N.I.T.")
                if record.partner_id.parent_id.company_type == 'person':
                  if not record.partner_id.dui:
                    record.msg_error("D.U.I.")
    
            if type_report == 'exp':
                for l in record.invoice_line_ids:
                    if not l.product_id.arancel_id:
                        record.msg_error("Posicion Arancelaria del Producto %s" %l.product_id.name)
        
            #si es retificativa
            if type_report == 'ndc':
              if not record.partner_id.parent_id:
                if not record.partner_id.nrc:
                  record.msg_error("N.R.C.")
                if not record.partner_id.nit:
                  record.msg_error("N.I.T.")
                if not record.partner_id.giro:
                  record.msg_error("Giro")
              else:
                if not record.partner_id.parent_id.nrc:
                  record.msg_error("N.R.C.")
                if not record.partner_id.parent_id.nit:
                  record.msg_error("N.I.T.")
                if not record.partner_id.parent_id.giro:
                  record.msg_error("Giro")
                  
        return super(AccountInvoice, self).action_post()

    # The _get_outstanding_info_JSON method is very complex and overrides a core Odoo method
    # that has likely changed significantly in Odoo 17. 
    # For now, I will comment it out to unblock installation.
    # If the user needs this specific SV logic for outstanding payments, it should be re-implemented
    # following the Odoo 17 pattern for the 'payment_widget' field.
    '''
    def _get_outstanding_info_JSON(self):
        ...
    '''


