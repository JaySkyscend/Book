
from odoo import models , fields , api


class BookInvoice(models.Model):
    _name = 'book.shop.invoice'
    _description = 'Book Invoice'

    name = fields.Char(string='Invoice Number',required=True,copy=False, readonly=True,default="New")
    order_id = fields.Many2one('book.shop.order',string='Book Order',required=True)
    customer_name = fields.Char(string='Customer Name',related='order_id.customer_name',store=True)
    invoice_date = fields.Datetime(string='Invoice Date',default=fields.Datetime.now)
    total_amount = fields.Float(string='Total Amount',related='order_id.total_amount',store=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('paid','Paid'),
    ], default='draft',string='Status')


    @api.model
    def create(self,vals):
        """Generate an Invoice Number when creating an invoice"""
        if vals.get('name','New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('book.shop.invoice') or 'New'
        return super(BookInvoice,self).create(vals)

    def action_mark_paid(self):
        """Mark invoice as paid"""
        self.write({'state':'paid'})

        # Update order state to 'done' when invoice is paid
        if self.order_id:
            self.order_id.write({'state':'done'})

