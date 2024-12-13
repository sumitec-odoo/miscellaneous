# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    picking_voucher_id = fields.Many2one(
        'stock.picking.voucher',
        'Remito',
        copy=False,
        ondelete='restrict',
    )