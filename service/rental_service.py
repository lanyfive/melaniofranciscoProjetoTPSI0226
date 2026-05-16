import database as db

class RentalService:
    def create_rental(self, customer_id: int, car_id: int, start_date: str, end_date: str):
        if not customer_id or not car_id or not start_date or not end_date:
            raise ValueError("ID do cliente, ID do carro, data de início e data de término são obrigatórios.")
        db.create_rental(customer_id, car_id, start_date, end_date)
        