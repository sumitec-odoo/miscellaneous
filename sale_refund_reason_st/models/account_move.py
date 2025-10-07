from odoo import api, models, fields
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    picking_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Picking Asociado",
        store=True,
        compute="_compute_picking_id",
    )

    picking_reason_id = fields.Many2one(
        'stock.return.picking.reason', 
        string='Motivo devolución',
        related='picking_id.reason_id',
        )

    @api.depends("picking_ids")
    def _compute_picking_id(self):
        for invoice in self:
            # import pdb; pdb.set_trace()
            if len(invoice.picking_ids) >= 1:
                # import pdb; pdb.set_trace()
                invoice.picking_id = invoice.picking_ids[0]
            else:
                invoice.picking_id = False

    def action_post(self):
        for rec in self:
            if rec.move_type == 'out_refund':
                if not rec.reason_id:
                    raise ValidationError('Debe informar el motivo de la nota de crédito')
                    # import pdb; pdb.set_trace()
        
        return super().action_post()