# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class PosicionArancelaria(models.Model):
  _name = "posicion.arancel"
  _description = "Tariff Position of Products for Export and Import"
  _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
  
  name = fields.Char(string='Name', required=True, tracking=True)
  porcentaje = fields.Float('Tariff', digits=(5,4), required=True, tracking=True, help="Use decimal point to set percentage")
  description = fields.Text('Description', tracking=True)

  
  @api.constrains('name')
  def _check_name(self):
    for l in self:
      if len(l.search([('name', '=', l.name)])) > 1:
        raise ValidationError("La Posicion Arancelaria %s  Ya Existe" % l.name)
    
  @api.constrains('porcentaje')
  def _check_porcentaje(self):
    for l in self:
      if l.porcentaje > 1:
        raise ValidationError("El Porcentaje no Puede ser mayor a 1 cambiar %s" % l.porcentaje)
      if l.porcentaje < 0:
        raise ValidationError("El Porcentaje no Puede ser menor a 0 cambiar %s" % l.porcentaje)