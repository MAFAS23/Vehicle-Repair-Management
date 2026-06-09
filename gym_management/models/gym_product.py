from odoo import models, fields

class GymProductTemporary(models.TransientModel):
    _name = 'gym.product.temp'
    _description = 'Tampilan Produk Gym Sementara'

    name = fields.Char(string="Nama Produk")

class GymProduct(models.Model):
    _name = 'gym.product'
    _description = 'Data Produk Gym'

    name = fields.Char(string="Nama Produk", required=True) 