# -*- coding: utf-8 -*-
# This file previously extended account.invoice which no longer exists in Odoo 17+.
# The model has been migrated to account.move.
# The 'active' field used for libro_iva tracking is now added to account.move instead.
from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = "account.move"
    libro_iva_active = fields.Boolean(
        'Libro IVA',
        help='Activo si esta factura ya fue contabilizada en el libro de iva',
        default=True,
    )
