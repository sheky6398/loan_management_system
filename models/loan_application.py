from odoo import models,fields,api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Application form"
    _inherit = ['mail.thread','mail.activity.mixin']

    def _default_currency_id(self):
        #It will give current company currency
        _logger.info(f'\n Currency={self.env.user.company_id.currency_id.name}\n')
        return self.env.user.company_id.currency_id
    
    def _default_employee_id(self):
        #It will give current user name 
        _logger.info(f'\n employee_id={self.env.user.employee_id.name}\n')
        return self.env.user.employee_id.id


    name = fields.Char(string="Loan Sequence",default=lambda self: ('New'),readonly=True,required=True)
    employee_id = fields.Many2one('hr.employee',string="Employee Name",required=True,default=_default_employee_id)
    department_id = fields.Many2one(string="Department",related='employee_id.department_id')
    job_title = fields.Char(string="Job Title",related='employee_id.job_title')
    manager_id = fields.Many2one('hr.employee',string="Manager")
    maximum_loan_amount = fields.Monetary(string="Maximum Loan Amount",related="loan_type_id.maximum_loan_amount")
    loan_amount = fields.Monetary(string="Loan Amount",required=True)
    currency_id = fields.Many2one("res.currency",string="Currency",default=_default_currency_id)
    loan_type_id = fields.Many2one('loan.type',string="Loan Type")
    no_of_installments = fields.Selection([('6','6 Months'), ('12','12 Months'),('24','24 Months'),('36','36 Months'),('48','48 Months'),('60','60 Months')],string="Term (Months)",default='12',required=True)
    monthly_emi = fields.Monetary(string="Monthly Emi",compute="_compute_monthly_emi")
    note = fields.Html(string="Note")
    state = fields.Selection([('draft','Draft'),('requested','Requested'),('submit_for_review','Submit For Review'),('accepted','Accepted'),('rejected','Rejected')],default='draft',string='Status')
    document = fields.Binary(string="Document",help="Upload Your Documents")
    document_type = fields.Selection([('voter_id','Voter id'),('aadhar_card','Aadhar_card'),('pan_card','Pan Card')],default='pan_card')
    installment_ids = fields.One2many('loan.installment','application_id', string="Installments")
    date_request = fields.Date(string='Requested Date', readonly=True,default=fields.Date.today())
    installment_ids = fields.One2many('loan.installment','application_id',string='Installments')
    installment_count = fields.Integer(string='Installment Count', compute='_compute_installment_count')
    date_created = fields.Date(string='Created Date',default=fields.Date.today(),readonly=True)
    accountant_id = fields.Many2one('hr.employee',string='Accountant')




    @api.depends('loan_amount','no_of_installments' )
    def _compute_monthly_emi(self):
        """It will Calculate Monthly Emi field which will come by dividing Loan Amount into No of Installments"""
        for record in self:
            if int(record.loan_amount) > 1 and int(record.no_of_installments) > 1:
                record.monthly_emi = int(record.loan_amount) / int(record.no_of_installments)
                _logger.info(f'\n compute={record.monthly_emi}\n')
                _logger.info(f'\n Record={record}\n')
                _logger.info(f'\n Self={self}\n')
            else:
                record.monthly_emi = 0

    @api.constrains('loan_amount')
    def _check_loan_amount(self):
        #It will Raise an Error when Loan Amount is greater than Maximum Loan Amount
        if self.loan_amount > self.maximum_loan_amount:
            _logger.info(f'\n Maximum ={type(self.maximum_loan_amount)}\n')
            _logger.info(f'\n Maximum ={(self.maximum_loan_amount)}\n')

            raise ValidationError(" You can't entered the amount that is greater than Maximum Loan amount ") 

    @api.onchange('employee_id')   
    def _onchange_employee_id(self):
        # If Employee id is found than it will give related Manager id 
        if self.employee_id:
            self.manager_id = self.employee_id.parent_id.id
            _logger.info(f'\n Manager id ={(self.employee_id.parent_id.name)}\n')

 
    @api.onchange('no_of_installments')   
    def _onchange_no_of_installments(self):
        if self.loan_type_id.name:
            """It will check maximum Loan term if user choose select greater months tham raise an error"""
            if int(self.no_of_installments) > int(self.loan_type_id.maximum_loan_term):
                _logger.info(f'\n installment={type(self.no_of_installments)} \n')
                _logger.info(f'\n term={self.loan_type_id.maximum_loan_term} \n')
                raise ValidationError(f"For {self.loan_type_id.name} maximum limit is {self.loan_type_id.maximum_loan_term} Months and you can't choose the limit that is greater than Maximum Limit ")

    @api.model
    def create(self,vals):
        #It will give a sequence number 
        if vals.get('name', ('New')) == ('Old'):
            vals['name'] = self.env['ir.sequence'].next_by_code('loan.application.sequence') or ('New')
        result = super(LoanApplication, self).create(vals)
        _logger.info(f'\n Result={result} \n')
        return result

    def action_open_installments(self):
        #It wiil open Loan Installments 
        return {
            'type': 'ir.actions.act_window',
            'name': 'Installments',
            'res_model': 'loan.installment',
            'domain': [('application_id', '=', self.id)],
            'view_mode': 'kanban,tree,form',
            'target': 'current',
        }

    def _compute_installment_count(self):
        #It will count loan installments 
        for rec in self:
            installment_count = self.env['loan.installment'].search_count([('application_id', '=', rec.id)])
            rec.installment_count = installment_count

    def requested_method(self):
        #This will send an Email of Loan Application Requested
        template_id = self.env.ref('loan_management_system.application_confirm_email_template')
        template_id.send_mail(self.id, force_send=True)
        #It will move state Draft to Requested
        self.state="requested"
        #This will check Manager_id field if not than raise an error
        if not self.manager_id:
            _logger.info(f'\n EMPTY ={not self.manager_id}\n')
            raise ValidationError("Manager name can't be empty ")


    
    def submit_for_review_method(self):
        #This will send an Email of Loan Application submit_for_review 
        template_id = self.env.ref('loan_management_system.application_approved_email_template')
        template_id.send_mail(self.id, force_send=True)
        #It will move state Requested to submit_for_review
        self.state = 'submit_for_review'

    # def write(self,vals):
    #     _logger.info(f'\n Update {vals} \n')
    #     record = super(LoanApplication,self).write(vals)
    #     _logger.info(f'\n RECORD {record} \n')
    #     _logger.info(f'\nEmployee={self.manager_id.user_id}\n')
    #     return record



    def action_url(self):
        #It will open the Website URL
        return {
            'type':'ir.actions.act_url',
            'target': 'new',
            'url' : 'https://www.google.co.in',
        }






