# -*- coding: utf-8 -*-
{
    'name': "service_mobile",

    'summary': """Mobile webapp for Service technicians""",
    'description': """
        Mobile webapp for creating quotation, sale order, project and invoice for
        a Service technician using his mobile phone.
    """,

    'author': "Vertel AB",
    'website': "https://vertel.se",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.1',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['website','sale_management','hr_timesheet','project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


# {
#     'name': 'Partner vCard',
#     'version': '0.2',
#     'category': '',
#     'description': """
# Electronic business card
# ========================
#
# """,
#     'author': 'Vertel AB',
#     'license': 'AGPL-3',
#     'website': 'http://www.vertel.se',
#     'depends': ['website',],
#     'data': [
#         'views/templates.xml',
#         ],
#     'application': False,
#     'installable': True,
# }
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4: