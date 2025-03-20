
from odoo import models , fields , api
from odoo.exceptions import  ValidationError

class BookInvoice(models.Model):
    _name = 'book.shop.invoice'
    _description = 'Book Invoice'

    name = fields.Char(string='Invoice Number',required=True,copy=False, readonly=True,default="New")
    order_id = fields.Many2one('book.shop.order',string='Book Order',required=True)
    customer_name = fields.Char(string='Customer Name',related='order_id.customer_name',store=True)
    customer_email = fields.Char(string="Customer Email",related="order_id.customer_email",store=True)
    invoice_date = fields.Datetime(string='Invoice Date',default=fields.Datetime.now)
    total_amount = fields.Float(string='Total Amount',related='order_id.total_amount',store=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('paid','Paid'),
    ], default='draft',string='Status')


    # Store book order details
    book_order_lines = fields.One2many('book.shop.order.line',related='order_id.book_order_lines',string="Books")

    @api.model_create_multi
    def create(self,vals_list):
        """Batch create invoices with auto-generated Invoice Number & Paid status"""
        for vals in vals_list:
            if vals.get('name','New') == 'New':
                vals.update({'name':self.env['ir.sequence'].next_by_code('book.shop.invoice') or 'New'})
                #vals['name'] = self.env['ir.sequence'].next_by_code('book.shop.invoice') or 'New'


        invoices =  super(BookInvoice,self).create(vals_list)

        # Automatically mark invoices as Paid and update order state
        # for invoice in invoices:
        #     invoice.write({'state':'paid'})
        #     if invoice.order_id:
        #         invoice.order_id.write({'state':'done'})

        for invoice in invoices:
            # Ensure the order has valid books
            if not invoice.order_id.book_order_lines:
                raise ValidationError("Cannot create an invoice without books in the order!")

            #  check stock before deduction
            for line in invoice.order_id.book_order_lines:
                if line.book_id.stock < line.quantity:
                    raise ValidationError(f"Not enough stock for {line.book_id.name}! Available: {line.book_id.stock}, Required: {line.quantity}")

            # Deduct stock after validation
            for line in invoice.order_id.book_order_lines:
                line.book_id.stock -= line.quantity

            invoice.order_id.write({'state':'done'})  # mark order as done
            invoice.write({'state':'paid'}) # Auto-mark invoice as paid

        return invoices

    def action_mark_paid(self):
        """Manually mark an invoice as Paid"""
        self.write({'state':'paid'})

        # Update order state to 'done' when invoice is paid
        if self.order_id:
            self.order_id.write({'state':'done'})


    def action_print_invoice(self):
        """Generate and Download Invoice PDF"""
        return self.env.ref('book_shop.book_invoice_report_action').report_action(self)

    def action_send_invoice_email(self):
        """ Ask for an email if not available and send invoice"""
        if not self.customer_email:
            raise ValidationError("No email found! Please provide an email for the customer.")

        template = self.env.ref('book_shop.book_invoice_email_template')
        template.send_mail(self.id,force_send=True)

