from odoo import api, models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_bu(self):
        bu = self.env['res.users'].sudo().browse(self.env.user.id).business_unit_st_id
        
        return bu

    business_unit_st_id = fields.Many2one('business.unit.st',string="Unidad de negocio", default=_default_bu)