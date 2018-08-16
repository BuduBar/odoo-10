# -*- coding: utf-8 -*-
# Made in Busissnesys. Author: JO Carrizoza

from odoo import api, fields, models, _

class CarColors(models.Model):
    _name = 'car.colors'
    _description = 'The car Color model'
    _rec_name = 'color'

    color = fields.Char('Color', size=30, help="The car Color model")