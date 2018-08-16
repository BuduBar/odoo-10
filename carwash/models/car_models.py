# -*- coding: utf-8 -*-
# Made in Busissnesys. Author: JO Carrizoza

from odoo import api, fields, models, _


class CarModels(models.Model):
    _name = 'car.models'
    _description = 'The car model'
    _rec_name = 'name'

    model_logo = fields.Binary('Logo')
    name = fields.Char('Model', size=30, help="The car brand models")
    brand_id = fields.Many2one('car.brands', string='Brand')
    slug = fields.Char('Slug', size=30, help='Slug of the brand')