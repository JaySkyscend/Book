from V17.odoo17.odoo.tools.populate import compute
from odoo import models, fields , api , exceptions

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    book_ids = fields.Many2many('book.shop.book',string='Books')
    book_quantities = fields.One2many('sale.order.book.line','sale_order_id',string="Book Quantities")
    total_book_price = fields.Float(string="Total Book Price",compute="_compute_total_book_price",store = True)

    @api.depends('book_quantities')
    def _compute_total_book_price(self):
        """Compute total price for books in the order"""
        for order in self:
            order.total_book_price = sum(line.book_id.price * line.quantity for line in order.book_quantities)


