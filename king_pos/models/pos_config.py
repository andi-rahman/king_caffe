from odoo import models, api, fields
import logging

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    iface_pin = fields.Boolean('PIN', default=True)
    iface_kitchen = fields.Boolean('Kitchen', default=True)
    iface_bar = fields.Boolean('Bar', default=True)
    pin = fields.Char('PIN', required=True)