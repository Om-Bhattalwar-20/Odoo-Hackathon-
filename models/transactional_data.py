from odoo import models, fields, api
from odoo.exceptions import UserError

class EcosphereCarbonTransaction(models.Model):
    _name = 'ecosphere.carbon.transaction'
    _description = 'Carbon Transaction'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    department_id = fields.Many2one('ecosphere.department', string='Department')
    emission_factor_id = fields.Many2one('ecosphere.emission.factor', string='Emission Factor')
    value = fields.Float(string='Calculated Emission')
    date = fields.Date(string='Date', default=fields.Date.context_today)

class EcosphereCsrActivity(models.Model):
    _name = 'ecosphere.csr.activity'
    _description = 'CSR Activity'

    name = fields.Char(string='Title', required=True)
    category_id = fields.Many2one('ecosphere.category', string='Category', domain=[('type', '=', 'csr')])
    description = fields.Text(string='Description')
    points_reward = fields.Integer(string='Points Reward')
    date = fields.Date(string='Date')

class EcosphereEmployeeParticipation(models.Model):
    _name = 'ecosphere.employee.participation'
    _description = 'Employee Participation'

    employee_id = fields.Many2one('res.users', string='Employee', required=True)
    activity_id = fields.Many2one('ecosphere.csr.activity', string='Activity', required=True)
    proof = fields.Binary(string='Proof Document')
    points_earned = fields.Integer(string='Points Earned')
    completion_date = fields.Date(string='Completion Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved')
    ], string='Approval Status', default='draft')

    @api.constrains('state', 'proof')
    def _check_evidence_requirement(self):
        # Fetch the setting value from system parameters
        evidence_required = self.env['ir.config_parameter'].sudo().get_param('ecosphere.evidence_requirement')
        
        for record in self:
            # Only raise the error if the setting is True AND proof is missing
            if evidence_required and record.state == 'approved' and not record.proof:
                raise UserError("Evidence Requirement is enabled: You must attach proof before approving.")
            
    class EcosphereChallenge(models.Model):
     _name = 'ecosphere.challenge'
    _description = 'Sustainability Challenge'

    name = fields.Char(string='Title', required=True) 
    category_id = fields.Many2one('ecosphere.category', string='Category', domain=[('type', '=', 'challenge')]) 
    description = fields.Text(string='Description') 
    xp_reward = fields.Integer(string='XP Reward') 
    difficulty = fields.Selection([('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], string='Difficulty') 
    evidence_required = fields.Boolean(string='Evidence Required', default=True) 
    deadline = fields.Date(string='Deadline') 
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('active', 'Active'), 
        ('review', 'Under Review'),
        ('completed', 'Completed'), 
        ('archived', 'Archived')
    ], string='Status', default='draft') 

class EcosphereChallengeParticipation(models.Model):
    _name = 'ecosphere.challenge.participation'
    _description = 'Challenge Participation'

    challenge_id = fields.Many2one('ecosphere.challenge', string='Challenge', required=True) 
    employee_id = fields.Many2one('res.users', string='Employee', required=True) 
    progress = fields.Float(string='Progress (%)') 
    proof = fields.Binary(string='Proof Document') 
    approval_status = fields.Selection([('pending', 'Pending'), ('approved', 'Approved')], string='Approval') 
    xp_awarded = fields.Integer(string='XP Awarded') 

class EcosphereComplianceIssue(models.Model):
    _name = 'ecosphere.compliance.issue'
    _description = 'Compliance Issue'

    name = fields.Char(string='Description', required=True) 
    severity = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], string='Severity') 
    owner_id = fields.Many2one('res.users', string='Owner', required=True) 
    due_date = fields.Date(string='Due Date', required=True) 
    state = fields.Selection([('open', 'Open'), ('closed', 'Closed')], string='Status', default='open') 

class EcosphereDepartmentScore(models.Model):
    _name = 'ecosphere.department.score'
    _description = 'Department Score'

    department_id = fields.Many2one('ecosphere.department', string='Department', required=True) 
    env_score = fields.Float(string='Environmental Score') 
    soc_score = fields.Float(string='Social Score') 
    gov_score = fields.Float(string='Governance Score') 
    total_score = fields.Float(string='Total Score')

    def action_calculate_emission(self):
        # This checks if the setting is enabled
        auto_calc = self.env['ir.config_parameter'].sudo().get_param('ecosphere.auto_emission')
        if auto_calc:
            for record in self:
                # Logic: If an emission factor is linked, calculate the value
                if record.emission_factor_id:
                    # Simplified calculation logic for hackathon
                    record.value = record.emission_factor_id.carbon_value * 1.0