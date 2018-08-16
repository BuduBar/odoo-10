# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, conf
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    location_mrp_origin_id = fields.Many2one('stock.location', 'Origin Location')
    location_mrp_destination_id = fields.Many2one('stock.location', 'Destination Location')