from odoo import models,fields,api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class EmployeeInherited(models.Model):
    _inherit = "hr.employee"


    gender = fields.Selection([('none','None'),('male','Male')])




    # @api.onchange('mobile_phone')   
    # def _onchange_mobile_phone(self):
    #     if len(self.mobile_phone) != 10 :
    #         _logger.info(f'\nPhone NUmber={type(self.mobile_phone)}\n')

    #         raise UserError('Phone Number must be 10 digit')


    # @api.model
    # def create(self,vals_list):
    #     record = super(EmployeeInherited,self).create(vals_list)   
    #     _logger.info(f'\nRecord={record}\n')
    #     _logger.info(f'\nSELF={self}\n')
    #     _logger.info(f'\nVals List={vals_list}\n')
    #     for rec in record:
    #         if len(rec.mobile_phone) != 10 :
    #             raise ValidationError('Phone Number must be 10 digit')
    #     return record

    # def write(self,vals):
    #     record = super(EmployeeInherited,self).write(vals)
    #     _logger.info(f'\n RECORD {record} \n')
    #     _logger.info(f'\nSELF={self}\n')
    #     _logger.info(f'\nVals ={vals}\n')

    #     for rec in self:
    #         if len(rec.mobile_phone) != 10 :
    #             raise ValidationError('Phone Number must be 10 digit')
    #     return record

    # @api.model
    # def create(self,vals_list):
    #     # vals_list.update({'mobile_phone':123487852,'work_phone':113543,'gender':'none'})

    #     _logger.info(f'\n Student is being created by following details:{vals_list} \n')
    #     record = super(EmployeeInherited,self).create(vals_list)  
    #     vals_list['name'] = record.name.title()
    #     _logger.info(f'\nSELF={self}\n')

    #     return record


    def write(self,bharat):
        bharat.update({'mobile_phone':123487852,'work_phone':113543,'gender':'none'})
        # bharat['name'] = self.name.title()
        _logger.info(f'\nSELF={self}\n')
        _logger.info(f'\nVals={bharat}\n')
        updated_record = super(EmployeeInherited,self).write(bharat)
        _logger.info(f'\nUpdated Record={updated_record}\n')
        return updated_record

