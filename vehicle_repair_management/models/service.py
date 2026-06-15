# -*- coding: utf-8 -*-

from odoo import models, fields

class VehicleService(models.Model):
    _name = 'vehicle_repair_management.service'
    _description = 'Vehicle Repair Service'

    name = fields.Char(string='Name', required=True)
    product_id = fields.Many2one('product.product', string='Product')
    price = fields.Float(string='Price')
    unit = fields.Char(string='Unit', help="e.g. Tire, Hour, Piece")
    vehicle_type_ids = fields.Many2many(
        'vehicle_repair_management.vehicle_type', 
        relation='service_vehicle_type_rel', 
        column1='service_id', 
        column2='vehicle_type_id', 
        string='Service For Vehicle Type'
    )
    description = fields.Text(string='Description')
    service_category_id = fields.Many2one('vehicle_repair_management.service_category', string='Service Category')
    cost_type = fields.Selection([
        ('fix', 'FIX'),
        ('price_values', 'price values'),
        ('free', 'free')
    ], string='Cost Type', default='fix')
