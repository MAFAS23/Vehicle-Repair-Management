# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ServiceTemplate(models.Model):
    _name = 'vehicle_repair_management.service_template'
    _description = 'Service Template'

    name = fields.Char(string='Title/Name', required=True)
    active = fields.Boolean(string='Status Active', default=True)
    
    vehicle_type_id = fields.Many2one('vehicle_repair_management.vehicle_type', string='Vehicle Type')
    brand_id = fields.Many2one('vehicle_repair_management.vehicle_brand', string='Vehicle Brand')
    team_id = fields.Many2one('vehicle_repair_management.service_team', string='Repair Team')
    member_ids = fields.Many2many(
        'hr.employee',
        relation='service_template_hr_employee_rel',
        column1='template_id',
        column2='employee_id',
        string='Team Member'
    )
    
    line_ids = fields.One2many('vehicle_repair_management.service_template_line', 'template_id', string='Service / Repair Work')


class ServiceTemplateLine(models.Model):
    _name = 'vehicle_repair_management.service_template_line'
    _description = 'Service Template Line'

    template_id = fields.Many2one('vehicle_repair_management.service_template', required=True, ondelete='cascade')
    mechanic_id = fields.Many2one('hr.employee', string='Mechanic')
    service_id = fields.Many2one('vehicle_repair_management.service', string='Service', required=True)
    description = fields.Char(string='Description')
    cost_type = fields.Selection([
        ('fix', 'FIX'),
        ('price_values', 'price values'),
        ('free', 'free')
    ], string='Cost Type')
    cost = fields.Float(string='Cost')
    uom = fields.Char(string='Abstract Uom')
    quantity = fields.Float(string='Quantity', default=1.0)
    work_time = fields.Float(string='Work Time')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('cost', 'quantity')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.cost * line.quantity
            
    @api.onchange('service_id')
    def _onchange_service_id(self):
        if self.service_id:
            self.cost_type = self.service_id.cost_type
            self.cost = self.service_id.price
            self.uom = self.service_id.unit
            self.description = self.service_id.name
