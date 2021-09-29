
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

from itertools import groupby
import logging


_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"


    def _prepare_picking_preorder_vals(self, partner, picking_type, location_id, location_dest_id, lines):
        return {
            'partner_id': partner.id if partner else False,
            'user_id': False,
            'picking_type_id': picking_type.id,
            'move_type': 'direct',
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'pos_session_id': lines.order_id.session_id.id,
            'pos_order_id': lines.order_id.id,
        }

    @api.model
    def _create_picking_from_pos_preorder(self, location_dest_id, lines, picking_type, partner=False):
        pickings = self.env['stock.picking']
        is_need_materials = lines.filtered(lambda l: l.product_id.is_need_materials and not float_is_zero(l.qty, precision_rounding=l.product_id.uom_id.rounding))
        if not is_need_materials:
            return pickings

        if is_need_materials:
            location_id = picking_type.default_location_src_id.id
            # create picking split by order line
            for line in is_need_materials.sorted(key='id', reverse=True):
                preorder_picking = self.env['stock.picking'].create(
                    self._prepare_picking_preorder_vals(partner, picking_type, location_id, location_dest_id, lines)
                )
                list_moves = []
                for material in line.product_id.material_product_ids:
                    product = material.product_variant_id
                    quantity = product.material_qty * line.qty
                    moves = preorder_picking._create_move_from_pre_order_lines(line, product, quantity)
                    list_moves.append(moves.id)
                preorder_picking.write({
                    'move_ids_without_package': [(6, 0, list_moves)],
                })
                try:
                    with self.env.cr.savepoint():
                        preorder_picking.action_confirm()
                except (UserError, ValidationError):
                    pass

                pickings |= preorder_picking
        return pickings

    def _create_move_from_pre_order_lines(self, lines, product_id, quantity):
        self.ensure_one()
        move = self.env['stock.move'].create(
            self._prepare_preorder_stock_move_vals(lines, product_id, quantity))
        return move

    def _prepare_preorder_stock_move_vals(self, first_line, product, quantity):
        return {
            'name': product.name,
            'product_uom':product.uom_id.id,
            'picking_id': self.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': product.id,
            'product_uom_qty': quantity,
            'state': 'draft',
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'company_id': first_line.company_id.id,
        }
