# -*- coding: utf-8 -*-

from odoo import models, fields

class Accessory(models.Model):
    _name = 'vehicle_repair_management.accessory'
    _description = 'Vehicle Accessory'

    repair_id = fields.Many2one('vehicle_repair_management.vehicle_repair_management', string='Repair Reference', required=True, ondelete='cascade')
    name = fields.Char(string='Name', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    description = fields.Char(string='Description')
