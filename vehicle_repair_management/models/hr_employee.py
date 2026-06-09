# -*- coding: utf-8 -*-

from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    is_mechanic = fields.Boolean(string="Is a Mechanic", default=False)
