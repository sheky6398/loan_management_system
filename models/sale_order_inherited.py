from odoo import models
from odoo.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    

    def action_confirm(self):
        #For testing purpose, it will check if delivery address is not found than raise an error
        for rec in self:
            if not rec.partner_shipping_id.city :
                raise Warning("Please Enter City Name in Delivery Address")
            else:
                super(SaleOrder,self).action_confirm()