#-*-conding:utf-8-*-
from odoo import models, fields, api, _

class libro_line(models.Model):
        _name = 'libro.line'
        _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
        _description = "Ventas al contado"
        _order = 'fecha_doc, correlativo, num_doc'

        libro_iva_id = fields.Many2one('libro.iva', 'Referencia de libro', required=True, ondelete='cascade')
        
        company_id = fields.Many2one('res.company', string='Company', change_default=True,
                required=True, readonly=True,
                default=lambda self: self.env.company)

        company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
        
        # comunes
        # type = 
        retenciones = fields.Monetary(_('Retenciones'), store=True, currency_field='company_currency_id')
        totales = fields.Monetary(_('Totales'), store=True, currency_field='company_currency_id')
        #exentas_p = fields.Monetary(_('Ventas Exentas'), store=True, currency_field='company_currency_id', readonly=True)
        exentas_nosujetas = fields.Monetary(_('Ventas Exentas'), store=True, currency_field='company_currency_id')
        correlativo = fields.Char(string=_("No."))
        fecha_doc = fields.Date(string=_('Fecha de Emision'),)
        num_doc = fields.Char(string=_("Numero de Documento"))
        name = fields.Char(string=_("Nombre"))
        nrc = fields.Char(string=_("NRC"))
        nit = fields.Char(string=_("NIT"))
        dui = fields.Char(string=_("DUI"))
        #no_sujetas = fields.Monetary(_('No Sujetas'), store=True, currency_field='company_currency_id', readonly=True)
        #gravadas_p = fields.Monetary(_('Gravadas'), store=True, currency_field='company_currency_id', readonly=True)
        gravadas = fields.Monetary(_('Gravadas'), store=True, currency_field='company_currency_id')
        retenciones = fields.Monetary(_('Impuesto Retenido a Terceros'), store=True, currency_field='company_currency_id')
        
        
        #contribuyente
        prefijo = fields.Char(string=_("Prefijo o Serie"))
        n_form_unico = fields.Char(string=_("No Control Interno Sistema Formulario Unico"))
        debito_fiscal = fields.Monetary(_('Debito Fiscal'), store=True, currency_field='company_currency_id')
        #iva_t = fields.Monetary(_('Debito Fiscal'), store=True, currency_field='company_currency_id', readonly=True)
        
        # compras
        internas_e = fields.Monetary(_('Internas Exentas'), store=True, currency_field='company_currency_id')
        importaciones_e = fields.Monetary(_('Importaciones Exentas'), store=True, currency_field='company_currency_id')
        internas_g = fields.Monetary(_('Internas Gravadas'), store=True, currency_field='company_currency_id')
        importaciones_g = fields.Monetary(_('Importaciones Gravadas'), store=True, currency_field='company_currency_id')
        iva_importacion = fields.Monetary(_('IVA de Importacion'), store=True, currency_field='company_currency_id')
        iva_credito_g = fields.Monetary(_('Credito Fiscal'), store=True, currency_field='company_currency_id')
        percepcion = fields.Monetary(_('Percepciones'), store=True, currency_field='company_currency_id')
        excluidas = fields.Monetary(_('Compraas Excluidas'), store=True, currency_field='company_currency_id')
        
        #consumidor	
        dia = fields.Char(string=_("Dia"))
        num_inicial = fields.Char(string=_("Del No."))
        num_final = fields.Char(string=_("Al No."))
        n_maq_caja = fields.Char(string=_("No. Maquina o Caja Registradora"))
        exportaciones = fields.Monetary(_('Exportaciones'), store=True, currency_field='company_currency_id',)
        v_c_ter = fields.Monetary(_('Ventas por Cuenta de Terceros'), store=True, currency_field='company_currency_id')
        #debito_fiscal = fields.Monetary(_('Debito Fiscal'), store=True, currency_field='company_currency_id', readonly=True)