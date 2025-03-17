from odoo import fields, models

class Author(models.Model):
    _name = 'book.shop.author'
    _description = 'Book Author'


    name = fields.Char(string='Author Name',required=True)
    biography = fields.Text(string='Biography')
    book_ids = fields.One2many('book.shop.book','author_id',string='Books')