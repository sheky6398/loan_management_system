{
    'name': "Loan Management System",
    'author': 'Bharat Yadav',
    'version': '1.0.2',
    'summary': 'Employee can apply the form for Loan as per his requirement',
    'depends':['mail','hr','base','sale'],
    'data': [
        'report/sale_order_inherited.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'report/loan_application.xml',
        'report/loan_installment.xml',
        'report/report.xml',
        'views/loan_type_views.xml',
        'wizard/loan_installment_payment_wizard.xml',
        'data/application_confirm_mail_template.xml',
        'data/application_approved_mail_template.xml',
        'data/application_reject_mail_template.xml',
        'data/application_accepted_hr_mail_template.xml',
        'data/installment_payment_mail_template.xml',
        'wizard/application_accepted_wizard.xml',
        'wizard/application_reject_wizard.xml', 
        'views/loan_application_views.xml',       
        'views/loan_installment_views.xml',       
    ]

}