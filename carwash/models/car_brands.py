# -*- coding: utf-8 -*-
# Made in Busissnesys. Author: JO Carrizoza

from odoo import api, fields, models, _

class CarBrands(models.Model):
    _name = 'car.brands'
    _description = 'The car Brands'
    _rec_name = 'name'

    brand_logo = fields.Binary('Logo')
    name = fields.Char('Brands', size=30, help="All car Brands")
    slug = fields.Char('Slug', size=30, help='Slug of the brand')
    models_ids = fields.One2many('car.models', 'brand_id', 'models')

