# -*- coding: utf-8 -*-

from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    is_mechanic = fields.Boolean(string="Is a Mechanic", default=False)
    
    expertise_service_ids = fields.Many2many(
        'vehicle_repair_management.service',
        relation='hr_employee_expertise_service_rel',
        column1='employee_id',
        column2='service_id',
        string='Expertise Service'
    )
