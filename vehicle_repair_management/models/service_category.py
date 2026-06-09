# -*- coding: utf-8 -*-

from odoo import models, fields

class ServiceCategory(models.Model):
    _name = 'vehicle_repair_management.service_category'
    _description = 'Service Category'

    name = fields.Char(string='Category Name', required=True)
