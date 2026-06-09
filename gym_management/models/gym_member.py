from odoo import models, fields, api

class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Data Anggota Gym'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Nama', required=True, tracking=True)
    phone = fields.Char(string='Telepon', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    user_id = fields.Many2one('res.users', string='Salesperson', tracking=True)
    city = fields.Char(string='Kota', tracking=True)
    country_id = fields.Many2one('res.country', string='Negara', tracking=True)
    company_id = fields.Many2one('res.company', string='Perusahaan', 
                                default=lambda self: self.env.company, tracking=True)
    active = fields.Boolean(string='Aktif', default=True)
    
    _sql_constraints = [
        ('email_uniq', 'unique(email)', 'Email harus unik!')
    ] 