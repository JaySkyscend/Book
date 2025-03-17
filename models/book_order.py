

from odoo import models, fields , api , _



class BookOrder(models.Model):
    _name = 'book.shop.order'
    _description = 'Book Order'

    name = fields.Char(string='Order Reference',required=True,copy=False,readonly=True,default="New")
    customer_name = fields.Char(string='Customer Name',required=True)
    order_date = fields.Datetime(string='Order Date',default=fields.Datetime.now)
    book_ids = fields.Many2many('book.shop.book',string='Books')
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

    @api.depends('book_ids')
    def _compute_total(self):
        """Compute the total price of the selected books"""
        for order in self:
            order.total_amount = sum(book.price for book in order.book_ids)

    def action_confirm(self):
        """Confirm the book order and reduce stock"""
        for order in self:
            for book in order.book_ids:
                if book.stock < 1:
                    raise ValueError(f"Book {book.name} is out of stock!")
                book.stock -= 1
        self.write({'state':'confirmed'})

    def action_done(self):
        """Mark the order as done"""
        self.write({'state':'done'})


