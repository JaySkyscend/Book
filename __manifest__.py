
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
     'views/sale_order_views.xml',
     'views/book_shop_menu.xml',
    ],
    'installable':True,
    'application':True,
}
