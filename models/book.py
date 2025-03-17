from odoo import models, fields

class Book(models.Model):
    _name = 'book.shop.book'
    # technical name of the model
    _description = 'Book Details'

    name = fields.Char(string='Title',required=True)
    author_id = fields.Many2one('book.shop.author',string='Author')
    publisher_id = fields.Many2one('book.shop.publisher',string='Publisher')
    price = fields.Float(string='Price',required=True)
    stock = fields.Integer(string='Stock',default=0)
    isbn = fields.Char(string='ISBN',required = True)


