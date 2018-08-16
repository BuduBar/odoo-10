# -*- coding: utf-8 -*-
# Made in Busissnesys. Author: JO Carrizoza

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    car_brand = fields.Many2one('car.brands', string='Car Brand')
    car_model = fields.Many2one('car.models', string='Car Model')
    car_color = fields.Many2one('car.colors', string='Car Color')
    car_year  = fields.Integer(string='Car Year')
    

    @api.onchange('car_brand')
    def check_change(self):
        model_list = []
        if self.car_brand:
            for model in self.car_brand.models_ids:
                model_list.append(model.id)
            return {
                'domain': { 'car_model': [('id', 'in', model_list)]}
            }
