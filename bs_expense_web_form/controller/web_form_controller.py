# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    @http.route('/expense', type='http', auth='user', website=True)
    def expense_website_form(self):
        products = request.env['product.product'].sudo().search([('can_be_expensed', '=', True)])
        values = {}
        values.update({'products': products})
        return request.render("bs_expense_web_form.expense", values)

    @http.route('/expense/submission/successful', type='http', auth='user', website=True)
    def expense_submission_successful(self):
        return request.render("bs_expense_web_form.expense_submission_successful")

    @http.route('/expense/submit', type='http', auth="public", methods=['POST'])
    def create_expense_with_values(self, **kwargs):
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)]).id
        values = {
            'name': kwargs.get('description', False),
            'product_id': int(kwargs.get('product_id', False)),
            'date': kwargs.get('expense_date', False),
            'total_amount': kwargs.get('total_expense', False),
            'employee_id': employee,
            'unit_amount': 1,
        }
        expense = request.env['hr.expense'].sudo().create(values)
        if expense:
            return request.redirect_query('/expense/submission/successful')
        else:
            # TODO : here new message will be shown "Something went wrong! please submit your expense again"
            return True

    @http.route('/my_expenses', type='http', auth='user', website=True)
    def my_expenses_list(self):
        expenses = request.env['hr.expense'].sudo().search([('employee_id.user_id', '=', request.env.user.id)])
        values = {}
        values.update({'expenses': expenses})
        return request.render("bs_expense_web_form.my_expenses", values)

    @http.route('/advance-payment/request', type='http', auth='user', website=True)
    def advance_payment_request_website_form(self):
        currency_ids = request.env['res.currency'].sudo().search([])
        payment_types = request.env['advance.payment.configuration'].sudo().search([('state', '=', 'confirm')])
        values = {}
        values.update({'currency': currency_ids, 'payments' : payment_types})
        return request.render("bs_expense_web_form.advance_payment_request", values)

