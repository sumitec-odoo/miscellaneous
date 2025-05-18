from odoo.addons.base.models.ir_ui_view import View

def monkey_patches():
    """ Monkey Patch para desactivar la validación XML de las vistas """

    def _bypass_check_xml(self):
        return True  # Desactiva la validación de XML en vistas

    # Aplicar el Monkey Patch al método _check_xml
    View._check_xml = _bypass_check_xml
