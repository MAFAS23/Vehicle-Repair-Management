# -*- coding: utf-8 -*-
from odoo import models, fields

class SavedVehicle(models.Model):
    _name = 'vehicle_repair_management.saved_vehicle'
    _description = 'Saved Vehicle'
    _rec_name = 'plate_no'

    plate_no = fields.Char(string='Plate No', required=True)
    
    # Customer Detail
    customer_id = fields.Many2one('res.partner', string='Customer')
    phone = fields.Char(related='customer_id.phone', string='Phone', readonly=False)
    email = fields.Char(related='customer_id.email', string='Email', readonly=False)
    
    # Vehicle Detail
    vehicle_type_id = fields.Many2one('vehicle_repair_management.vehicle_type', string='Vehicle Type')
    brand_id = fields.Many2one('vehicle_repair_management.vehicle_brand', string='Brand')
    model = fields.Char(string='Model')
    year = fields.Char(string='Year of Manufacturing')
    color = fields.Char(string='Color')
    transmission = fields.Selection([('automatic', 'Automatic'), ('manual', 'Manual')], string='Transmission Type')
    fuel_type_id = fields.Many2one('vehicle_repair_management.vehicle_fuel_type', string='Fuel Type')
