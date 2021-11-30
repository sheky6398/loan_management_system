from odoo import models,fields,api
from datetime import *
import logging

_logger = logging.getLogger(__name__)


class LoanInstallment(models.Model):
    _name = 'loan.installment'
    _description = 'Installments for Loan'
    _inherit = ['mail.thread','mail.activity.mixin']


    def _default_currency_id(self):
        #It will give current company currency
        return self.env.user.company_id.currency_id

    name = fields.Char(string="Installment Reference",default=lambda self: ('New'),readonly=True)
    application_id = fields.Many2one('loan.application',string="Application Number ",readonly=True)
    monthly_emi = fields.Monetary(string="Monthly Emi",readonly=True)
    currency_id = fields.Many2one('res.currency',string="Currency", default=_default_currency_id)
    date_due = fields.Date(string='Due Date',readonly=True)
    state = fields.Selection([('pending','Pending'),('overdue','Overdue'),('paid','Paid')],default="pending",string="status",compute="_compute_state",store=True)
    date_paid = fields.Date(string="Paid Date", default=fields.Date.today(),readonly=True)
    mode = fields.Selection([('online','Online'),('cash','Cash'),('cheque','Cheque')], default='cash', string="Mode")
    note = fields.Text(string="Note")    


    _logger.info(f'application={application_id}')
    application = application_id.name
    def name_get(self):
        result = []
        for rec in self:
            name = str(rec.application_id.name) + '-' + rec.name
            _logger.info(f'\nAPPLICATION={self.application_id.name}\n')
            _logger.info(f'\nAPPLICATION={name}\n')
            result.append((rec.id, name))
            _logger.info(f'\ntoday daye ={date.today()}\n')
            _logger.info(f'\ndate day ={self.date_due}\n')
            
        return result

    @api.model
    def create(self,vals):
        #It will give a sequence number 
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('loan.installment.sequence') or ('New')
        result = super(LoanInstallment, self).create(vals)
        return result

    def action_paid(self):
        #it will move state to Paid
        for rec in self:
            rec.state = 'paid'
            _logger.info(f'\n State ={rec.state}\n')  



    @api.depends('state','date_due')
    def _compute_state(self):
        #It will check if due date is greater than current date than state move to Overdue 
        for rec in self:
            if date.today() > rec.date_due:
                rec.state = 'overdue'
                _logger.info(f'\n COMPUTE ={date.today() > rec.date_due}\n')   
                _logger.info(f'\n State ={rec.state}\n')  
            else:
                rec.state = 'pending' 
        


