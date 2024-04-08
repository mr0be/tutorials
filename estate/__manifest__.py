{
    'name': "Real Estate",
    'version': '0.1',
    'depends': ['base'],
    'author': "John Doe",
    'category': 'Tutorials/estate',
    'description': """
    Description text
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True
    
}