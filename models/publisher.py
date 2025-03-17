from odoo import models, fields

class Publisher(models.Model):
    _name = 'book.shop.publisher'
    _description = 'Book Publisher'

    name = fields.Char(string='Publisher Name',required=True)
    address = fields.Text(string="Address")
    book_ids = fields.One2many('book.shop.book','publisher_id',string='Books')
