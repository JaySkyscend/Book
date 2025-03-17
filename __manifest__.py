
{
    'name':'Book Shop Management',
    'version':'1.0',
    'summary':'Manage book inventory, authors , and sales',
    'author':'JayPatel',
    'depends': ['sale'],
    'data': [
     'security/ir.model.access.csv',
     'views/book_view.xml',
     'views/author_view.xml',
     'views/publisher_view.xml',
     'views/book_shop_menu.xml',
     'views/book_order_views.xml',
     'data/book_order_sequence.xml'
    ],
    'installable':True,
    'application':True,
}

