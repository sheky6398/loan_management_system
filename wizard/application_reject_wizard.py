from odoo import models,fields

class ApplicationReject(models.TransientModel):
    _name = "application.reject.wizard"
    _description = "Reject the Loan Application Form"


    reason = fields.Text(string="Reason")

    def application_reject(self):     
        """This will send an email of loan application reject mail and also creat a loan application environment an also state move to Rejected"""
        template_id = self.env.ref('loan_management_system.application_reject_email_template')
        application_rejection_id = self.env.context.get('active_id')
        application_rejection_record = self.env['loan.application'].browse(application_rejection_id)
        application_rejection_record.message_post(body=self.reason) 
        template_id.send_mail(application_rejection_record.id, force_send=True)
        application_rejection_record.write({
            'state': 'rejected'
        })
        
