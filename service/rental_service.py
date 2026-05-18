import database as db

class RentalService:
    
    def create_rental(self, customer_id: int, car_id: int, start_date: str, end_date: str, total_cost: float):
        if not customer_id or not car_id or not start_date or not end_date:
            raise ValueError("ID do cliente, ID do carro, data de início e data de término são obrigatórios.")
        db.create_rental(customer_id, car_id, start_date, end_date, total_cost)

    def update_rental(self, rental_id: int, customer_id: int, car_id: int, start_date: str, end_date: str, total_cost: float):
        if not rental_id:
            raise ValueError("ID do aluguel é obrigatório.")
        if not customer_id or not car_id or not start_date or not end_date:
            raise ValueError("ID do cliente, ID do carro, data de início e data de término são obrigatórios.")
        db.update_rental(rental_id, customer_id, car_id, start_date, end_date, total_cost)

    def delete_rental(self, rental_id: int):
        if not rental_id:
            raise ValueError("ID do aluguel é obrigatório.")
        db.delete_rental(rental_id)

    def get_all_rentals(self):
        return db.get_all_rentals()
