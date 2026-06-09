# -*- coding: utf-8 -*-
from odoo import models, fields

class VehicleBrand(models.Model):
    _name = 'vehicle_repair_management.vehicle_brand'
    _description = 'Vehicle Brand'

    name = fields.Char(string='Brand Name', required=True)
    image = fields.Image(string='Image')
    vehicle_type_ids = fields.Many2many(
        'vehicle_repair_management.vehicle_type', 
        relation='vehicle_brand_type_rel', 
        column1='brand_id', 
        column2='type_id', 
        string='Manufactured Vehicle Types'
    )
