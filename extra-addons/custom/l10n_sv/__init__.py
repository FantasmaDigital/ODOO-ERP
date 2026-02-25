# -*- coding: utf-8 -*-
from . import models

from odoo import api, SUPERUSER_ID

def drop_journal(env):
  """
  Este hook intentaba archivar diarios por defecto ('INV', 'BILL'),
  pero falla si tienen asientos contables en borrador.
  Como hemos desactivado la carga de diarios de la localización por incompatibilidad,
  desactivamos también este borrado automático para evitar errores de validación.
  """
  pass
    
    
  '''tax = env['account.tax'].create({
    'chart_template_id': env.ref('sv_coa'),
    'name':"Retencion 1 %",
    'description':"RETENCION 1%",
    'amount': -1,
    'amount_type':"percent",
    'type_tax_use':"sale",
    'account_id': env.ref('iva_retencion'),
    'refund_account_id': env.ref('iva_retencion'),
    #'tag_ids': [(6,0,[env.ref('tax_tag_04')])],
    'tax_group_id': env.ref('tax_group_iva_retencion')
  })
  
  p_fiscal = env['account.fiscal.position.tax'].search([('id','=', env.ref('position_tax_gran_ventas_2'))])
  p_fiscal.write({
    'tax_dest_id':tax})'''
      