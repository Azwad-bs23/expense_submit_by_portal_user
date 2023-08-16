
from odoo import models, fields


class AdvancePaymentConfiguration(models.Model):
    _name = 'advance.payment.configuration'
    _description = ''

    name = fields.Char(string='Name')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal')
    credit_account = fields.Many2one(comodel_name='account.account', string='Credit')
    debit_account = fields.Many2one(comodel_name='account.account', string='Debit')