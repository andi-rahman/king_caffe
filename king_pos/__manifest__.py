# -*- coding: utf-8 -*-

{
    "name": "King Q Caffee PoS",
    "version": "14.0.1.0.0",
    'license': 'OPL-1',
    'summary': "POS Lock Paymet",
    'category': 'Point of Sale',
    'author': "GB System",
    'support': 'rahmanandi24@gmail.com',
    "description": """
        """,
    "depends": ['point_of_sale', 'pos_restaurant', 'purchase'],
    "data": [
        'security/ir.model.access.csv',
        'views/pos_order_view.xml',
        'views/product_views.xml',
        'views/pos_config.xml',
    ],
    'qweb': [
        'static/src/xml/ProductScreen/ControlButtons/PrintBar.xml',
        'static/src/xml/Screens/BarScreens.xml',
        'static/src/xml/Screens/KitchenScreens.xml',
        'static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
    ],
}
