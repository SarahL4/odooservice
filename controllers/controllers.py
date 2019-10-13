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
import werkzeug

import logging

# ~ _logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)


class ServiceMobile(http.Controller):

    @http.route('/service/all/order/', auth='user', website=True)
    def index_order(self, **kw):
        return http.request.render('service_mobile.index', {
            'root': '/service/all/order/',
            'order_ids': http.request.env['sale.order'].search([]),

        })

    @http.route('/service/<model("sale.order"):order>/order/', auth='user', website=True, methods=['GET', 'POST'])
    def update_order(self, order, **post):
        if post:
            logger.exception('kw %s' % post)
            order.note = post.get('note')
            order.prio = post.get('prio')

            order.order_line.product_uom_qty = post.get('qty')
            # order.order_line.update_order_line(order.order_line.id)

            logger.exception('kw %s' % order.note)

            return werkzeug.utils.redirect('/service/all/order/', 302)
        else:
            sale_order_line = http.request.env['sale.order.line'].search([('product_uom.name', '=', 'Timme(ar)')])
            sale_order_line_ids = sale_order_line.search([('order_id', '=', order.id)])
            return http.request.render('service_mobile.view_order', {
                'root': '/service/%s/order/' % order.id,
                'partner_ids': http.request.env['res.partner'].search([('customer', '=', True)]),
                # 'sale_order_line_ids': http.request.env['sale.order.line'].search([]),
                'order': order,
                'sale_order_line_ids': sale_order_line_ids,
                # 'sale_order_line_ids': http.request.env['sale.order.line'].search([('product_uom', '=', 'Timme(ar)')]),
                'help': {'name': 'This is help string for name'},
                'validation': {'name': 'Warning'},
                'input_attrs': {},
            })

    @http.route('/service/order/create', auth='user', website=True, methods=['GET', 'POST'])
    def create_order(self, **post):
        if post:
            new_order_params = {
                'partner_id': int(post.get('partner_id')),
            }

            new_order = http.request.env['sale.order'].create(new_order_params)
            new_order.set_template(int(post.get('sale_order_template_id')))

            # ~ return self.index_order()
            return werkzeug.utils.redirect('/service/all/order/', 302)
        else:
            return http.request.render('service_mobile.create_order', {
                'root': '/service/order/create',
                'partner_ids': http.request.env['res.partner'].search([('customer', '=', True)]),
                'sale_order_template_ids': http.request.env['sale.order.template'].search([]),
                # ~ 'order': order,
                'help': {'name': 'This is helpstring for name'},
                'validation': {'name': 'Warning'},
                'input_attrs': {},
            })

    @http.route('/service/<model("sale.order"):order>/order/delete', auth='user', website=True)
    def delete_order(self, order, **kw):
        if order.state != 'cancel':
            order_state: 'cancel'
            order.state = 'cancel'

            return http.request.render('service_mobile.index', {
                'root': '/service/all/order/',
                'order_ids': http.request.env['sale.order'].search([]),
                'order_state': 'cancel',
                'order.state': order.state
            })
        else:
            order.unlink()
            order_state: 'cancel'
            order.state = 'cancel'
            return werkzeug.utils.redirect('/service/all/order/', 302)

    @http.route('/service/<model("sale.order"):order>/order/send', auth='user')
    def confirm_order(self, order, **kw):
        if order.state != 'cancel':
            order.send_offer()
            if order.state == 'draft':
                order.state = 'sent'

        return werkzeug.utils.redirect('/service/all/order', 302)

    # VG-uppgift
    @http.route('/service/public/order', auth='none')
    def index_order_pub(self, **kw):
        return http.request.render('service_mobile.index_public', {
            'root': '/service/public/order',
            'order_ids': http.request.env['sale.order'].sudo().search([]),
        })

# -------------------------------------------
    # F4 Project.project

    @http.route('/service/all/project', auth='user', website=True)
    def index_project(self, **kw):
        return http.request.render('service_mobile.index_project', {
            'root': '/service/all/project',
            'order_ids': http.request.env['sale.order'].search([]),
            'project_ids': http.request.env['project.project'].search([]),
        })

    @http.route('/service/<model("project.project"):project>/project/', auth='user', website=True, methods=['GET','POST'])
    def update_project(self, project, **post):
        if post:
            logger.exception('kw %s' % post)
            project.user_id = int(post.get('user_id')),
            project.partner_id = int(post.get('partner_id')),

            logger.exception('kw %s' % project.user_id)

            return werkzeug.utils.redirect('/service/all/project', 302)
        else:
            return http.request.render('service_mobile.view_project', {
                'root': '/service/%s/project/' % project.id,
                'project': project,
                'project.partner_id.name':project.partner_id.name,
                'project.user_id': project.user_id,
                'partner_ids': http.request.env['res.partner'].search([('customer', '=', True)]),
                'user_ids': http.request.env['res.users'].search([]),
                'help': {'name': 'This is help string for name'},
                'validation': {'name': 'Warning'},
                'input_attrs': {},
            })

    @http.route('/service/project/create', auth='user', website=True, methods=['GET', 'POST'])
    def create_project(self, **post):
        if post:
            new_project_params = {
                'name': post.get('project_name'),
                'allow_timesheets': post.get('allow_timesheets'),
                'partner_id': int(post.get('partner_id')),
            }

            http.request.env['project.project'].create(new_project_params)

            return werkzeug.utils.redirect('/service/all/project/', 302)
        else:
            return http.request.render('service_mobile.create_project', {
                'root': '/service/project/create',
                'project_ids': http.request.env['project.project'].search([]),
                'partner_ids': http.request.env['res.partner'].search([('customer', '=', True)]),
                'order_ids': http.request.env['sale.order'].search([]),
                'help': {'name': 'This is help string for name'},
                'validation': {'name': 'Warning'},
                'input_attrs': {},
            })

    @http.route('/service/<model("project.project"):project>/project/delete', auth='user', website=True)
    def delete_project(self, project, **kw):
        project.unlink()
        # self.index_project()
        return werkzeug.utils.redirect('/service/all/project', 302)

# @http.route('/service/<model("project.project"):project>/project/invoice', auth='user')
# def invoice_propject(self, order,**kw):
#     project.invoice() # ?????????????
#     self.index_project()
