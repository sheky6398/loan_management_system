from odoo import models,fields
import logging
_logger = logging.getLogger(__name__)


class InstallmentPayment(models.TransientModel):
    _name = "loan.installment.payment.wizard"
    _description = "Loan Installment Payment"


    def _default_currency_id(self):
        #This will give current company currency
        return self.env.user.company_id.currency_id

    def _default_name(self):
        #This will give default name of loan installment 
        active_employee_id = self.env.context.get('active_id')
        active_employee_record = self.env['loan.installment'].browse(active_employee_id)
        _logger.info(f'\n  NAME {active_employee_record.name}\n')
        return active_employee_record.name

    def _default_application_id(self):
        #This will give default Application of loan installment 
        active_employee_id = self.env.context.get('active_id')
        active_employee_record = self.env['loan.installment'].browse(active_employee_id)
        return active_employee_record.application_id


    name = fields.Char(string="Installment Reference",readonly=True,default=_default_name)
    currency_id = fields.Many2one('res.currency',string="Currency", default=_default_currency_id)
    date_payment = fields.Date(string="Payment Date", default=fields.Date.today(),readonly="1")
    mode = fields.Selection([('cash','Cash'), ('online','Online'), 
                                ('cheque','Cheque')],default='cash',required=True)
    monthly_emi = fields.Monetary(string="Monthly Emi",related="application_id.monthly_emi",readonly="1")
    application_id = fields.Many2one('loan.application',string="Application Number ",default=_default_application_id)
    note = fields.Text(string="Note")    


    def action_payment(self):
        active_employee_id = self.env.context.get('active_id')
        active_employee_record = self.env['loan.installment'].browse(active_employee_id)
        _logger.info(f'\n  ACTIVE EMPLOYEE {active_employee_id}\n')
        _logger.info(f'\n  ACTIVE NAME {active_employee_record.name}\n')
        _logger.info(f'\n  MODE {self.mode}\n')
        _logger.info(f'\n  EMI {self.monthly_emi}\n')
        _logger.info(f'\n  EMPLOYEE MAIL ID {self.env.user.employee_id.work_email}\n')
        _logger.info(f'\n  ACCOUNTANT {self}\n')
        active_payment = active_employee_record .write({
            'mode': self.mode,
            'monthly_emi': self.monthly_emi,
            'date_paid' : self.date_payment,
            'note' : self.note
        })
        template_id = self.env.ref('loan_management_system.installment_payment_email_template')
        _logger.info(f'\n TEMPLATE ID {template_id}\n')
        template_id.send_mail(active_employee_record.id, force_send=True)


