# -*- coding: utf-8 -*-

from odoo import models, fields


class AdvancePaymentConfiguration(models.Model):
    _name = 'advance.payment.configuration'
    _description = ''
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    STATES = [('draft', 'Draft'), ('confirm', 'Confirmed')]

    name = fields.Char(string='Name')
    state = fields.Selection(selection=STATES, string='Status', default='draft', tracking=True)
    # TODO : A domain will be added in journal id according to need
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal', tracking=True)
    credit_account = fields.Many2one(comodel_name='account.account', string='Credit', tracking=True)
    debit_account = fields.Many2one(comodel_name='account.account', string='Debit', tracking=True)

    def approve_configuration(self):
        return self.write({'state': 'confirm'})
