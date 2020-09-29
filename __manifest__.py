# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Invoicing - add approval steps',
    'version' : '1.1',
    'depends' : ['account'],
    'data': [
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        ],
    'installable': True,
    'application': False,
    'auto_install': False
}
