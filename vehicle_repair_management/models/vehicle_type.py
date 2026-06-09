# -*- coding: utf-8 -*-
from odoo import models, fields

class VehicleType(models.Model):
    _name = 'vehicle_repair_management.vehicle_type'
    _description = 'Vehicle Type'

    name = fields.Char(string='Type Name', required=True)
