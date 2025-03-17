from odoo import models, fields , api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    book_ids = fields.Many2many('book.shop.book',string='Books')

    @api.model
    def create(self,vals):
        order = super(SaleOrder, self).create(vals)
        for book in order.book_ids:
            if book.stock < 1:
                raise ValueError(f"Book {book.name} is out of stock!")
            book.stock -= 1
        return order
