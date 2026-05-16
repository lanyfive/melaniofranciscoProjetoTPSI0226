import re
from datetime import datetime
import database as db

class CustomerService:
    def create_customer(self, nome, nif, idcard, birthdate, email, phone, address, drivinglicense):
        if not nome.strip() or not nif.strip() or not idcard.strip():
            raise ValueError("Nome, NIF e cartão de identidade são obrigatórios.")
        if not re.match(r'^\d{9}$', nif):
            raise ValueError("NIF inválido.")
        if not re.match(r'^\d{8}[A-Z]$', idcard):
            raise ValueError("Cartão de identidade inválido.")
        if birthdate:
            try:
                birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Data de nascimento inválida.")
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("E-mail inválido.")
        if phone and not re.match(r'^\d{9}$', phone):
            raise ValueError("Telefone inválido.")
        db.create_customer(nome, nif, idcard, birthdate, email, phone, address, drivinglicense)
