from odoo import models, fields

class EcosphereDepartment(models.Model):
    _name = 'ecosphere.department'
    _description = 'ESG Department Hierarchy'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    head_id = fields.Many2one('res.users', string='Department Head')
    parent_id = fields.Many2one('ecosphere.department', string='Parent Department')
    employee_count = fields.Integer(string='Employee Count')
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active')

class EcosphereCategory(models.Model):
    _name = 'ecosphere.category'
    _description = 'Shared ESG Category'

    name = fields.Char(string='Name', required=True)
    type = fields.Selection([
        ('csr', 'CSR Activity'),
        ('challenge', 'Challenge')
    ], string='Type', required=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active')

class EcosphereEmissionFactor(models.Model):
    _name = 'ecosphere.emission.factor'
    _description = 'Emission Factor'

    name = fields.Char(string='Name', required=True)
    carbon_value = fields.Float(string='Carbon Value (kg CO2)', required=True, help="Carbon values used during calculations")
    active = fields.Boolean(string='Active', default=True)

class EcosphereBadge(models.Model):
    _name = 'ecosphere.badge'
    _description = 'Gamification Badge'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    unlock_rule = fields.Integer(string='Unlock Rule (Target XP/Count)', required=True, help="Employee achievements threshold")
    icon = fields.Binary(string='Icon', attachment=True)

class EcosphereReward(models.Model):
    _name = 'ecosphere.reward'
    _description = 'Gamification Reward'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    points_required = fields.Integer(string='Points Required', required=True)
    stock_status = fields.Integer(string='Stock Status', default=0, help="Redeemable incentives available")