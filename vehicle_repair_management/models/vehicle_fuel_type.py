# -*- coding: utf-8 -*-
from odoo import models, fields

class VehicleFuelType(models.Model):
    _name = 'vehicle_repair_management.vehicle_fuel_type'
    _description = 'Vehicle Fuel Type'

    name = fields.Char(string='Fuel Type', required=True)
