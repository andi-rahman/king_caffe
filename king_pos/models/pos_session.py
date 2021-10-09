from odoo import fields, models, _
import logging

_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = "pos.session"

    def action_pos_session_closing_control(self):
        for session in self:
            for order in session.order_ids.sorted(lambda x: x.id):
                lines = []
                for line in order.lines.filtered(lambda x: x.product_id.is_need_materials):
                    lines.append(line.id)

                if any(p.product_id.is_need_materials for p in order.lines):
                    self._prepare_pre_order(lines, order)

        return super(PosSession, self).action_pos_session_closing_control()


    def _prepare_pre_order(self, lines, order):
        temp = {
            'date': fields.date.today(),
            'pos_session_id': self.id,
            'pos_order_id': order.id,
            'pos_order_line_ids': [(6, 0, lines)],
        }
        pickings = self._create_picking_preorder_at_end_of_session(order)
        if pickings:
            temp.update({'picking_ids': [(6, 0, pickings.ids)]})
        return temp

    def _create_picking_preorder_at_end_of_session(self, order):
        self.ensure_one()
        lines_grouped_by_dest_location = {}
        picking_type = self.config_id.picking_type_id

        pickings = False

        if not picking_type or not picking_type.default_location_dest_id:
            session_destination_id = self.env['stock.warehouse']._get_partner_locations()[0].id
        else:
            session_destination_id = picking_type.default_location_dest_id.id

        for order in order:
            if order.company_id.anglo_saxon_accounting and order.to_invoice:
                continue
            destination_id = order.partner_id.property_stock_customer.id or session_destination_id
            if destination_id in lines_grouped_by_dest_location:
                lines_grouped_by_dest_location[destination_id] |= order.lines
            else:
                lines_grouped_by_dest_location[destination_id] = order.lines

        for location_dest_id, lines in lines_grouped_by_dest_location.items():
            pickings = self.env['stock.picking']._create_picking_from_pos_preorder(location_dest_id, lines, picking_type)
        return pickings
