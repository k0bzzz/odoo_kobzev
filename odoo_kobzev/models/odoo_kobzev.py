import random
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class InheritedModel(models.Model):
    _inherit = "sale.order"

    test = fields.Char(
        string="Test",
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    is_new = fields.Integer(default=0)

    @api.onchange('tax_totals', 'date_order')
    def _onchange_tax_totals_and_date_order(self):
        for rec in self:
            if rec.is_new < 2:
                rec.test = random.randint(1, 2 ** 30)
                rec.is_new += 1
            else:
                rec.test = _('%s - %s', format(rec.tax_totals['amount_total'], ',.2f'), rec.date_order.strftime('%d/%m/%Y %H:%M:%S'))

    @api.constrains('test')
    def _check_len_test(self):
        for rec in self:
            if rec.test and len(rec.test) > 50:
                raise ValidationError("Длина текста должна быть меньше 50 символов!")
