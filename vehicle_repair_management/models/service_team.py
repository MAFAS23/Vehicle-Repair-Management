# -*- coding: utf-8 -*-
from odoo import models, fields

class ServiceTeam(models.Model):
    _name = 'vehicle_repair_management.service_team'
    _description = 'Service Team'

    name = fields.Char(string='Team Name', required=True)
    image = fields.Image(string="Image")
    team_leader_id = fields.Many2one('hr.employee', string='Team Leader')
    service_ids = fields.Many2many(
        'vehicle_repair_management.service', 
        relation='service_team_service_rel', 
        column1='team_id', 
        column2='service_id', 
        string='Vehicle Service'
    )
    description = fields.Text(string='Team Description')
    
    member_ids = fields.Many2many(
        'hr.employee', 
        relation='service_team_hr_employee_rel', 
        column1='team_id', 
        column2='employee_id', 
        string='Team Members'
    )
