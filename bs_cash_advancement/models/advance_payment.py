# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AdvancePayment(models.Model):
    _name = 'advance.payment'
    _description = ''
    _rec_name = 'name'

    name = fields.Char(string='Name', compute='_compute_name')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', related='employee_id.user_id')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    requested_amount = fields.Float(string="Requested Amount")
    approved_amount = fields.Float(string="Approved Amount")

    @api.depends('employee_id')
    def _compute_name(self):
        for record in self:
            if record.employee_id:
                record.name = 'Advance Payment of %s' % (record.employee_id.name)