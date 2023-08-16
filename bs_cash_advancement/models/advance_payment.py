# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AdvancePayment(models.Model):
    _name = 'advance.payment'
    _description = ''
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    STATES = [('draft', 'Draft'), ('requested', 'Requested'), ('approved', 'Approved')]

    name = fields.Char(string='Name', compute='_compute_name')
    state = fields.Selection(selection=STATES, string='Status', default='draft', tracking=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', related='employee_id.user_id.partner_id')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    requested_amount = fields.Float(string="Requested Amount")
    approved_amount = fields.Float(string="Approved Amount", tracking=True)
    advance_payment_config_id = fields.Many2one(comodel_name='advance.payment.configuration', string='AP Configuration')
    payment_id = fields.Many2one(comodel_name='account.payment', string='Payment')

    @api.depends('employee_id')
    def _compute_name(self):
        for record in self:
            if record.employee_id:
                record.name = 'Advance Payment of %s' % (record.employee_id.name)
            else:
                record.name = 'New'

    def request_to_advance_payment(self):
        self.write({'state': 'requested'})

    def approve_to_advance_payment(self):
        self.write({'state': 'approved'})
