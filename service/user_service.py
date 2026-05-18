import re
from datetime import datetime
import database as db

class UserService:
    def create_user(self, nome, login, password, role):
        if not nome.strip() or not login.strip() or not password.strip():
            raise ValueError("Nome, login e senha são obrigatórios.")
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', login):
            raise ValueError("Login inválido.")
        if len(password) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres.")
        db.create_user(nome, login, password, role)

    def update_user(self, user_id, nome):
        if not user_id:
            raise ValueError("ID do usuário é obrigatório.")
        if not nome.strip():
            raise ValueError("Nome é obrigatório.")
        db.update_user(user_id, nome)

    def delete_user(self, user_id):
        if not user_id:
            raise ValueError("ID do usuário é obrigatório.")
        db.delete_user(user_id)

    def get_all_users(self):
        return db.get_all_users()
