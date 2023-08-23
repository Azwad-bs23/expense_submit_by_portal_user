# -*- coding: utf-8 -*-
{
    'name': 'Advanced Payment',
    'description': """
        """,
    'version': '15.0',
    'author': "Brain Station 23 Ltd.",
    'website': "http://brainstation-23.com",
    'category': '',
    'depends': ['hr', 'hr_expense', 'payment', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/advance_payment_views.xml',
        'views/web_menu.xml',
        'views/advance_payment_configuration_views.xml',
        'views/advance_payment_request.xml',
        'views/advance_cash_submitted_page.xml',
        'views/cash_advancement_in_docs.xml',
        'views/my_cash_advancement_list.xml',

    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
}
