# -*- coding: utf-8 -*-
{
    'name': 'Advanced Payment',
    'description': """
        """,
    'version': '15.0',
    'author': "Brain Station 23 Ltd.",
    'website': "http://brainstation-23.com",
    'category': '',
    'depends': ['hr', 'hr_expense', 'payment'],
    'data': [
        'security/ir.model.access.csv',
        'views/advance_payment_views.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
}