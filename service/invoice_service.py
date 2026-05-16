import database as db

class InvoiceService:
    def create_invoice(self, rental_id: int, issue_date: str, amount: float):
        if not rental_id or not issue_date or not amount:
            raise ValueError("ID de aluguer, data de emissão e valor são obrigatórios.")
        db.create_invoice(rental_id, issue_date, amount)
        