from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VehicleRepairManagement(models.Model):
    _name = 'vehicle_repair_management.vehicle_repair_management'
    _description = 'Vehicle Repair Work Order'

    # Sequence
    name = fields.Char(string='Work Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')

    # State
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('under_process', 'Under Process'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, default='draft')

    # Header
    saved_vehicle_id = fields.Many2one('vehicle_repair_management.saved_vehicle', string='Plate Number', required=True)
    
    # Customer
    client_id = fields.Many2one('res.partner', string='Client', related='saved_vehicle_id.customer_id', readonly=False, store=True)
    phone = fields.Char(string='Phone', related='client_id.phone', readonly=False)
    email = fields.Char(string='Email', related='client_id.email', readonly=False)
    unknown_issue = fields.Boolean(string="I Don't Know What Needs To Be Done")
    
    # Basic Information
    receiving_date = fields.Datetime(string='Receiving Date', default=fields.Datetime.now)
    delivery_date = fields.Datetime(string='Delivery Date')
    vehicle_type_id = fields.Many2one('vehicle_repair_management.vehicle_type', string='Vehicle Type', related='saved_vehicle_id.vehicle_type_id', readonly=False, store=True)
    brand_id = fields.Many2one('vehicle_repair_management.vehicle_brand', string='Brand', related='saved_vehicle_id.brand_id', readonly=False, store=True)
    
    # Issue
    work_description = fields.Text(string='Work Description')
    
    # Lainnya
    service_template_id = fields.Many2one('vehicle_repair_management.service_template', string='Service Template')
    service_team_id = fields.Many2one('vehicle_repair_management.service_team', string='Service Team')
    team_leader_id = fields.Many2one('hr.employee', string='Team Leader')
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string='Priority')
    
    # Data Kendaraan
    model = fields.Char(string='Model', related='saved_vehicle_id.model', readonly=False, store=True)
    color = fields.Char(string='Color', related='saved_vehicle_id.color', readonly=False, store=True)
    transmission_type = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], string='Transmission Type', related='saved_vehicle_id.transmission', readonly=False, store=True)
    year_of_manufacturing = fields.Char(string='Year of Manufacturing', related='saved_vehicle_id.year', readonly=False, store=True)
    warranty = fields.Boolean(string='Warranty')
    insurance = fields.Boolean(string='Insurance')
    pollution = fields.Boolean(string='Pollution')
    accomplished_date = fields.Date(string='Accomplished Date')
    last_change_oil = fields.Date(string='Last Change Oil')
    odometer_reading = fields.Float(string='Odometer Reading')
    
    # Bahan Bakar
    fuel_level = fields.Float(string='Fuel Level (%)')
    fuel_type_id = fields.Many2one('vehicle_repair_management.vehicle_fuel_type', string='Fuel Type', related='saved_vehicle_id.fuel_type_id', readonly=False, store=True)
    
    # Images
    image = fields.Image(string='Vehicle Image')
    
    # Tabs
    worksheet_line_ids = fields.One2many('vehicle_repair_management.worksheet_line', 'repair_id', string='Worksheet')
    part_line_ids = fields.One2many('vehicle_repair_management.part_line', 'repair_id', string='Part Used')
    accessory_ids = fields.One2many('vehicle_repair_management.accessory', 'repair_id', string='Accessories Available In Vehicle')
    
    # Totals
    notes = fields.Text(string='Notes / Description')
    worksheets_expenses = fields.Float(string='Worksheets Expenses', compute='_compute_totals', store=True)
    used_part_expenses = fields.Float(string='Used Part Expenses', compute='_compute_totals', store=True)
    estimated_repair_untaxed_expenses = fields.Float(string='Estimated Repair Untaxed Expenses', compute='_compute_totals', store=True)

    @api.depends('worksheet_line_ids.subtotal', 'part_line_ids.subtotal')
    def _compute_totals(self):
        for rec in self:
            ws_exp = sum(line.subtotal for line in rec.worksheet_line_ids)
            pt_exp = sum(line.subtotal for line in rec.part_line_ids)
            rec.worksheets_expenses = ws_exp
            rec.used_part_expenses = pt_exp
            rec.estimated_repair_untaxed_expenses = ws_exp + pt_exp

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.repair.work.order') or 'New'
        return super(VehicleRepairManagement, self).create(vals)

    @api.onchange('service_template_id')
    def _onchange_service_template(self):
        if self.service_template_id:
            self.service_team_id = self.service_template_id.team_id
            self.team_leader_id = self.service_template_id.team_id.team_leader_id
            
            # Auto-populate worksheet
            lines = []
            for t_line in self.service_template_id.line_ids:
                lines.append((0, 0, {
                    'mechanic_id': t_line.mechanic_id.id,
                    'service_id': t_line.service_id.id,
                    'description': t_line.description,
                    'cost_type': t_line.cost_type,
                    'cost': t_line.cost,
                    'uom': t_line.uom,
                    'quantity': t_line.quantity,
                    'work_time': t_line.work_time,
                }))
            # Reset existing lines and append new
            self.worksheet_line_ids = [(5, 0, 0)] + lines

    def action_confirm(self):
        self.state = 'confirmed'

    def action_under_process(self):
        self.state = 'under_process'

    def action_done(self):
        self.state = 'done'
        
        SaleOrder = self.env['sale.order']
        order_lines = []
        
        for ws in self.worksheet_line_ids:
            if ws.service_id.product_id:
                order_lines.append((0, 0, {
                    'product_id': ws.service_id.product_id.id,
                    'name': ws.description or ws.service_id.name,
                    'product_uom_qty': ws.quantity,
                    'price_unit': ws.cost,
                }))
        
        for part in self.part_line_ids:
            if part.product_id:
                order_lines.append((0, 0, {
                    'product_id': part.product_id.id,
                    'name': part.description or part.product_id.name,
                    'product_uom_qty': part.quantity,
                    'price_unit': part.unit_price,
                }))
                
        if order_lines:
            # Lakukan pengecekan stok terakhir sebelum membuat SO
            for line in order_lines:
                product = self.env['product.product'].browse(line[2]['product_id'])
                qty = line[2]['product_uom_qty']
                if product.type == 'product' and product.qty_available < qty:
                    raise ValidationError("Stok untuk produk '%s' tidak mencukupi! Tersedia: %s, Dibutuhkan: %s. Silakan restock terlebih dahulu." % (product.name, product.qty_available, qty))

            so = SaleOrder.create({
                'partner_id': self.client_id.id,
                'origin': self.name,
                'order_line': order_lines,
            })
            
            so.action_confirm()
            
            for picking in so.picking_ids:
                for move in picking.move_ids:
                    move.quantity_done = move.product_uom_qty
                picking.button_validate()
            
            invoice = so._create_invoices()
            invoice.action_post()
        
    def action_cancel(self):
        self.state = 'cancel'


class WorksheetLine(models.Model):
    _name = 'vehicle_repair_management.worksheet_line'
    _description = 'Worksheet Line'

    repair_id = fields.Many2one('vehicle_repair_management.vehicle_repair_management', string='Repair', required=True, ondelete='cascade')
    mechanic_id = fields.Many2one('hr.employee', string='Mechanic')
    service_id = fields.Many2one('vehicle_repair_management.service', string='Service', required=True)
    description = fields.Char(string='Description')
    cost_type = fields.Selection([('fix', 'FIX'), ('price_values', 'price values'), ('free', 'free')], string='Cost Type')
    cost = fields.Float(string='Cost')
    uom = fields.Char(string='Abstract Uom')
    quantity = fields.Float(string='Quantity', default=1.0)
    work_time = fields.Float(string='Work Time')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('cost', 'quantity')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.cost * line.quantity

    @api.onchange('service_id', 'quantity')
    def _onchange_service_id(self):
        if self.service_id:
            # Cek stok secara live di layar (UI)
            if self.service_id.product_id and self.service_id.product_id.type == 'product':
                if self.service_id.product_id.qty_available < self.quantity:
                    warning = {
                        'title': 'Stok Tidak Mencukupi!',
                        'message': 'Stok untuk barang %s tidak cukup (Tersisa: %s). Silakan kurangi Quantity atau restock terlebih dahulu.' % (self.service_id.product_id.name, self.service_id.product_id.qty_available)
                    }
                    self.quantity = self.service_id.product_id.qty_available
                    return {'warning': warning}
            
            self.cost_type = self.service_id.cost_type
            self.cost = self.service_id.price
            self.uom = self.service_id.unit
            self.description = self.service_id.name

class PartLine(models.Model):
    _name = 'vehicle_repair_management.part_line'
    _description = 'Part Used Line'

    repair_id = fields.Many2one('vehicle_repair_management.vehicle_repair_management', string='Repair', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Part', domain=[('is_vehicle_part', '=', True)])
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Qty', default=1.0)
    unit_price = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.onchange('product_id', 'quantity')
    def _onchange_product_id(self):
        if self.product_id:
            # Cek stok secara live di layar (UI)
            if self.product_id.type == 'product':
                if self.product_id.qty_available < self.quantity:
                    warning = {
                        'title': 'Stok Tidak Mencukupi!',
                        'message': 'Stok untuk barang %s tidak cukup (Tersisa: %s). Silakan kurangi Quantity atau restock terlebih dahulu.' % (self.product_id.name, self.product_id.qty_available)
                    }
                    self.quantity = self.product_id.qty_available
                    return {'warning': warning}
            
            self.description = self.product_id.name
            self.unit_price = self.product_id.lst_price
