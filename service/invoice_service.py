import database as db

class InvoiceService:
    
    def get_all_invoices(self):
        return db.get_all_invoices()
