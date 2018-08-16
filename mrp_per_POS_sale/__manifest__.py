# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Business SYS Developers México.

{
    'name' : 'MRP By product POS',
    'depends' : ['base','point_of_sale'],
    'description': 'Create a Order Production by Product to produce and discount of material list',
    'author': 'JO Carrizoza',    
    'category' : 'Cafes and Restaurants',
    'version' : '0.1',
    'data' : [
        'views/res_company_view.xml',
    ],
    'application': True,
}
