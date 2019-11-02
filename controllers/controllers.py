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


from odoo import http, fields
from odoo.http import request, Response
import werkzeug
import datetime
import base64

import logging

# ~ _logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)


class ServiceMobile(http.Controller):
    # Show list of orders (show only "Fully Invoiced")
    @http.route('/service/all/order/', auth='user', website=True)
    def index_order(self, **kw):
        # order_ids = http.request.env['sale.order'].search([])
        order_ids = http.request.env['sale.order'].search([]).filtered(
            lambda r: r.invoice_status != 'invoiced' and r.state != 'cancel')
        return http.request.render('service_mobile.index', {
            'root': '/service/all/order/',
            'order_ids': order_ids
        })

    @http.route('/service/all/order_mobile/', auth='public', website=True)
    def index_mobile(self, **kw):
        order_ids = http.request.env['sale.order'].search([]).filtered(
            lambda r: r.invoice_status != 'invoiced' and r.state != 'cancel')

        return http.request.render('service_mobile.mobile_layout', {
            'root': '/service/all/order_mobile/',
            'order_ids': order_ids
        })

    # @http.route('/service/all/order_mobile',auth='user', website=True)
    # def index_mobile(self, **kw):
    #     order_ids = http.request.env['sale.order'].search([]).filtered(
    #         lambda r: r.invoice_status != 'invoiced' and r.state != 'cancel')
    #
    #     return http.request.render('service_mobile.index_mobile', {
    #         'root': '/service/all/order_mobile',
    #         'order_ids': order_ids
    #     })

    # Show list of orders quantity and amount
    @http.route('/service/all/result/', auth='user', website=True)
    def index_result(self, **kw):
        order_ids_hour = http.request.env['sale.order.line'].search([('product_uom.name', '=', 'Timme(ar)')])
        order_ids_piece = http.request.env['sale.order.line'].search([('product_uom.name', '=', 'st')])

        qtys = order_ids_hour.mapped('product_uom_qty')
        qty_total = 0
        for q in qtys:
            qty_total += q

        price_sub = order_ids_hour.mapped('price_subtotal')
        price_subtotal = 0
        for p in price_sub:
            price_subtotal += p

        price_t = order_ids_hour.mapped('price_tax')
        price_tax = 0
        for pt in price_t:
            price_tax += pt

        price_to = order_ids_hour.mapped('price_total')
        price_total = 0
        for pto in price_to:
            price_total += pto
        # -------------------------------
        pqtys = order_ids_piece.mapped('product_uom_qty')
        pqty_total = 0
        for q in pqtys:
            pqty_total += q

        pprice_sub = order_ids_piece.mapped('price_subtotal')
        pprice_subtotal = 0
        for p in pprice_sub:
            pprice_subtotal += p

        pprice_t = order_ids_piece.mapped('price_tax')
        pprice_tax = 0
        for pt in pprice_t:
            pprice_tax += pt

        pprice_to = order_ids_piece.mapped('price_total')
        pprice_total = 0
        for pto in pprice_to:
            pprice_total += pto

        return http.request.render('service_mobile.index_result', {
            'root': '/service/all/result/',
            'order_ids_hour': order_ids_hour,
            'order_ids_piece': order_ids_piece,
            'product_uom_hour': order_ids_hour[0].product_uom.name,
            'product_uom_piece': order_ids_piece[0].product_uom.name,
            'qty_total': qty_total,
            'price_subtotal': price_subtotal,
            'price_tax': price_tax,
            'price_total': pprice_total,
            'pqty_total': pqty_total,
            'pprice_subtotal': pprice_subtotal,
            'pprice_tax': pprice_tax,
            'pprice_total': pprice_total,
        })

    # Route-address can type: http://localhost:8069/kimvvs.se/1 or http://localhost:8069/kimvvs.se/yourcompany-1/
    # Get partner information such as partner.id as parameter from route-address.
    # Return a page that show a visit-card of a partner
    @http.route('/kimvvs.se/<model("res.partner"):_partner>/', auth='public', website=True)
    def vcard_partner_view(self, _partner, **kw):
        partner_ids = http.request.env['res.partner'].search([])
        partner = partner_ids.filtered(lambda r:r.id ==_partner.id)

        return http.request.render('service_mobile.partner_vcard_view', {
            'root': '/kimvvs.se/%s' % partner.id,
            'partner': partner
        })

    # When "lägg till kontakterna" link in "/kimvvs.se/1" is clicked, partner's info/ID send to controller here
    # Method "vcard_partner" in controller prepare alla required data to visit-card in form of vcard.vcf
    # Method return a vcard data, and automatically allow user download this visit-card and use it in email or mobile contacts
    @http.route(['/kimvvs.se/<model("res.partner"):_partner>/send/vcard.vcf'], auth='public', website=True)
    def vcard_partner(self, _partner, **kw):
        partner = http.request.env['res.partner'].search([('id', '=', _partner.id)])

        _company_name = ''
        if partner.company_name:
            _company_name = partner.company_name
        else:
            _company_name = partner.parent_id.display_name

        _title = ''
        if partner.function:
            _title = partner.function
        else:
            _title = 'No Title'

        result = """BEGIN:VCARD
                    VERSION:3.0
                    FN;CHARSET=UTF-8:{name}
                    TITLE;CHARSET=UTF-8:{title}
                    TEL;TYPE=WORK,VOICE:{phone}
                    EMAIL;CHARSET=UTF-8;type=WORK,INTERNET:{email}
                    ORG;CHARSET=UTF-8:{company}
                    URL;CHARSET=UTF-8:'http://localhost:8069/kimvvs.se/{id}
                    REV:2019-11-02T09:26:53.011Z
                    END:VCARD""".format(
            name=partner.name,
            title=_title,
            phone=partner.phone,
            email=partner.email,
            company=_company_name,
            id=partner.id)
        return Response(result, mimetype='text/vcard')

    # Show order detail and update order
    @http.route('/service/<model("sale.order"):order>/order/', auth='user', website=True, methods=['GET', 'POST'])
    def update_order(self, order, **post):
        if post:
            order.note = post.get('note')
            order.prio = post.get('prio')
            # env['sale.order.line'].search([('order_id', '=', order.id), ('line.product_uom', '=', http.request.env.ref('uom.product_uom_hour'))])

            sale_order_line_ids = order.order_line.search(
                [('order_id', '=', order.id), ('product_uom.name', '=', 'Timme(ar)')])
            if len(sale_order_line_ids) > 0:
                sale_order_line_ids[0].product_uom_qty = post.get('qty')
                sale_order_line_ids[0].qty_delivered = post.get('qty_delivered')

            # return werkzeug.utils.redirect('/service/all/order/', 302)
            return http.request.render('service_mobile.view_order', {
                'root': '/service/%s/order/' % order.id,
                'order': order,
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'employee': http.request.env['hr.employee'].search([('user_id', '=', http.request.session.uid)]),
                'partner_ids': http.request.env['res.partner'].search([('customer', '=', True)]),
                'sale_order_line_ids': sale_order_line_ids,
                'help': {'name': 'This is help string for name'},
                'validation': {'name': 'Warning'},
                'input_attrs': {},
            })
        else:
            sale_order_line_ids = order.order_line.search(
                [('order_id', '=', order.id), ('product_uom.name', '=', 'Timme(ar)')])
            # sale_order_line_ids = order.order_line.search([('order_id', '=', order.id),('product_uom.name', '=', http.request.env.ref('uom.product_uom_hour'))])
            try:
                task_index = order.tasks_ids[0]
            except IndexError:
                task_index = 'null'

            if task_index != 'null':
                task_objs = order.tasks_ids[0].project_id.analytic_account_id.line_ids.filtered(
                    lambda r: r.task_id.sale_order_id.name == order.name)

                return http.request.render('service_mobile.view_order', {
                    'root': '/service/%s/order/' % order.id,
                    'partner_ids': http.request.env['res.partner'].search([('customer', '=', True)]),
                    'order': order,
                    'sale_order_line_ids': sale_order_line_ids,
                    'task_objs': task_objs,
                    'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'employee': http.request.env['hr.employee'].search([('user_id', '=', http.request.session.uid)]),
                    'help': {'name': 'This is help string for name'},
                    'validation': {'name': 'Warning'},
                    'input_attrs': {},
                })
            else:
                return http.request.render('service_mobile.view_order', {
                    'root': '/service/%s/order/' % order.id,
                    'partner_ids': http.request.env['res.partner'].search([('customer', '=', True)]),
                    'order': order,
                    'sale_order_line_ids': sale_order_line_ids,
                    'task_objs': task_index,
                    'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'employee': http.request.env['hr.employee'].search([('user_id', '=', http.request.session.uid)]),
                    'help': {'name': 'This is help string for name'},
                    'validation': {'name': 'Warning'},
                    'input_attrs': {},
                })

    # Add work hour till order-project-task
    @http.route('/service/<model("sale.order"):order>/task/', auth='user', website=True, methods=['GET', 'POST'])
    def add_task(self, order, **post):
        tasks = order.tasks_ids
        if post:
            if len(order.tasks_ids) > 0:
                new_task_params = {'date': datetime.datetime.now(),
                                   # 'employee_id': http.request.website.user_id.id,
                                   'employee_id': http.request.env['hr.employee'].search(
                                       [('user_id', '=', http.request.session.uid)])[0].id,
                                   'name': post.get('name'),
                                   'unit_amount': float(post.get('hours')),
                                   'account_id': order.tasks_ids[0].project_id.analytic_account_id.id,
                                   'task_id': order.tasks_ids[0].id,
                                   'user_id': http.request.session.uid,
                                   # 'user_id': order.tasks_ids[0].user_id.id,
                                   'project_id': order.tasks_ids[0].project_id.id,
                                   }
                http.request.env['account.analytic.line'].create(new_task_params)
            return werkzeug.utils.redirect('/service/%s/order/' % order.id, 302)
        else:
            task_objs = order.tasks_ids[0].project_id.analytic_account_id.line_ids.filtered(
                lambda r: r.task_id.sale_order_id.name == order.name)

            logger.exception('kw %s' % task_objs)
            return http.request.render('service_mobile.view_task', {
                'root': '/service/%s/task/' % order.id,
                'order': order,
                'task_objs': task_objs,
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'employee': http.request.env['hr.employee'].search([('user_id', '=', http.request.session.uid)]),
                'help': {'name': 'This is help string for name'},
                'validation': {'name': 'Warning'},
                'input_attrs': {},
            })

    # Update/delivery on row "levererat antal" -> Deliver Now
    @http.route('/service/<model("sale.order.line"):order_line>/line/deliver', auth='user', website=True)
    def update_delivery(self, order_line, **kw):
        order_line.qty_delivered = order_line.product_uom_qty
        order_url = '/service/%s/order/' % order_line.order_id.id

        return werkzeug.utils.redirect(order_url, 302)

    # Create an new order
    @http.route('/service/order/create', auth='user', website=True, methods=['GET', 'POST'])
    def create_order(self, **post):
        if post:
            new_order_params = {
                'partner_id': int(post.get('partner_id')),
            }

            new_order = http.request.env['sale.order'].create(new_order_params)
            new_order.set_template(int(post.get('sale_order_template_id')))

            return werkzeug.utils.redirect('/service/all/order/', 302)
        else:
            return http.request.render('service_mobile.create_order', {
                'root': '/service/order/create',
                'partner_ids': http.request.env['res.partner'].search([('customer', '=', True)]),
                'sale_order_template_ids': http.request.env['sale.order.template'].search([]),
                'help': {'name': 'This is help string for name'},
                'validation': {'name': 'Warning'},
                'input_attrs': {},
            })

    # Delete an order
    @http.route('/service/<model("sale.order"):order>/order/delete', auth='user', website=True)
    def delete_order(self, order, **kw):
        if order.state != 'cancel':
            order.state = 'cancel'
            order.unlink()
            return werkzeug.utils.redirect('/service/all/order/', 302)

        # if order.state != 'cancel':
        #     order_state: 'cancel'
        #     order.state = 'cancel'
        #
        #     return http.request.render('service_mobile.index', {
        #         'root': '/service/all/order/',
        #         'order_ids':http.request.env['sale.order'].search([]).filtered(lambda r: r.invoice_status != 'invoiced'),
        #         'order_state': 'cancel',
        #         'order.state': order.state
        #     })
        # else:
        #     order.unlink()
        #     order_state: 'cancel'
        #     order.state = 'cancel'
        #     return werkzeug.utils.redirect('/service/all/order/', 302)

    # Send order
    @http.route('/service/<model("sale.order"):order>/order/send', auth='user')
    def confirm_order(self, order, **kw):
        if order.state != 'cancel':
            # send_offer()
            template = http.request.env.ref('sale.email_template_edi_sale')
            template.write({'email_to': order.partner_id.email})
            template.send_mail(order.id, force_send=True)
            if order.state == 'draft':
                order.state = 'sent'

        return werkzeug.utils.redirect('/service/all/order', 302)

    # F7 Show order's images: /service/%s/images' % order.id
    @http.route('/service/<model("sale.order"):order>/images', auth='user', website=True, methods=['GET', 'POST'])
    def order_images(self, order, **post):
        if post:
            # Upload file
            if post.get('ufile'):
                ufile = post.get('ufile')
                file_datas_bytes = ufile.read()
                file_datas_binary = base64.b64encode(file_datas_bytes)
                logger.warn("Bytes data: %s" % file_datas_bytes[:100])
                logger.warn("Binary data: %s" % file_datas_binary[:100])

                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                attachment_params = {
                    'name': '%s %s' % (ufile.name, current_datetime),
                    'type': 'binary',
                    'datas': file_datas_binary,
                    'datas_fname': ufile.filename,
                    'res_model': 'sale.order',
                    'res_id': order.id,
                    'mimetype': ufile.mimetype,
                }
                attachment_new = http.request.env['ir.attachment'].create(attachment_params)
                order_url = '/service/%s/images/' % order.id
                return werkzeug.utils.redirect(order_url, 302)
                # return werkzeug.utils.redirect('/service/all/order', 302)
        else:
            order_attachment_ids = http.request.env['ir.attachment'].search(
                [('res_model', '=', 'sale.order'), ('res_id', '=', order.id)])
            return http.request.render('service_mobile.order_images', {
                'root': '/service/%s/images/' % order.id,
                'order': order,
                'order_attachment_ids': order_attachment_ids,
                'help': {'name': 'This is help string for name'},
                'validation': {'name': 'Warning'},
                'message': {'ufile': ''},
                'input_attrs': {},
            })

        # order_url='/service/%s/order/' % order_line.order_id.id

        # return werkzeug.utils.redirect(order_url, 302)

    @http.route('/service/<model("sale.order"):order>/order/flag', type='json', auth="user", website=True)
    def post_flag(self, order, **kwargs):
        if not http.request.session.uid:
            return {'error': 'anonymous_user'}

        try:
            # Invert order.prio False -> True, True -> False
            order.prio = not order.prio
        except:
            return {'error': 'post_non_flaggable'}

        return {'success': 'Yes!',
                'flag_value': order.prio,
                'order_id': order.id,
                }

    # method: skapa fakturan. den returnerar ett id, inte objekt
    @http.route('/service/<model("sale.order"):order>/invoice/send/', type="json", auth='user', website=True)
    def create_invoice(self, order, **kw):
        if not http.request.session.uid:
            return {'error': 'anonymous_user'}

        try:
            new_invoice_id = order.action_invoice_create()
            invoice = http.request.env['account.invoice'].browse(new_invoice_id)

            if invoice.state != 'cancel' and order.state == 'sale' and order.state != 'cancel':
                if invoice.state == 'draft':
                    # Customer can pay now
                    invoice.state = 'open'

                template = http.request.env.ref('account.email_template_edi_invoice')
                template.write({'email_to': invoice.partner_id.email})
                template.send_mail(invoice.id, force_send=True)

            if order.state != 'cancel':
                order.invoice_status = "invoiced"
        except:
            return {'error': 'post_non_check'}

        return {'success': 'Yes!',
                'check_value': order.invoice_status,
                'order_id': order.id,
                }

        # return werkzeug.utils.redirect('/service/all/order/', 302)

    # method: skapa fakturan. den returnerar ett id, inte objekt
    # @http.route('/service/<model("sale.order"):order>/invoice/send/', auth='user', website=True, methods=['GET', 'POST'])
    # def create_invoice(self, order, **kw):
    #     new_invoice_id = order.action_invoice_create()
    #     invoice = http.request.env['account.invoice'].browse(new_invoice_id)
    #     template = http.request.env.ref('account.email_template_edi_invoice')
    #     template.write({'email_to': order.partner_id.email})
    #     template.send_mail(invoice.id, force_send=True)
    #
    #     return werkzeug.utils.redirect('/service/all/order/', 302)

    # -------------------------------------------
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
        project_ids = http.request.env['project.project'].search([]).sorted(key=lambda r: r.id, reverse=True)
        return http.request.render('service_mobile.index_project', {
            'root': '/service/all/project',
            'project_ids': project_ids,
        })

    @http.route('/service/<model("project.project"):project>/project/', auth='user', website=True,
                methods=['GET', 'POST'])
    def update_project(self, project, **post):
        if post:
            try:
                project.user_id = int(post.get('user_id'))
                project.partner_id = int(post.get('partner_id'))
            except IndexError:
                project.user_id = 'null'
                project.partner_id = 'null'

            logger.exception('kw %s' % post)

            # Upload file
            if post.get('ufile'):
                ufile = post.get('ufile')
                file_datas_bytes = ufile.read()
                file_datas_binary = base64.b64encode(file_datas_bytes)
                logger.warn("Bytes data: %s" % file_datas_bytes[:100])
                logger.warn("Binary data: %s" % file_datas_binary[:100])

                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                attachment_params = {
                    'name': '%s %s' % (ufile.name, current_datetime),
                    'type': 'binary',
                    'datas': file_datas_binary,
                    'datas_fname': ufile.filename,
                    'res_model': 'project.project',
                    'res_id': project.id,
                    'mimetype': ufile.mimetype,
                }

                attachment_new = http.request.env['ir.attachment'].create(attachment_params)

            return werkzeug.utils.redirect('/service/all/project', 302)
        else:
            project_attachment_ids = http.request.env['ir.attachment'].search([('res_id', '=', project.id)])
            project_id = http.request.env['project.project'].search([('id', '=', project.id)])
            return http.request.render('service_mobile.view_project', {
                'root': '/service/%s/project/' % project.id,
                'project': project,
                'project_partner_id': project_id.partner_id,
                'project_user_id': project_id.user_id,
                'project_doc_count': project_id.doc_count,
                'partner_ids': http.request.env['res.partner'].search([('customer', '=', True)]),
                'user_ids': http.request.env['res.users'].search([]),
                'project_attachment_ids': project_attachment_ids,
                'help': {'name': 'This is help string for name'},
                'validation': {'name': 'Warning'},
                'message': {'ufile': ''},
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
