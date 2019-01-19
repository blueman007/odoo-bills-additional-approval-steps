# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo import api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    #state = fields.Selection(selection_add=[('g_m_approve', 'G.M. Approve'),('f_m_approve', 'F.M. Approve')])
    
    state = fields.Selection([
            ('g_m_approve', 'G.M. Approve'),
            ('f_m_approve', 'F.M. Approve'),
            ('draft','Draft'),
            ('open', 'Open'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")
    
    @api.one
    def general_manager_approval(self):
        self.write({'state': 'g_m_approve'})
        
    @api.one
    def financial_manager_approval(self):
        self.write({'state': 'f_m_approve'})
        
        
    

    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: inv.state != 'f_m_approve'):
            raise UserError(_("Invoice must be in Financial Manager Approve state in order to validate it."))
        if to_open_invoices.filtered(lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        return to_open_invoices.invoice_validate()