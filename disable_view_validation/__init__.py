from odoo.addons.base.models.ir_ui_view import View
import logging

_logger = logging.getLogger(__name__)

_original_check_xml = View._check_xml

def _check_xml(self):
    try:
        _original_check_xml(self)
    except Exception as e:
        _logger.warning("Se ignoró un error al validar el XML de una vista: %s", e)

View._check_xml = _check_xml
