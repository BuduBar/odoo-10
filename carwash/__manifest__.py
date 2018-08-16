# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CarWash',
    'depends': ['base'],
    'description': """ To implement in anywhere car wash  """,
    'author': 'JO Carrizoza',
    'category' : 'Uncategorized',
    'version' : '0.1',
    'data': [
        #'security/account_asset_security.xml',
        'data/car.brands.csv',
        'data/car.models.csv',
        'views/res_partner_views.xml',
        'views/car_brand_views.xml',
        'views/car_model_views.xml',
        'views/car_color_views.xml'        
    ],
    'application': True,
}
