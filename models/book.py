from odoo import models, fields , api

class Book(models.Model):
    _name = 'book.shop.book'
    # technical name of the model
    _description = 'Book Details'

    name = fields.Char(string='Title',required=True)
    author_id = fields.Many2one('book.shop.author',string='Author')
    publisher_id = fields.Many2one('book.shop.publisher',string='Publisher')
    price = fields.Float(string='Price',required=True)
    stock = fields.Integer(string='Stock',default=0)
    isbn = fields.Char(string='ISBN',required = True)
    sales_count = fields.Integer(string="Total Sales",compute="_compute_sales_count",store=True)


    @api.depends('stock')
    def _compute_sales_count(self):
        """Compute total sales for each book"""
        for book in self:
            sales_data = self.env['book.shop.order.line'].read_group(
                [('book_id','=',book.id)],
                ['quantity'],
                      ['book_id']
            )
            book.sales_count = sales_data[0]['quantity'] if sales_data else 0

    @api.model
    def get_best_selling_book(self):
        """Fetch the book with the highest sales"""
        best_seller = self.env['book.shop.order.line'].read_group(
            [('book_id','!=',False)], # Filters out lines without books
             ['book_id','quantity:sum'],
                   ['book_id'],
                   orderby='quantity_sum_desc',
                   limit=1
        )

        if best_seller:
            book = self.env['book.shop.book'].browse(best_seller[0]['book_id'][0])
            return f"Best Selling Book: {book.name} with {best_seller[0]['quantity_sum']} copies sold."
        else:
            return "No Books sold yet."