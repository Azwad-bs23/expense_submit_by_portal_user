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

    @http.route('/expense/submission/error', type='http', auth='user', website=True)
    def expense_submission_error(self):
        return request.render("bs_expense_web_form.error_500")

    @http.route('/expense/submit', type='http', auth="public", methods=['POST'])
    def create_expense_with_values(self, **kwargs):
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)]).id
        product_uom = request.env['product.product'].sudo().search(
            [('id', '=', int(kwargs.get('product_id', False)))]).uom_id.id
        values = {
            'name': kwargs.get('description', False),
            'product_id': int(kwargs.get('product_id', False)),
            'date': kwargs.get('expense_date', False),
            'total_amount': kwargs.get('total_expense', False),
            'employee_id': employee,
            'unit_amount': kwargs.get('total_expense', False),
            'product_uom_id': product_uom,
        }
        expense = request.env['hr.expense'].sudo().create(values)
        if expense:
            return request.redirect_query('/expense/submission/successful')
        else:
            return request.redirect_query('/expense/submission/error')

    @http.route('/my_expenses', type='http', auth='user', website=True)
    def my_expenses_list(self):
        expenses = request.env['hr.expense'].sudo().search([('employee_id.user_id', '=', request.env.user.id)])
        total_approved_amount = 0
        total_paid_amount = 0
        total_amount_to_submit = 0
        total_amount_submitted = 0
        total_amount_refused = 0
        for record in expenses:
            if record.state == 'draft':
                total_amount_to_submit += record.total_amount
            elif record.state == 'reported':
                total_amount_submitted += record.total_amount
            elif record.state == 'approved':
                total_approved_amount += record.total_amount
            elif record.state == 'done':
                total_paid_amount += record.total_amount
            elif record.state == 'refused':
                total_amount_refused += record.total_amount
        values = {}
        values.update({'expenses': expenses,
                       'to_submit_amount': total_amount_to_submit,
                       'submitted_amount': total_amount_submitted,
                       'approved_amount': total_approved_amount,
                       'paid_amount': total_paid_amount,
                       'refused_amount': total_amount_refused,
                       })
        return request.render("bs_expense_web_form.my_expenses", values)
