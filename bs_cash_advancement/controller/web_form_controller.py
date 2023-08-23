# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    @http.route('/advance-payment/request', type='http', auth='user', website=True)
    def advance_payment_request_website_form(self):
        currency_ids = request.env['res.currency'].sudo().search([])
        payment_types = request.env['advance.payment.configuration'].sudo().search([('state', '=', 'confirm')])
        values = {}
        values.update({'currency': currency_ids, 'payments': payment_types})
        return request.render("bs_cash_advancement.advance_payment_request", values)

    @http.route('/cash_advancement/submission/successful', type='http', auth='user', website=True)
    def cash_advancement_submission_successful(self):
        return request.render("bs_cash_advancement.advance_cash_submission_successful")

    @http.route('/cash_advancement/submit', type='http', auth="public", methods=['POST'])
    def create_cash_advancement_with_values(self, **kwargs):
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)]).id
        values = {
            'employee_id': employee,
            'currency_id': kwargs.get('currency_id', False),
            'advance_payment_config_id': kwargs.get('payment_id', False),
            'requested_amount': kwargs.get('requested_amount', False),
            'state': 'requested',
            'approved_amount': 0.0,
        }
        expense = request.env['advance.payment'].sudo().create(values)
        if expense:
            return request.redirect_query('/cash_advancement/submission/successful')
        else:
            # TODO : here new message will be shown "Something went wrong! please submit your expense again"
            return True

    @http.route('/my_cash_advancement', type='http', auth='user', website=True)
    def my_cash_advancement(self):
        advancement = request.env['advance.payment'].sudo().search([('employee_id.user_id', '=', request.env.user.id)])
        values = {}
        values.update({'advancement': advancement})
        return request.render("bs_cash_advancement.my_cash_advancement", values)
