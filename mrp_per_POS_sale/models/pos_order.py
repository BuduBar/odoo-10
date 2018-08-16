# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, conf, _
from odoo.exceptions import Warning, UserError
from odoo.tools import float_compare, float_round
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    @api.multi
    def create(self, values):
        mrp_obj = self.env['mrp.production']
        product_obj = self.env['product.product']  
        procurement_obj = self.env['procurement.order'] 
        bom_obj = self.env['mrp.bom']            
        if values.get('lines'):
            for line in values.get('lines'):
                product = product_obj.browse(line[2].get('product_id'))
                #if product.route_ids.name:                   
                _logger.warning('---------------> product name {}'.format(product.product_tmpl_id.name))                
                bom = bom_obj.search([('product_tmpl_id', '=', product.product_tmpl_id.id)])        
                mrp_created = mrp_obj.create({
                                        'product_id': product.id,
                                        'product_qty': line[2].get('qty'),
                                        'product_uom_id': product.product_tmpl_id.uom_id.id, 
                                        'bom_id': bom.id,
                                        'date_planed_start': values.get('date_order'), 
                                        'user_id': self.env.uid,
                                        'origin': values.get('name') 
                })    
                mrp_created.action_assign()     
                exception_order = procurement_obj.search([("origin", "like", mrp_created.name)])                 
                if exception_order:
                    #print '%s: %s' % (_(Warning), _('No hay {}'.format(exception_order.product_id.name)))
                    #_logger.warning('---------------> exception {}, No hay pŕoductos'.format(exception_order))
                    raise UserError('No hay {}'.format(exception_order.product_id.name))   
                else:
                    self.do_produce_mrp_by_product(mrp_created) 
                    mrp_created.button_mark_done()
                    _logger.warning('---------------> todo bien')          
        
        return super(PosOrder, self).create(values)

    def do_produce_mrp_by_product(self, mrp_obj):
        # Nothing to do for lots since values are created using default data (stock.move.lots)
        moves = mrp_obj.move_raw_ids
        quantity = mrp_obj.product_qty
        if float_compare(quantity, 0, precision_rounding=mrp_obj.product_uom_id.rounding) <= 0:
            raise UserError(_('You should at least produce some quantity'))
        for move in moves.filtered(lambda x: x.product_id.tracking == 'none' and x.state not in ('done', 'cancel')):
            if move.unit_factor:
                rounding = move.product_uom.rounding
                move.quantity_done_store += float_round(quantity * move.unit_factor, precision_rounding=rounding)
        moves = mrp_obj.move_finished_ids.filtered(lambda x: x.product_id.tracking == 'none' and x.state not in ('done', 'cancel'))
        for move in moves:
            rounding = move.product_uom.rounding
            if move.product_id.id == mrp_obj.product_id.id:
                move.quantity_done_store += float_round(quantity, precision_rounding=rounding)
            elif move.unit_factor:
                # byproducts handling
                move.quantity_done_store += float_round(quantity * move.unit_factor, precision_rounding=rounding)
        self.check_finished_move_lots(mrp_obj)
        if mrp_obj.state == 'confirmed':
            mrp_obj.write({
                'state': 'progress',
                'date_start': datetime.now(),
            })
        return {'type': 'ir.actions.act_window_close'}

    
    def check_finished_move_lots(self, move_obj):
        lots_obj = self.env['stock.move.lots']
        _logger.warning('-------------------> aqui ')
        produce_move = move_obj.move_finished_ids.filtered(lambda x: x.product_id == move_obj.product_id and x.state not in ('done', 'cancel'))
        _logger.warning('-------------------> produce_move {}'.format(produce_move))
        _logger.warning('-------------------> tracking {}'.format(produce_move.product_id.tracking))
        if produce_move and produce_move.product_id.tracking != 'none':
            # TODO ver para sirve self.lot_id
            if not self.lot_id:
                raise UserError(_('You need to provide a lot for the finished product'))
            existing_move_lot = produce_move.move_lot_ids.filtered(lambda x: x.lot_id == self.lot_id)
            if existing_move_lot:
                existing_move_lot.quantity += move_obj.product_qty
                existing_move_lot.quantity_done += move_obj.product_qty
            else:
                vals = {
                  'move_id': produce_move.id,
                  'product_id': produce_move.product_id.id,
                  'production_id': move_obj.id,
                  'quantity': move_obj.product_qty,
                  'quantity_done': move_obj.product_qty,
                  'lot_id': self.lot_id.id,
                }
                lots_obj.create(vals)
            for move in move_obj.move_raw_ids:
                for movelots in move.move_lot_ids.filtered(lambda x: not x.lot_produced_id):
                    if movelots.quantity_done and self.lot_id:
                        #Possibly the entire move is selected
                        remaining_qty = movelots.quantity - movelots.quantity_done
                        if remaining_qty > 0:
                            default = {'quantity': movelots.quantity_done, 'lot_produced_id': self.lot_id.id}
                            new_move_lot = movelots.copy(default=default)
                            movelots.write({'quantity': remaining_qty, 'quantity_done': 0})
                        else:
                            movelots.write({'lot_produced_id': self.lot_id.id})
        return True