from odoo import models,fields,api
import logging
_logger = logging.getLogger(__name__)

class LoanType(models.Model):
    _name = 'loan.type'
    _description = 'Loan Type'


    def _default_currency_id(self):
        #It will give current company currency
        return self.env.user.company_id.currency_id


    name = fields.Char(string='Loan Type',required=True)
    terms_and_condition = fields.Text(string="Terms & conditions")
    maximum_loan_amount = fields.Monetary(string="Maximum Loan Amount",required=True)
    maximum_loan_term = fields.Selection([('6','6 Months'), ('12','12 Months'),('24','24 Months'),('36','36 Months'),('48','48 Months'),('60','60 Months')],default='6',string="Maximum Loan Term",required=True)
    currency_id = fields.Many2one('res.currency',string="Currency",default=_default_currency_id)


    def copy(self, default=None):
        """This will Copy the Existing record and also add the Duplicate in postfix of name
        and also add the Duplicate record in terms and condition field"""
        default = dict(default or {})
        default.update(
            terms_and_condition  = 'Duplicate Record',
            maximum_loan_term = '24',
            name=("%s (Duplicate)") % self.name)
        _logger.info(f'\nDefault={default}\n') 
        _logger.info(f'\nSelf={self}\n')     

        new_record = super(LoanType,self).copy(default=default)
        _logger.info(f'\nNew Record={new_record}\n')
        _logger.info(f'\nSelf={self}\n')     

        return new_record


    # def copy(self, default={}):
    #     default['name']=("%s (Duplicate)") % (self.name)
    #     new_record = super(LoanType,self).copy(default=default)
    #     _logger.info(f'\nNew Record={new_record}\n')
    #     _logger.info(f'\nDefault={default}\n')     
    #     _logger.info(f'\nSelf={self}\n')     

    #     return new_record


    @api.model
    def create(self,vals_list):
        #For Testing purpose, it will override a create method and add some default fields
        vals_list.update({'name':'education loan','maximum_loan_term':'36','maximum_loan_amount':500000},{'name':'health loan','maximum_loan_term':'36','maximum_loan_amount':500000})
        _logger.info(f'\n Vals_list:{vals_list} \n')
        record = super(LoanType,self).create(vals_list)  
        record['name'] = record.name.title()
        _logger.info(f'\n Vals_list:{vals_list} \n')
        _logger.info(f'\nSELF={self}\n')
        _logger.info(f'\nRecord={record}\n')

        return record