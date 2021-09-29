from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    is_food = fields.Boolean('Food', default=False)
    is_drink = fields.Boolean('Drink', default=False)
    is_need_materials = fields.Boolean('Is Need Materials', default=False)
    material_qty = fields.Integer('Quantity')
    material_product_ids = fields.Many2many('product.template', 'material_rel', 'product_id', 'material_id', string='Materials', store=True)

    @api.constrains('is_food', 'is_drink')
    def _check_closing_date(self):
        for product in self:
            if product.is_food and product.is_drink:
                raise ValidationError(_("is confused, you can't select all type product"))

    # @api.onchange('is_food', 'is_drink')
    # def onchange_type_product(self):
    #     _logger.info("SSSSSSSSSS")
    #     if self.is_food:
    #         self.is_drink = False


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"


    is_food = fields.Boolean('Food', related='product_id.is_food', store=True)
    is_drink = fields.Boolean('Drink', related='product_id.is_drink', store=True)