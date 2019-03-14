# -*- coding: utf-8 -*-
# Copyright © 2019 - All Rights Reserved
# Author      Business SYS Developers México.

from odoo import api, fields, models, tools, conf, _
from odoo.exceptions import Warning, UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    to_make_mrp = fields.Boolean(
        string=_('To make MRP'),
        help="Verified if the product can make mrp order"
    )

    @api.onchange('to_make_mrp')
    def onchange_to_make_mrp(self):
        if self.to_make_mrp:
            if not self.bom_count:
                raise Warning('Please set Bill of Material for this product.')
