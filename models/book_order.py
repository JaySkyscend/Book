
from odoo import models, fields , api , _
from odoo.exceptions import ValidationError



class BookOrder(models.Model):
    _name = 'book.shop.order'
    _description = 'Book Order'

    name = fields.Char(string='Order Reference',required=True,copy=False,readonly=True,default="New")
    customer_name = fields.Char(string='Customer Name',required=True)
    customer_email = fields.Char(string='Customer Email',required=True)
    order_date = fields.Datetime(string='Order Date',default=fields.Datetime.now)
    book_order_lines = fields.One2many('book.shop.order.line','order_id',string='Books Ordered')
    total_amount = fields.Float(string='Total Amount',compute='_compute_total',store = True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('done','Done')
    ], default='draft',string='Status')


    invoice_id = fields.Many2one('book.shop.invoice',string="Invoice")

    @api.model
    def create(self,vals):
        """Generate a unique Order Reference when creating a new order"""
        if vals.get('name','New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('book.shop.order') or 'New'

        order = super().create(vals)

        # Automatically create an invoice upon order creation
        invoice  = order.env['book.shop.invoice'].create({
            'order_id':order.id,
            'customer_name':order.customer_name,
            'total_amount':order.total_amount,
        })

        order.invoice_id = invoice.id # link the invoice to the order

        return order

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

            # change order state to 'Confirmed'
            order.write({'state':'confirmed'})



            # Automatically Create Invoice if not already created
            if not order.invoice_id:
                invoice = self.env['book.shop.invoice'].create({
                    'order_id': order.id,
                    'customer_name':order.customer_name,
                    'total_amount': order.total_amount,
                 })

                order.invoice_id = invoice.id

    def action_done(self):
        """Mark the order as done"""
        self.write({'state':'done'})


    # def action_create_invoice(self):
    #     """Manually generate an invoice for the book order"""
    #     for order in self:
    #         if order.invoice_id:
    #             raise ValueError("An invoice has already been generated for this order.")
    #
    #     invoice = self.env['book.shop.invoice'].create({
    #         'order_id':order.id ,
    #         'customer_name':order.customer_name,
    #         'total_amount' : order.total_amount,
    #     })
    #
    #     order.write({'invoice_id':invoice.id})



class BookOrderLine(models.Model):
    _name = 'book.shop.order.line'
    _description = 'Book Order Line'

    order_id = fields.Many2one('book.shop.order',string='Order Reference',required=True,ondelete='cascade')
    book_id = fields.Many2one('book.shop.book',string='Book',required=True)
    quantity = fields.Integer(string='Quantity',default=1)

