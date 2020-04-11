{
    'name': 'Health Portal',
    'version': '13.0.0.0',
    'category': 'Medical',
    'summary': 'Health Portal - Patient Management System',
    'website': 'https://github.com/jacob-willdooit/CoVidooers',
    'depends': [
        'stock',
        'uom',
    ],
    'description': """
Health Portal - Patient Management System
=========================================

    """,
    'data': [
        'data/ir_module_category_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/health_condition_views.xml',
        'views/health_event_views.xml',
        # 'views/health_medication_views.xml',
        'views/health_patient_views.xml',
        'views/health_portal_views.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'qweb': [
    ],
    'application': True,
}
