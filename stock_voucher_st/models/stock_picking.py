# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def do_print_voucher(self):
        # import pdb; pdb.set_trace()
        '''This function prints the voucher'''
        report = self.env['ir.actions.report'].search(
            [('report_name', '=', 'stock_voucher_st.report_picking')],
            limit=1).report_action(self)
        return report

    def assign_numbers(self, estimated_number_of_pages, book):
        result = super(StockPicking,self).assign_numbers(estimated_number_of_pages, book)

        cantidad_renglones = self.env['stock.book'].browse(self.book_id.id).lines_per_voucher

        if (cantidad_renglones == 0):
            raise UserError("Debe configurar la cantidad de renglones para el talonario.")

        vouchers = self.env['stock.picking.voucher'].search([('picking_id','=',self.id)])

        for voucher in vouchers:
            # movimientos que todavía no tienen remitos asignados
            moves = self.env['stock.move'].search(['&',('picking_id','=',self.id),('picking_voucher_id','=',False)])
            renglon = 0
            # for move in moves.filtered(lambda x: x.quantity_done):
            for move in moves:
                move.write({'picking_voucher_id': voucher.id})
                renglon = renglon + 1
                if renglon >= cantidad_renglones:
                    break
            
        return result

    def clean_voucher_data(self):
        moves = self.env['stock.move'].search([('picking_id','=',self.id)])
        for move in moves:
            move.picking_voucher_id = None
        result = super(StockPicking,self).clean_voucher_data()
