import database as db

class InvoiceService:

    def get_all_invoices(self):
        return db.get_all_invoices()

    def pay_invoice(self, invoice_id):
        if not invoice_id:
            raise ValueError("ID da fatura é obrigatório.")
        db.update_invoice(invoice_id)