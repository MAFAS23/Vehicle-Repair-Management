# -*- coding: utf-8 -*-
{
    'name': "vehicle_repair_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_repair_views.xml',
        'views/hr_employee_views.xml',
        'views/service_category_views.xml',
        'views/vehicle_type_views.xml',
        'views/vehicle_brand_views.xml',
        'views/vehicle_part_views.xml',
        'views/vehicle_repair_menus.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
