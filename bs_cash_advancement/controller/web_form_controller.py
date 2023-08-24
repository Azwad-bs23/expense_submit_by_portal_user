# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager


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

    @http.route('/cash_advancement/submission/error', type='http', auth='user', website=True)
    def cash_advancement_submission_error(self):
        return request.render("bs_cash_advancement.error_500")

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
            return request.redirect_query('/cash_advancement/submission/error')

    @http.route(['/my_cash_advancement', '/my_cash_advancement/page/<int:page>'], type='http', auth='user',
                website=True)
    def my_cash_advancement(self, page=1, sortby='id',  search="", search_in="All", **kwarg):
        advancement = request.env['advance.payment'].sudo().search([('employee_id.user_id', '=', request.env.user.id)])

        """Get the Sorted List"""
        sorted_advancement_list = {
            'id': {'label': 'Latest', 'order': 'id desc'},
            'currency_id': {'label': 'Currency', 'order': 'currency_id'},
            'advance_payment_config_id': {'label': 'Payment Method', 'order': 'advance_payment_config_id'},
            'requested_amount': {'label': 'Requested Amount', 'order': 'requested_amount desc'},
            'approved_amount': {'label': 'Approved Amount', 'order': 'approved_amount desc'},
            'state': {'label': 'Status', 'order': 'state'}
        }
        default_order_by = sorted_advancement_list[sortby]['order']

        """Get Searched Items"""
        search_advancement_list = {
            'All': {'label': 'All', 'input': 'All', 'domain': [('employee_id.user_id', '=', request.env.user.id)]},
            'Currency': {'label': 'Currency', 'input': 'Currency','domain': [('currency_id', 'ilike', search), ('employee_id.user_id', '=', request.env.user.id)]},
            'Payment Method': {'label': 'Payment Method', 'input': 'Payment Method', 'domain': [('advance_payment_config_id', 'ilike', search), ('employee_id.user_id', '=', request.env.user.id)]},
            'Status': {'label': 'Status', 'input': 'Status', 'domain': [('state', 'ilike', search), ('employee_id.user_id', '=', request.env.user.id)]}
        }
        search_domain = search_advancement_list[search_in]['domain']

        """Return records in Pagination"""
        total_advancement_count = len(advancement.ids)
        page_details = pager(url='/my_cash_advancement',
                             total=total_advancement_count,
                             page=page,
                             url_args={'sortby': sortby, 'search_in': search_in, 'search': search},
                             step=10)

        advancement = advancement.search(search_domain,
                                   limit=10,
                                   order=default_order_by,
                                   offset=page_details['offset'], )

        values = {}
        values.update({'advancement': advancement,
                       'page_name': 'cash_advancement',
                       'pager': page_details,
                       'searchbar_sortings': sorted_advancement_list,
                       'sortby': sortby,
                       'search_in': search_in,
                       'searchbar_inputs': search_advancement_list,
                       'search': search
                       })

        return request.render("bs_cash_advancement.my_cash_advancement", values)
