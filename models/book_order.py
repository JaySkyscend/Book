
from odoo import models, fields , api , _



class BookOrder(models.Model):
    _name = 'book.shop.order'
    _description = 'Book Order'

    name = fields.Char(string='Order Reference',required=True,copy=False,readonly=True,default="New")
    customer_name = fields.Char(string='Customer Name',required=True)
    order_date = fields.Datetime(string='Order Date',default=fields.Datetime.now)
    book_order_lines = fields.One2many('book.shop.order.line','order_id',string='Books Ordered')
    total_amount = fields.Float(string='Total Amount',compute='_compute_total',store = True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('done','Done')
    ], default='draft',string='Status')

    @api.model
    def create(self,vals):
        """Generate a unique Order Reference when creating a new order"""
        if vals.get('name','New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('book.shop.order') or 'New'
        return super(BookOrder, self).create(vals)

    @api.depends('book_order_lines')
    def _compute_total(self):
        """Compute the total price based on book quantity and price"""
        for order in self:
            order.total_amount = sum(line.book_id.price * line.quantity for line in order.book_order_lines)

    def action_confirm(self):
        """Confirm the book order and reduce stock"""
        for order in self:
            for line in order.book_order_lines:
                if line.book_id.stock < line.quantity:
                    raise ValueError(f"Not enough stock for {line.book_id.name}!")
                line.book_id.stock -= line.quantity
            self.write({'state':'confirmed'})

    def action_done(self):
        """Mark the order as done"""
        self.write({'state':'done'})


class BookOrderLine(models.Model):
    _name = 'book.shop.order.line'
    _description = 'Book Order Line'

    order_id = fields.Many2one('book.shop.order',string='Order Reference',required=True,ondelete='cascade')
    book_id = fields.Many2one('book.shop.book',string='Book',required=True)
    quantity = fields.Integer(string='Quantity',default=1)

