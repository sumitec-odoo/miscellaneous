# Copyright 2025 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Business Unit",
    "summary": "",
    "version": "18.0.1.0.0",
    "category": "Misc",
    "website": "",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "base",
            "sale",
            ],
    "data": [
        'security/ir.model.access.csv',        
        'views/business_unit_st_views.xml',
        'views/sale_order_views.xml',
        'views/res_users_views.xml',
        ],
    "installable": True,
}
