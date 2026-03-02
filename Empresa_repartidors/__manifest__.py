# -*- coding: utf-8 -*-
{
    'name': 'Empresa de repartos',
    'version': '1.0',
    'summary': 'Empresa de repartos.',
    'description': """
        Esto es una empresa de repartos y nada mas
    """,
    'author': 'Alexis',
    'website': 'No hay',
    'category': 'Educativo',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/reparto_views.xml',
        'views/empleado_views.xml',
        'views/vehiculo_views.xml',
        'wizard/wizard_repartos_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}