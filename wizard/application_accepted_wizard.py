from odoo import models,fields
from datetime import *
from dateutil.relativedelta import *
import logging
_logger = logging.getLogger(__name__)


class ApplicationAccepted(models.TransientModel):
    _name = "application.accepted.wizard"
    _description = "Accept the Loan Application Form"


    approval_comment = fields.Text(string="Approval Comment")

    def application_accepted(self):  
        #This will send an email of Loan Application Accepted 
        template_id = self.env.ref('loan_management_system.application_accepted_hr_email_template')
        #create a environment of loan application 
        application_accepted_id = self.env.context.get('active_id')
        application_accepted_record = self.env['loan.application'].browse(application_accepted_id)
        application_accepted_record.message_post(body=self.approval_comment) 
        template_id.send_mail(application_accepted_record.id, force_send=True)
        application_accepted_record.accountant_id = self.env.user.employee_id.id
        application_accepted_record.write({
            'state': 'accepted'
        })
        active_no_of_installments = application_accepted_record.no_of_installments
        active_monthly_emi = application_accepted_record.monthly_emi
        current_date = date.today()
        current_month = current_date + relativedelta(months=+1)

        for i in range(int(application_accepted_record.no_of_installments)):    
            #Create a loan instalment where monthly emi would be increase by 1 month for every installment       
            next_month = current_month + relativedelta(months=+i)           
            create_installment = self.env['loan.installment'].create({ 
            'application_id' : application_accepted_record.id,
            'monthly_emi' : active_monthly_emi,
            'date_due' : next_month,
            'state': 'pending', 
            })
            _logger.info(f'\n installment={type(application_accepted_record.no_of_installments)}\n')
            




        



        
