# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock voucher ST",
    "summary": "",
    "version": "17.0.1.0.0",
    "category": "Stock",
    "website": "",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        # CORE ce
        "stock",
        # adhoc - stock - base para imprimir el remito
        "stock_voucher",
        # OCA - stock-logistics-workflow - incluir los Nro de factura asociados al remito
        # "stock_picking_invoice_link",
        ],
    "data": [
        'views/report_stockpicking.xml',
        'views/stock_picking_views.xml',
        ],
    "installable": True,
}
