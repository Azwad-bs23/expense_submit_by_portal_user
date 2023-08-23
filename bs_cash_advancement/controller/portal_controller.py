from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CashAdvancementCount(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super(CashAdvancementCount, self)._prepare_home_portal_values(counters)
        cash_advancement_count = request.env['advance.payment'].sudo().search_count([('employee_id.user_id', '=', request.env.user.id)])
        values.update({'cash_advancement_count': cash_advancement_count})
        return values
