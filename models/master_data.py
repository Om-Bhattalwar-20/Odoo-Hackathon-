from odoo import models, fields
from odoo.exceptions import UserError
class ResUsers(models.Model):
    _inherit = 'res.users'
    
    # We give a default of 100 points so you can easily test redeeming rewards right away!
    esg_points = fields.Integer(string='ESG Points Balance', default=100)

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
    stock_status = fields.Integer(string='Stock Status', default=5, help="Redeemable incentives available")

    def action_redeem_reward(self):
        for reward in self:
            user = self.env.user
            # Rule 1: Check if the reward is out of stock
            if reward.stock_status <= 0:
                raise UserError("Out of Stock! This reward is currently unavailable.")
            
            # Rule 2: Check if the employee has enough points
            if user.esg_points < reward.points_required:
                raise UserError(f"Insufficient Points! You need {reward.points_required} points, but your current balance is only {user.esg_points}.")
            
            # Rule 3: Deduct points from employee balance and reduce stock
            user.esg_points -= reward.points_required
            reward.stock_status -= 1
            
            # Return a success notification pop-up
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Reward Redeemed!',
                    'message': f'You successfully redeemed {reward.name}. Remaining points: {user.esg_points}',
                    'type': 'success',
                    'sticky': False,
                }
            }    active = fields.Boolean(string='Active', default=True)

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
