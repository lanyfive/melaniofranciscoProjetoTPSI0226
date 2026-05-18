import re
from datetime import datetime
import database as db

class CarService:
    _PLATE_PATTERN = re.compile(
        r"^("
        r"[A-Z]{2}-\d{2}-\d{2}|"
        r"\d{2}-[A-Z]{2}-\d{2}|"
        r"\d{2}-\d{2}-[A-Z]{2}|"
        r"[A-Z]{2}-\d{2}-[A-Z]{2}|"
        r"[A-Z]{2}-\d{3}-[A-Z]{2}"
        r")$")
    
    def _validate_price(self, price):
        try:
            price = float(price)
        except ValueError:
            raise ValueError("Preço inválido. Exemplo: 10 ou 10.99")
        
        if price <= 0:
            raise ValueError("Preço deve ser um valor positivo.")
        if not re.match(r"^\d+(\.\d{1,2})?$", str(price)):
            raise ValueError("Preço inválido. Exemplo: 10 ou 10.99")
    
    def _validate_year(self, year):
        try:
            year = int(year)
        except ValueError:
            raise ValueError("Ano inválido. Insira um número.")
        
        current_year = datetime.now().year
        if year < 2000 or year > current_year:
            raise ValueError(f"Ano inválido. Entre 2000 e {current_year}.")
    
    def _validate_plate(self, plate):
        plate = plate.upper().strip()
        if not self._PLATE_PATTERN.match(plate):
            raise ValueError("Matrícula inválida. Formatos aceites: " 
                             "AA-00-00, 00-AA-00, 00-00-AA, AA-00-AA, AA-000-AA")
        return plate

    def create_car(self, brand, model, year, plate, category, fuel_type, insurance, daily_rate):        
        required = {"Marca": brand, "Modelo": model, "Matrícula": plate,
            "Categoria": category, "Combustível": fuel_type, "Seguro": insurance}
        for field, value in required.items():
            if not str(value).strip():
                raise ValueError(f"{field} é obrigatório.")
        
        self._validate_year(year)
        plate = self._validate_plate(plate)
        self._validate_price(daily_rate)
        db.create_car(brand, model, year, plate, category, fuel_type, insurance, daily_rate)

    def update_car(self, car_id, brand, model, year, plate, category, fuel_type, insurance, daily_rate):
        if not car_id:
            raise ValueError("ID do carro é obrigatório.")
        
        required = {"Marca": brand, "Modelo": model, "Matrícula": plate,
            "Categoria": category, "Combustível": fuel_type, "Seguro": insurance}
        for field, value in required.items():
            if not str(value).strip():
                raise ValueError(f"{field} é obrigatório.")
        
        self._validate_year(year)
        plate = self._validate_plate(plate)
        self._validate_price(daily_rate)
        db.update_car(car_id, brand, model, year, plate, category, fuel_type, insurance, daily_rate)

    def delete_car(self, car_id):
        if not car_id:
            raise ValueError("ID do carro é obrigatório.")
        db.delete_car(car_id)

    def get_all_cars(self):
        return db.get_all_cars()
    