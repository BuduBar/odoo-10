# -*- coding: utf-8 -*-
# Copyright © 2019 - All Rights Reserved
# Author      Business SYS Developers México.

{
    'name' : 'MRP By product POS',
    'description': 'Create a Order Production by Product to produce and discount of material list',
    'author': 'Business SYS Developers México',    
    'category' : 'Point of Sale',
    'version' : '0.1',
    'depends': [
        'base',
        'point_of_sale',
        'mrp', 
        'stock'
    ],
    'data' : [
        'views/product_template_view.xml',
    ],
    'application': True,
}
