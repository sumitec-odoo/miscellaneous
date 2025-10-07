# Copyright 2025 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Refund Reason",
    "summary": "",
    "version": "18.0.1.0.0",
    "category": "Misc",
    "website": "",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "account",
            "stock_picking_return_reason", # juanp
            "stock_picking_invoice_link", # OCA
            "account_invoice_refund_reason", # OCA
            ],
    "data": [
            'views/account_move_views.xml',
        ],
    "installable": True,
}
