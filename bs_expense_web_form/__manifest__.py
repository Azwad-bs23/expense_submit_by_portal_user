# -*- coding: utf-8 -*-
{
    'name': 'Expense web form',
    'description': """
        Portal user will be able to submit his/her expenses through web form in website and a 
        ===================================================
        """,
    'version': '15.0',
    'author': "Brain Station 23 Ltd.",
    'website': "http://brainstation-23.com",
    'category': '',
    'depends': ['hr', 'hr_expense', 'product', 'website', 'portal'],
    'data': [
        'views/hr_employee_views.xml',
        'views/expense_template.xml',
        'views/web_menu.xml',
        'views/expense_submitted_page.xml',
        'views/expenses_in_docs.xml',
        'views/my_expenses_list.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
}