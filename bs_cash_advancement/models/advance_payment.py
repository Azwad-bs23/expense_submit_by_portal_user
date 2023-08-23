# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.http import request

class AdvancePayment(models.Model):
    _name = 'advance.payment'
    _description = ''
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    STATES = [('draft', 'Draft'), ('requested', 'Requested'), ('approved', 'Approved')]

    name = fields.Char(string='Name', compute='_compute_name')
    state = fields.Selection(selection=STATES, string='Status', default='draft', tracking=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', required=True, store=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', related='employee_id.user_id.partner_id', store=True)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', store=True)
    requested_amount = fields.Float(string="Requested Amount", tracking=True, readonly=True)
    approved_amount = fields.Float(string="Approved Amount", required=True, tracking=True)
    approved_date = fields.Date(string='Approved Date')
    advance_payment_config_id = fields.Many2one(comodel_name='advance.payment.configuration', string='AP Configuration', store=True)
    payment_id = fields.Many2one(comodel_name='account.payment', string='Payment', store=True)

    @api.depends('employee_id')
    def _compute_name(self):
        for record in self:
            if record.employee_id:
                record.name = 'Advance Payment of %s' % (record.employee_id.name)
            else:
                record.name = 'New'

    def request_to_advance_payment(self):
        return self.write({'state': 'requested'})

    def approve_to_advance_payment(self):
        values = {
            'payment_type': 'outbound',
            'partner_id': self.partner_id.id,
            'amount': self.approved_amount,
            'journal_id': self.advance_payment_config_id.journal_id.id,
            'currency_id': self.currency_id.id,
        }
        payment = request.env['account.payment'].sudo().create(values)
        return self.write({'approved_date': date.today(), 'state': 'approved', 'payment_id': payment})
