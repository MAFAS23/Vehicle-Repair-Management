{
    'name': 'Gym Management',
    'version': '1.0',
    'summary': 'Aplikasi Manajemen Anggota Gym',
    'description': 'Modul sederhana untuk mengelola anggota dan produk gym',
    'category': 'Services',
    'author': 'Athif',
    'depends': ['base', 'mail', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_member_views.xml',
        'views/gym_product_views.xml',
        'views/gym_invoice_views.xml',
        'views/gym_menu.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}