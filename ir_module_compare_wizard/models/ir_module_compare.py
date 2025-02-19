# Copyright 2024 Unai Beristan, Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.models import expression
from odoo.modules.module import get_module_path
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import check_number, convert2str


class IrModuleImport(models.Model):
    _name = "ir.module.import"
    _inherit = "base.import"
    _description = "Wizard to compare modules"

    import_line_ids = fields.One2many(
        comodel_name="ir.module.import.line",
    )
    module_count = fields.Integer(
        string="# Modules",
        compute="_compute_module_count",
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            module_technical_name = row_values.get(
                _("Technical Name"),
                row_values.get(
                    "Technical Name",
                    row_values.get(_("Module Name"), row_values.get("Module Name", "")),
                ),
            )
            if not module_technical_name:
                return {}
            module_last_version = row_values.get(
                _("Installed Version"),
                row_values.get(
                    "Installed Version",
                    row_values.get(
                        _("Latest Version"), row_values.get("Latest Version", "")
                    ),
                ),
            )
            module_website = row_values.get(_("Website"), row_values.get("Website", ""))
            module_author = row_values.get(_("Author"), row_values.get("Author", ""))
            module_notes = row_values.get(_("Notes"), row_values.get("Notes", ""))
            module_author_generic = row_values.get(
                _("Module Author Generic"), row_values.get("Module Author Generic", "")
            )
            priority = row_values.get(_("Priority"), row_values.get("Priority", 0))
            migrate_module = row_values.get(
                _("Migrate Module"), row_values.get("Migrate Module", True)
            )
            install_module = row_values.get(
                _("Install Module"), row_values.get("Install Module", True)
            )
            log_info = ""
            values.update(
                {
                    "module_technical_name": convert2str(module_technical_name),
                    "module_last_version": convert2str(module_last_version),
                    "module_website": convert2str(module_website),
                    "module_author": convert2str(module_author),
                    "module_notes": convert2str(module_notes),
                    "module_author_generic": convert2str(module_author_generic),
                    "priority": check_number(priority),
                    "migrate_module": bool(migrate_module),
                    "install_module": bool(install_module),
                    "log_info": log_info,
                }
            )
        return values

    def _compute_module_count(self):
        for record in self:
            record.module_count = len(record.mapped("import_line_ids.import_module_id"))

    def button_open_modules(self):
        self.ensure_one()
        modules = self.mapped("import_line_ids.import_module_id")
        action = self.env["ir.actions.actions"]._for_xml_id("base.open_module_tree")
        action["domain"] = expression.AND(
            [[("id", "in", modules.ids)], safe_eval(action.get("domain") or "[]")]
        )
        action["context"] = dict(self._context, create=False)
        return action

    def action_validate(self):
        self.env["ir.module.module"].update_list()
        return super().action_validate()


class IrModuleImportLine(models.Model):
    _name = "ir.module.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import module lines"

    import_id = fields.Many2one(
        comodel_name="ir.module.import",
    )
    import_module_id = fields.Many2one(
        string="Found Module",
        comodel_name="ir.module.module",
    )
    import_module_state = fields.Selection(
        string="Database State",
        related="import_module_id.state",
        store=True,
    )
    installed_version = fields.Char(
        string="Database Version",
        related="import_module_id.installed_version",
        store=True,
    )
    action = fields.Selection(
        selection_add=[("install", "Install"), ("update", "Update")],
        ondelete={"install": "set default", "update": "set default"},
    )
    module_technical_name = fields.Char(
        string="Technical Name",
        # states={"done": [("readonly", True)]},
        required=True,
    )
    module_last_version = fields.Char(
        string="Last Version",
        # states={"done": [("readonly", True)]},
    )
    module_website = fields.Char(
        string="Website",
        # states={"done": [("readonly", True)]},
    )
    module_path = fields.Char(
        string="Path",
        # states={"done": [("readonly", True)]},
    )
    module_author = fields.Char(
        string="Author",
        # states={"done": [("readonly", True)]},
    )
    module_author_generic = fields.Char(
        string="Author Generic",
        # states={"done": [("readonly", True)]},
    )
    module_notes = fields.Char(
        string="Notes",
        # states={"done": [("readonly", True)]},
    )
    migrate_module = fields.Boolean(
        string="Migrate",
        # states={"done": [("readonly", True)]},
        default=True,
    )
    install_module = fields.Boolean(
        string="Review",
        # states={"done": [("readonly", True)]},
        default=False,
    )
    priority = fields.Integer(
        # states={"done": [("readonly", True)]},
    )

    def _action_validate(self):
        self.ensure_one()
        update_values = super()._action_validate()
        log_infos = []
        module, log_info_module = self._check_module()
        if log_info_module:
            log_infos.append(log_info_module)
        path = False
        if module:
            path = get_module_path(self.module_technical_name, display_warning=False)
            if not path:
                log_infos.append(
                    _("Module %(module_name)s not installable")
                    % {
                        "module_name": self.module_technical_name,
                    }
                )
        state = "error" if log_infos else "pass"
        action = "nothing"
        if state != "error":
            action = "update" if module.state == "installed" else "install"
        update_values.update(
            {
                "import_module_id": module and module.id,
                "migrate_module": (
                    False if module and state != "error" else self.migrate_module
                ),
                "module_path": path or "",
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _check_module(self):
        self.ensure_one()
        log_info = ""
        if self.import_module_id:
            return self.import_module_id, log_info
        module_obj = self.env["ir.module.module"]
        search_domain = [("name", "=", self.module_technical_name)]
        modules = module_obj.search(search_domain)
        if not modules:
            log_info = _("No module %(module_name)s found.") % {
                "module_name": self.module_technical_name,
            }
        return modules, log_info

    def button_update(self):
        self.ensure_one()
        self.import_module_id.button_immediate_upgrade()

    def button_install(self):
        self.ensure_one()
        self.import_module_id.button_immediate_install()
