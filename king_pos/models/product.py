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
    material_product_ids = fields.One2many('product.materials', 'material_id', string='Materials', store=True)

    @api.constrains('is_food', 'is_drink')
    def _check_type_product_in_pos(self):
        for product in self:
            if product.is_food and product.is_drink:
                raise ValidationError(_("is confused, you can't select all type product"))


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"


    is_food = fields.Boolean('Food', related='product_id.is_food', store=True)
    is_drink = fields.Boolean('Drink', related='product_id.is_drink', store=True)


class ProductMaterials(models.Model):
    _name = "product.materials"

    material_id = fields.Many2one('product.template', 'Materials For Product')
    product_tmpl_id = fields.Many2one('product.template', 'Materials Product')
    material_qty = fields.Float('Quantity')
    uom_id = fields.Many2one('uom.uom', related='product_tmpl_id.uom_id')