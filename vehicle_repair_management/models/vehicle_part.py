# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_vehicle_part = fields.Boolean(string="Is a Vehicle Part", default=False)
