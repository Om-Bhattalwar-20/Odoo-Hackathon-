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