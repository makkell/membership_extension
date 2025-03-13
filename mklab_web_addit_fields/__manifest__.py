# -*- coding: utf-8 -*-
{
    'name': "mklab_web_addit_fields",

    'summary': """
        Модуль, добавляющий ряд полей в контакты и в карточку клиента на web - портале Odoo""",

    'description': """
        Модуль, добавляющий ряд полей в модуль Контакты(res.partner) и Веб-портал (web)
    """,

    'author': "МК.Лаб",
    'website': "https://Inf-centre.ru",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts', 'website_partner'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/portal.xml',
    ],
}
