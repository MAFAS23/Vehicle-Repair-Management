# -*- coding: utf-8 -*-
# from odoo import http


# class VehicleRepairManagement(http.Controller):
#     @http.route('/vehicle_repair_management/vehicle_repair_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vehicle_repair_management/vehicle_repair_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vehicle_repair_management.listing', {
#             'root': '/vehicle_repair_management/vehicle_repair_management',
#             'objects': http.request.env['vehicle_repair_management.vehicle_repair_management'].search([]),
#         })

#     @http.route('/vehicle_repair_management/vehicle_repair_management/objects/<model("vehicle_repair_management.vehicle_repair_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vehicle_repair_management.object', {
#             'object': obj
#         })
