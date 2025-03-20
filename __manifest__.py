
{
    'name':'Book Shop Management',
    'version':'1.0',
    'summary':'Manage book inventory, authors , and sales',
    'author':'JayPatel',
    'depends': ['sale','mail','base'],
    'data': [
     'security/book_security.xml',
     'security/ir.model.access.csv',
     'views/book_view.xml',
     'views/author_view.xml',
     'views/publisher_view.xml',
     'views/book_shop_menu.xml',
     'views/book_order_views.xml',
     'data/book_order_sequence.xml',
     'views/book_invoice_views.xml',
     'data/book_invoice_sequence.xml',
     #'data/book_invoice_email_template.xml',
     #'report/book_invoice_report.xml',
     'views/book_invoice_template.xml',



    ],


    'installable':True,
    'application':True,
}

