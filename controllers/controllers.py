# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution, third party addon
# Copyright (C) 2004-2019 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from odoo import http

import logging
# ~ _logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)


class ServiceMobile(http.Controller):

    @http.route('/service/all/order/', auth='user')
    def index_order(self, **kw):
        return http.request.render('service_mobile.index', {
            'root': '/service/all/order/',
            'order_ids': http.request.env['sale.order'].search([]),
            
        })
        
    @http.route('/service/<model("sale.order"):order>/order/', auth='user',website=True, methods=['GET','POST'])
    def update_order(self, order,**post):
        if post:
            logger.exception('kw %s' % post)
            order.note = post.get('note')
            order.prio = post.get('prio')
            logger.exception('kw %s' % order.note)

            return self.index_order()
        else:
            return http.request.render('service_mobile.view_order', {
                              'root': '/service/%s/order/' % order.id,
                              'partner_ids': http.request.env['res.partner'].search([('customer','=',True)]),
                              'order': order,
                              'help': {'name':'This is helpstring for name'},
                               'validation': {'name':'Warning'},
                              'input_attrs': {},
                          })

    @http.route('/service/order/create', auth='user')
    def create_order(self, order,**kw):
        order.unlink()
        self.index_order()

    @http.route('/service/<model("sale.order"):order>/order/delete', auth='user')
    def delete_order(self, order,**kw):
        order.unlink()
        self.index_order()

    @http.route('/service/<model("sale.order"):order>/order/send', auth='user')
    def confirm_order(self, order,**kw):
        order.send() # ?????????????
        self.index_order()

#--------------------------------------------

    @http.route('/service/all/project/', auth='user')
    def index_project(self, **kw):
        return http.request.render('service_mobile.index_project', {
            'root': '/service/%s/project/' % order.id,
            'order_ids': http.request.env['sale.order'].search([]),
        })
        
    @http.route('/service/<model("project.project"):project>/project/', auth='user')
    def update_project(self, project,**kw):
        
        # if post xxx
        
        return http.request.render('service_mobile.view_project', {
            'root': '/service/%s/project/' % project.id,
            'product_ids': http.request.env['product.product'].search([('is_sale','=',True)]),
            'order': order,
        })

    @http.route('/service/<model("project.project"):project>/project/delete', auth='user')
    def delete_project(self, project,**kw):
        project.unlink()
        self.index_project()

    @http.route('/service/<model("project.project"):project>/project/invoice', auth='user')
    def invoice_propject(self, order,**kw):
        project.invoice() # ?????????????
        self.index_project()
