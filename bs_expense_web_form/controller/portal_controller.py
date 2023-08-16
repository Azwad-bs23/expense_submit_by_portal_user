from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class ExpenseCount(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super(ExpenseCount, self)._prepare_home_portal_values(counters)
        expense_count = request.env['hr.expense'].sudo().search_count([('employee_id.user_id', '=', request.env.user.id)])
        values.update({'expense_count': expense_count})
        return values
