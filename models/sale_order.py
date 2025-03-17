#
# from odoo import models, fields , api
# from odoo.exceptions import ValidationError
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#
#     book_quantities = fields.One2many('sale.order.book','order_id',string="Books Ordered")
#     total_book_price = fields.Float(string="Total Book Price",compute="_compute_total_book_price",store = True)
#
#     @api.depends('book_quantities')
#     def _compute_total_book_price(self):
#         """Compute total price for books in the order"""
#         for order in self:
#             order.total_book_price = sum(line.book_id.price * line.quantity for line in order.book_quantities)
#
#     def action_confirm(self):
#         """Override confirm to reduce stock"""
#         for order in self:
#             for line in order.book_quantities:
#                 if line.book_id.stock < line.quantity:
#                     raise ValidationError(f"Not enough stock for {line.book_id.name}!")
#                 line.book_id.stock -= line.quantity
#         return super(SaleOrder, self).action_confirm()
#
# class SaleOrderBook(models.Model):
#     """Intermediate model to handle book quantities in sale order"""
#     _name = 'sale.order.book'
#     _description = "Books in Sale Order"
#
#     order_id = fields.Many2one('sale.order',string="Sale Order", required=True)
#     book_id = fields.Many2one('book.shop.book',string="Book",required = True)
#     quantity = fields.Integer(string="Quantity",required = True, default=1)
#
#
