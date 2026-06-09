# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VehicleRepairManagement(models.Model):
    _name = 'vehicle_repair_management.vehicle_repair_management'
    _description = 'Vehicle Repair Work Order'

    # Header
    plate_number = fields.Char(string='Plate Number', required=True)
    
    # Customer
    client_id = fields.Many2one('res.partner', string='Client')
    phone = fields.Char(string='Phone', related='client_id.phone', readonly=False)
    email = fields.Char(string='Email', related='client_id.email', readonly=False)
    unknown_issue = fields.Boolean(string="I Don't Know What Needs To Be Done")
    
    # Basic Information
    receiving_date = fields.Datetime(string='Receiving Date', default=fields.Datetime.now)
    delivery_date = fields.Datetime(string='Delivery Date')
    vehicle_type = fields.Char(string='Vehicle Type')
    brand = fields.Char(string='Brand')
    
    # Issue
    work_description = fields.Text(string='Work Description')
    
    # Lainnya
    service_template = fields.Char(string='Service Template')
    service_team = fields.Char(string='Service Team')
    
    # Data Kendaraan
    vehicle_brand = fields.Char(string='Vehicle Brand')
    model = fields.Char(string='Model')
    color = fields.Char(string='Color')
    transmission_type = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], string='Transmission Type')
    year_of_manufacturing = fields.Char(string='Year of Manufacturing')
    warranty = fields.Boolean(string='Warranty')
    insurance = fields.Boolean(string='Insurance')
    pollution = fields.Boolean(string='Pollution')
    accomplished_date = fields.Date(string='Accomplished Date')
    last_change_oil = fields.Date(string='Last Change Oil')
    odometer_reading = fields.Float(string='Odometer Reading')
    
    # Bahan Bakar
    fuel_level = fields.Float(string='Fuel Level (%)')
    fuel_type = fields.Selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], string='Fuel Type')
    
    # Images
    image = fields.Image(string='Vehicle Image')
    
    # Accessories
    accessory_ids = fields.One2many('vehicle_repair_management.accessory', 'repair_id', string='Accessories Available In Vehicle')
